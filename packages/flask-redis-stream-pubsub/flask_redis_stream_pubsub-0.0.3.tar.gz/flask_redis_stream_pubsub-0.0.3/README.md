# flask-redis-stream-pubsub

`A message queue implemented based on Redis Stream`

**Advantages**:
1. **High Speed**: Redis stores data in memory, which offers very high read and write performance. This is particularly advantageous for applications that require low latency.
2. **Data Persistence**: Redis can offer data persistence by saving data to disk, meaning that messages will not be lost even if Redis restarts.
3. **Wide Range of Use Cases**: Redis can be used not only as a message queue but also as a cache, database, distributed lock, and more, reducing the complexity of the technology stack.
4. **Message Traceability**: Supports persistent storage of messages, allowing consumers to trace back messages.
5. **Support for Multiple Consumers**: Allows multiple consumers to compete for messages, speeding up the consumption rate.
6. **Blocking Read**: Supports blocking reads, ensuring there is no risk of missing messages.
7. **Message Acknowledgment Mechanism**: Supports consumer acknowledgment mechanisms, ensuring that messages are consumed at least once.

**Application Scenarios**:
1. **Asynchronous Processing**: Suitable for scenarios that require asynchronous processing, such as order handling and payment notifications.
2. **Load leveling (Peak Shaving and Valley Filling)**: During peak traffic periods, using a message queue can smooth out requests, preventing system overload.
3. **Data Broadcasting**: Suitable for scenarios where data needs to be broadcast to multiple consumers.
4. **Off-peak and Flow Control**: When the volume of data is too large, the message queue can allow for a certain amount of message accumulation, achieving off-peak processing.
5. **Eventual Consistency**: In distributed systems, using a message queue can achieve eventual consistency.
6. **Simple Small to Medium-sized Projects**: If the functionality is simple and the volume of access is not high, Redis Stream can be considered as a message queue.

## ⚙ Installation

```shell
pip install flask-redis-stream-pubsub
```

## ⚡ Quickstart

### 发送消息
```python
from flask import Flask

from flask_redis_stream_pubsub.pubsub import Producer

app = Flask(__name__)
app.config.from_object("example.config")

if __name__ == '__main__':
    producer = Producer()

    producer.init_app(app)
    
    #发送一条消息
    msgid = producer.publish("hello_word", {'name': 'dog'})
    print(msgid)


    # 批量发送
    sess = producer.session
    sess.add("hello_word", {'name': 'cat1'})
    sess.add("hello_word", {'name': 'cat2'})
    sess.add("hello_word", {'name': 'cat3'})
    sess.add("hello_word", {'name': 'cat4'})
    sess.add("hello_word", {'name': 'cat5'})

    msgids = sess.publish()
    print(msgids)
```

### 订阅消息
```python
import logging

from flask import Flask, current_app
from flask_redis_stream_pubsub.pubsub import Consumer, Msg

app = Flask(__name__)
app.config.from_object("example.config")
app.logger.setLevel(logging.INFO)

if __name__ == '__main__':
    cs = Consumer(__name__)


    @cs.subscribe("hello_word")
    def hello_word(msg: Msg):
        """ 业务代码没抛出异常, 就代表消费成功 """
        current_app.logger.info(msg)


    @cs.subscribe("hello_word", retry_count=3, timeout=30)
    def hello_word(msg: Msg):
        """ 重试3次, 每次间隔30秒 """
        current_app.logger.info(msg)
        raise RuntimeError("I will retry 3 times, with a 30 second interval between each attempt")


    @cs.subscribe("hello_word_cron", cron="*/5 * * * * *", retry_count=0)
    def hello_word_cron(msg: Msg):
        """ 每5秒执行一次, 不重试 """
        current_app.logger.info(msg)


    cs.init_app(app)
    cs.run("consumer:app")

```

### `example.config`

```python
PUBSUB_REDIS_URL = 'redis://:password@host:6379/0'
PUBSUB_REDIS_OPTION = {
    'group':'pubsub_g1', #消息分组 -> redis XGROUP groupname
    'workers':10, #消费进程数
    'retry_count':32, #默认重试次数
    'timeout_second':300, #默认超时时间，未来超时时间消费成功，将进行重试
    'block_second': 6, #读取消息的阻塞时间 -> xreadgroup block=6
    'read_count': 16, #一次最多读取的消息数量 -> xreadgroup read_count=16
}
```


> See [examples](/example)

## License

*MIT*