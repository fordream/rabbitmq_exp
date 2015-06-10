#!/usr/bin/env python
import pika
from pika.credentials import *
import time
import sys
import thread

def callback(ch, method, properties, body):
    time.sleep(body.count("."))
    print " [{}] Received {}".format(ch, body,)
    ch.basic_ack(delivery_tag = method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.0.1', credentials=PlainCredentials("test","pass")))
channels=[]
for i in range(0,int(sys.argv[1])):
    channel = connection.channel()
    channel.queue_declare(queue='hello', durable=True)
    channel.basic_qos(prefetch_count=1)
    #channel.basic_consume(callback,queue='hello', no_ack=True)
    channel.basic_consume(callback,queue='hello', no_ack=False)
    channels.append(channel)
for channel in channels:
    print '[{}] Waiting for messages. To exit press CTRL+C'.format(channel)
    print "start consuming messages"
    try:
        thread.start_new_thread(channel.start_consuming,())
    except Exception as e:
        print e
time.sleep(50)
