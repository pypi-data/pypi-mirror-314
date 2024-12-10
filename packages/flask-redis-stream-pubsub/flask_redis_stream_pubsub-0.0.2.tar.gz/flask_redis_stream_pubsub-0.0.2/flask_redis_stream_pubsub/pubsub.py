import asyncio
import logging
import os
import signal
import time
import traceback
import uuid
from functools import wraps
from multiprocessing import current_process, Pool, Process
from typing import Callable, Dict, List

import redis
from croniter import croniter
from flask import Flask, current_app, has_app_context
from flask.globals import app_ctx
from werkzeug.utils import import_string, find_modules
from redis import asyncio as aioredis

RESET = '\033[0m'

logger = logging.getLogger("rs")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logger.level)

formatter = logging.Formatter(f"[%(asctime)s] RS %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

PRODUCER_SESSION_BUFFER_SIZE = 16

SCHEDULER_PIPE_BUFFER_SIZE = 16
SCHEDULER_INTERVAL = 0.2
SCHEDULER_FIRST_DELAY = 1
SCHEDULER_JOB_STREAM_MAX_LEN = 256
SCHEDULER_LOCK_KEY_EX = 8

CONSUMER_RETRY_INTERVAL = 2

DEFAULT_STREAM_MAX_LEN = 2048


class Msg:
    __slots__ = ['stream_name', 'id', 'group_name', 'payload', 'consumer_name', 'retry_count']

    def __init__(self, stream_name, id, group_name, payload: Dict, consumer_name, retry_count=0):
        self.stream_name = stream_name
        self.id = id
        self.group_name = group_name
        self.payload: dict = payload
        self.consumer_name = consumer_name
        self.retry_count = retry_count

    def __str__(self):
        return f"Msg({self.consumer_name}-{self.id}-{self.stream_name}-{self.payload}-{self.group_name}-{self.retry_count})"

    @property
    def source(self) -> str:
        if '__SOURCE' in self.payload:
            return self.payload['__SOURCE']
        return ''

    @property
    def publish_time(self) -> int:
        if '__PUBLISH_TIME' in self.payload:
            return int(self.payload['__PUBLISH_TIME'])
        return 0


def _chunk_array(arr, size):
    return [arr[i:i + size] for i in range(0, len(arr), size)]


class Producer:
    __slots__ = ['maxlen', '__rcli']

    def __init__(self, redis_url='', maxlen=DEFAULT_STREAM_MAX_LEN):
        self.maxlen = maxlen
        self.__rcli = None
        if redis_url:
            self.__rcli = redis.from_url(redis_url, decode_responses=True)

    def init_redis(self, redis_url=''):
        self.__rcli = redis.from_url(redis_url, decode_responses=True)

    def init_app(self, app: Flask, config_prefix='PUBSUB_REDIS'):
        redis_url = app.config.get(
            "{0}_URL".format(config_prefix), "redis://localhost:6379/0"
        )

        rcli = redis.from_url(redis_url, decode_responses=True)
        self.__rcli = rcli

    def publish(self, stream_name: str, payload: dict, maxlen=None):
        __maxlen = maxlen if maxlen else self.maxlen
        payload['__PUBLISH_TIME'] = int(time.time() * 1000)
        payload['__SOURCE'] = 'producer'
        return self.__rcli.xadd(stream_name, payload, maxlen=__maxlen)

    @property
    def session(self):
        if has_app_context():
            if not hasattr(app_ctx, 'producer_session'):
                app_ctx.producer_session = ProducerSession(self.__rcli, self.maxlen)
            return app_ctx.producer_session

        return ProducerSession(self.__rcli, self.maxlen)


class ProducerSession:
    __slots__ = ['__rcli', 'maxlen', 'msgs']

    def __init__(self, rcli: redis.Redis, maxlen=None):
        self.__rcli = rcli
        self.msgs = []  # type:List
        self.maxlen = maxlen

    def add(self, stream_name: str, payload: dict, maxlen=None):
        __maxlen = maxlen if maxlen else self.maxlen
        self.msgs.append({
            'name': stream_name,
            'payload': payload,
            'maxlen': maxlen,
        })

    def clear(self):
        self.msgs = []

    def publish(self):
        __msgs = self.msgs[:]
        self.clear()

        __msg_groups = _chunk_array(__msgs, PRODUCER_SESSION_BUFFER_SIZE)
        res = []

        for msg_list in __msg_groups:
            with self.__rcli.pipeline() as pipe:
                current_time = int(time.time() * 1000)
                for msg in msg_list:
                    payload = msg['payload']
                    payload['__PUBLISH_TIME'] = current_time
                    payload['__SOURCE'] = 'producer'
                    pipe.xadd(msg['name'], payload, maxlen=msg['maxlen'])

                pipe_res = pipe.execute()
                if isinstance(pipe_res, list):
                    res.extend(pipe_res)

        return res


class Consumer:

    def __init__(self,
                 consumer_name: str,
                 group='',
                 workers=4,
                 retry_count=64,
                 timeout_second=300,
                 block_second=6,
                 read_count=10,
                 config_prefix='PUBSUB_REDIS',
                 app_factory: str | Callable = None):

        self.app_factory = app_factory
        self.group = group
        self.timeout_mill = timeout_second * 1000
        self.block_mill = block_second * 1000
        self.read_count = read_count
        self.rcli = None
        self.workers = workers
        self.retry_count = retry_count
        self.consumer_name = consumer_name

        self.__runing = True
        self.__call_map = {}
        self.xgroup_check = None
        self.woker_pool = None

        self.config_prefix = config_prefix
        self.redis_url = ''

    def init_obj(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)

        cfg = {}
        for key in dir(obj):
            if key.isupper():
                cfg[key] = getattr(obj, key)

        redis_url = cfg.get(
            "{0}_URL".format(self.config_prefix), "redis://localhost:6379/0"
        )
        self.redis_url = redis_url
        self.__init_config(cfg)

    def __init_config(self, cfg):
        if 'group' in cfg:
            self.group = cfg['group']
        if 'workers' in cfg:
            self.workers = cfg['workers']
        if 'retry_count' in cfg:
            self.retry_count = cfg['retry_count']
        if 'timeout_second' in cfg:
            self.timeout_mill = int(cfg['timeout_second']) * 1000
        if 'block_second' in cfg:
            self.block_mill = int(cfg['block_second']) * 1000
        if 'read_count' in cfg:
            self.read_count = cfg['read_count']
        if 'app_factory' in cfg:
            self.app_factory = cfg['app_factory']

    def init_app(self, app: Flask):
        redis_url = app.config.get(
            "{0}_URL".format(self.config_prefix), "redis://localhost:6379/0"
        )
        self.redis_url = redis_url

        cfg = app.config.get(f'{self.config_prefix}_OPTION')

        if not cfg:
            return

        self.__init_config(cfg)

    def import_module(self, module: str):
        for name in find_modules(module, recursive=True, include_packages=False):
            import_string(name)

    def subscribe(self, stream: str, timeout: float = None, retry_count: int = None, cron: str = None):
        if retry_count is None:
            retry_count = self.retry_count

        def decoration(f):
            if stream in self.__call_map:
                raise RuntimeError(f'{stream} Already exists of call_map')

            module = __import__(f.__module__, fromlist=[''])
            name = f.__name__

            if cron is None:
                self.__call_map[stream] = {
                    'module': module,
                    'name': name,
                    'type': 'subscribe',
                    'timeout': timeout,
                    'retry_count': retry_count,
                }
            else:
                if not croniter.is_valid(cron):
                    raise RuntimeError(f'{stream} cron It is invalid by {cron}')

                self.__call_map[stream] = {
                    'module': module,
                    'name': name,
                    'type': 'cron',
                    'cron': cron,
                    'iter': croniter(cron, second_at_beginning=True),
                    'stream': stream,
                    'timeout': timeout,
                    'retry_count': retry_count,
                }

            @wraps(f)
            def wrapper(*args, **kwargs):
                with current_process().app.app_context():
                    ack = False
                    try:
                        msg = args[0]
                        f(*args, **kwargs)
                        ack = True
                    except Exception as e:
                        ack = False
                        current_app.logger.error(f'\033[91m{traceback.format_exc()}')
                        raise e
                    finally:
                        cli = current_process().rcli
                        if retry_count <= 0:
                            ack = True
                        if ack:
                            ack_result = cli.xack(msg.stream_name, msg.group_name, msg.id)
                            if ack_result == 1:
                                cli.xdel(msg.stream_name, msg.id)

            return wrapper

        return decoration

    async def __retry(self, fix_call_map):
        while self.__runing:
            async with self.rcli.pipeline() as pipe:
                stream_list = []
                for k, val in self.__call_map.items():
                    _timeout_mill = self.timeout_mill
                    _opt_timeout = val['timeout']

                    if _opt_timeout:
                        _timeout_mill = int(float(_opt_timeout) * 1000)

                    _retry_count = val['retry_count']
                    stream_list.append({
                        'name': k,
                        'retry_count': _retry_count,
                        'timeout_mill': _timeout_mill,
                    })
                    await pipe.xpending_range(k, self.group, "0", "+",
                                              count=self.read_count, idle=_timeout_mill)

                res = await pipe.execute()

            call_count = 0
            for i in range(len(res)):
                message_ids = []
                message_del_ids = []
                times_delivered_map = {}

                stream_dict = stream_list[i]
                name = stream_dict['name']
                retry_count = stream_dict['retry_count']
                timeout_mill = stream_dict['timeout_mill']

                for d in res[i]:
                    if d['times_delivered'] > retry_count:
                        message_del_ids.append(d['message_id'])
                    else:
                        mid = d['message_id']
                        message_ids.append(mid)
                        times_delivered_map[mid] = d['times_delivered']

                if message_del_ids:
                    act_count = await self.rcli.xack(name, self.group, *message_del_ids)
                    if act_count > 0:
                        await self.rcli.xdel(name, *message_del_ids)

                if message_ids and name in fix_call_map:
                    call = fix_call_map[name]
                    xmsgs = await self.rcli.xclaim(name, self.group,
                                                   self.consumer_name, timeout_mill, message_ids)

                    for msg in xmsgs:
                        id = msg[0]
                        payload = msg[1]
                        times_delivered = times_delivered_map[id]

                        _msg = Msg(name, id, self.group, payload,
                                   self.consumer_name, retry_count=times_delivered)

                        self.woker_pool.apply_async(call, (_msg,))
                        call_count += 1

            if call_count > 0:
                await asyncio.sleep(0)
            else:
                await asyncio.sleep(CONSUMER_RETRY_INTERVAL)

    async def __xread(self, fix_call_map, streams):
        while self.__runing:
            rets = await self.rcli.xreadgroup(self.group, self.consumer_name, streams,
                                              count=self.read_count, block=self.block_mill)
            for ret in rets:
                stream = ret[0]
                if stream not in fix_call_map:
                    current_app.logger.error(f'{stream} not in call funcs')
                    continue

                for msg in ret[1]:
                    id = msg[0]
                    payload = msg[1]

                    _msg = Msg(stream, id, self.group, payload, self.consumer_name)

                    call = fix_call_map[stream]
                    self.woker_pool.apply_async(call, (_msg,))

    async def __job_pipe_xadds(self, jobs):
        async with self.rcli.pipeline() as pipe:
            for j in jobs:
                key = f'{j["stream"]}_{j["next_time"]}'
                uid = str(uuid.uuid4()).replace("-", "").upper()
                await pipe.set(f'{key}', uid, ex=SCHEDULER_LOCK_KEY_EX, nx=True)

            res = await pipe.execute()

            xcount = 0
            for i in range(len(jobs)):
                if res[i]:
                    job = jobs[i]
                    payload = {
                        '__PUBLISH_TIME': int(time.time() * 1000),
                        '__SOURCE': 'cron',
                    }
                    await pipe.xadd(job['stream'], payload, maxlen=SCHEDULER_JOB_STREAM_MAX_LEN)
                    xcount += 1

            if xcount > 0:
                await pipe.execute()

            return xcount

    async def __scheduler(self, jobs):
        await asyncio.sleep(SCHEDULER_FIRST_DELAY)

        __jobs = []
        for job in jobs:
            __jobs.append({
                'iter': job['iter'],
                'stream': job['stream'],
                'last_time': 0,
            })

        while self.__runing:
            current_time = time.time()
            zjobs_list = []

            for job in __jobs:
                _next_time = job['iter'].get_next(start_time=current_time)

                if job['last_time'] != _next_time:
                    zjobs_list.append({
                        'stream': job["stream"],
                        'next_time': _next_time,
                    })
                    job['last_time'] = _next_time

            if zjobs_list:
                chunkd_jobs = _chunk_array(zjobs_list, SCHEDULER_PIPE_BUFFER_SIZE)
                await asyncio.gather(*map(self.__job_pipe_xadds, chunkd_jobs))

            await asyncio.sleep(SCHEDULER_INTERVAL)

    def run(self, app_factory: str | Callable = None, **kwargs):
        redis_url = kwargs.get('redis_url')
        group = kwargs.get('group')
        workers = kwargs.get("workers")
        retry_count = kwargs.get("retry_count")
        timeout_second = kwargs.get("timeout_second")
        block_second = kwargs.get("block_second")
        read_count = kwargs.get("read_count")
        config_prefix = kwargs.get("config_prefix")

        if redis_url:
            self.redis_url = redis_url
        if group:
            self.group = group
        if workers:
            self.workers = workers
        if retry_count:
            self.read_count = retry_count
        if timeout_second:
            self.timeout_mill = int(timeout_second)*1000
        if block_second:
            self.block_mill = int(block_second) * 1000
        if read_count:
            self.read_count = read_count
        if config_prefix:
            self.config_prefix = config_prefix

        try:
            from uvloop import run
            logger.info(f'PID({os.getpid()}) {'\033[1m'}uvloop runing...{RESET}')
        except ImportError:
            from asyncio import run
            logger.info(f'PID({os.getpid()}) {'\033[1m'}eventloop runing...{RESET}')

        run(self.run_async(app_factory))

    async def run_async(self, app_factory: str | Callable = None):
        if app_factory is None:
            app_factory = self.app_factory

        self.woker_pool = Pool(self.workers, initializer=self.__init_process, initargs=(app_factory,))

        self.rcli = aioredis.from_url(self.redis_url, decode_responses=True)

        __fix_call_map = {}
        streams = {}

        job_list = []
        for k, v in self.__call_map.items():
            __fix_call_map[k] = getattr(v['module'], v['name'])
            streams[k] = '>'
            try:
                await self.rcli.xgroup_create(name=k, groupname=self.group, id='0', mkstream=True)
            except redis.exceptions.ResponseError:
                pass

            if v['type'] == 'cron':
                job_list.append(v)

        if not __fix_call_map:
            raise RuntimeError('Not subscribe')

        logger.info(
            f"PID({os.getpid()}) {'\033[94m'}Parameters: workers={self.workers},consumer_name={self.consumer_name},group_id={self.group}{RESET}")
        logger.info(f"PID({os.getpid()}) {'\033[96m'}Discovery of subscribers: {",".join(streams.keys())}{RESET}")

        def __shutdown(signum, frame):
            self.__runing = False
            logger.warning(
                f"PID({os.getpid()}) {'\033[93m'}Listen signum:{signum}, Start to shutdown...PID({os.getpid()}){RESET}")

        signal.signal(signal.SIGINT, __shutdown)
        signal.signal(signal.SIGTERM, __shutdown)

        tasks = [
            self.__xread(__fix_call_map, streams),
            self.__retry(__fix_call_map),
        ]
        if job_list:
            tasks.append(self.__scheduler(job_list))

        await asyncio.gather(*tasks)

        self.woker_pool.close()
        self.woker_pool.join()

        logger.info(f"PID({os.getpid()}) {'\033[92m'}Shutting down consumer successfully PID({os.getpid()}){RESET}")

    def __init_process(self, app_factory: str | Callable):
        app: Flask
        if isinstance(app_factory, str):
            app = import_string(app_factory)
        elif callable(app_factory):
            app = app_factory()
        else:
            raise RuntimeError("flask app is not initialization")

        if app is None:
            raise RuntimeError("flask app is not initialization")

        redis_url = app.config.get(
            "{0}_URL".format(self.config_prefix), "redis://localhost:6379/0"
        )

        rcli = redis.from_url(redis_url, decode_responses=True)

        current_process().rcli = rcli
        current_process().app = app


def runs(*consumers: Consumer, app_factory: str | Callable = None):
    if len(consumers) == 0:
        raise RuntimeError("consumers cannot be empty")

    plist = []

    for c in consumers:
        p = Process(target=c.run, args=(app_factory,))
        plist.append(p)
        p.start()

    def shutdown(signum, frame):
        for p in plist:
            p.terminate()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for p in plist:
        p.join()
