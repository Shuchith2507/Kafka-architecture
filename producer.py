import pika
import sys
import socket

# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
topic_name =  str(sys.argv[1])
message =   str(sys.argv[2])
connection_param = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_param)

channel = connection.channel()

channel.queue_declare(queue=topic_name)

channel.basic_publish(exchange='', routing_key=topic_name, body=message)

print("Sent message :{message}")

connection.close()



if __name__ == '_main_':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to connect to the given host and port
    if sock.connect_ex(('0.0.0.0', 8000)) == 0:
        app.run(port=8000)  #broker2
    elif sock.connect_ex(('0.0.0.0', 7000)) == 0:
        app.run(port=7000)
    elif sock.connect_ex(('0.0.0.0', 9000)) == 0:
        app.run(port=9000)
    else:
        print("No brokers available")
    
    sock.close()