import asyncio

from confluent_kafka import Consumer


BROKER_URL = "localhost:31090"
TOPIC_NAME = "police.service-calls"


def consume():

    c = Consumer({
        'bootstrap.servers': BROKER_URL,
        'group.id': 'grp1',
        'auto.offset.reset': 'earliest'
    })

    c.subscribe([TOPIC_NAME])

    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        print('Received message: {}'.format(msg.value().decode('utf-8')))


def main():
    try:
        consume()
    except KeyboardInterrupt as e:
        print("shutting down")


if __name__ == "__main__":
    main()
