import random
from datetime import datetime, date
from json import JSONEncoder
from time import sleep

import pymqi
import os
import sys
import json
import logging


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()


def loop(connection, queue_high, queue_low, name):
    recipients = ['Subscriber01', 'Subscriber02', 'Subscriber03']
    while True:
        pause = random.randint(10, 30)
        sleep(float(pause) / 10.)
        value = random.randint(1, 100)
        message = {'timestamp': datetime.now(), 'source': name, 'value': value}
        if value < 10:
            logging.info('sending {}'.format(message))
            queue_low.enqone(connection.msgproperties(payload=json.dumps(message, cls=DateTimeEncoder), recipients=recipients))
        elif value > 90:
            logging.info('sending {}'.format(message))
            queue_high.enqone(connection.msgproperties(payload=json.dumps(message, cls=DateTimeEncoder), recipients=recipients))

        connection.commit()


def main(name):

    queue_manager = pymqi.connect('QM.1', 'SVRCONN.CHANNEL.1', '192.168.1.121(1434)')

    q = pymqi.Queue(queue_manager, 'TESTQ.1')
    q.put('Hello from Python!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    if len(sys.argv) != 2:
        logging.error('missing argument: source name')
        sys.exit(-1)

    try:
        main(sys.argv[1])

    except KeyboardInterrupt:
        print('Goodbye!')
