#!/usr/bin/env python
import pika
from pika.credentials import *
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
               '172.17.0.1', credentials=PlainCredentials("test","pass")))
channel = connection.channel()
channel.queue_declare(queue='hello', durable=True)

for i in range(0,int(sys.argv[1])):
    msg="t{}".format(i)
    for j in range(0,i):
        msg+='.'
    channel.basic_publish(exchange='', routing_key='hello', body=msg, 
        properties=pika.BasicProperties(delivery_mode = 2,))
    print "send {}".format(msg)
                       
connection.close()
