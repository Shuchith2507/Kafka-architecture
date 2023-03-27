# import pika


# def on_message_received(ch, method, properties, body):
#     print(f"received new message: {body}")


# connection_parameters = pika.ConnectionParameters('localhost')

# connection = pika.BlockingConnection(connection_parameters)

# channel = connection.channel()

# channel.queue_declare(queue='letterbox1')

# channel.basic_consume(queue='letterbox1', auto_ack=True,
#                       on_message_callback=on_message_received)

# print("Starting Consuming")

# channel.start_consuming()

import pika
import json
import sys
import os

Topic_name= str(sys.argv[1])
action = str(sys.argv[2])


def on_message_received(ch, method, properties, body):
    print(f"received new message: {body}")


connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()


def action1():
    with open(os.getcwd()+"/broker2/log1.json", 'r') as temp_file:
        data = json.load(temp_file)
        print(data[Topic_name])
    pass
if action:
    if action == "--from-beginning":
        action1()
        
    elif action == "--from-producer":
        

        channel.queue_declare(queue= Topic_name)

        channel.basic_consume(queue=Topic_name, auto_ack=True,
                            on_message_callback=on_message_received)

        print("Starting Consuming")

        channel.start_consuming()
    
    else:
        print("Invalid flag")