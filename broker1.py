from flask import Flask, redirect, url_for, request, render_template
import os
import pika
import time
import socket
import threading
import json
from collections import defaultdict

def printit():
  threading.Timer(20.0, printit).start()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((socket.gethostname(), 1001))
  print("Client Connected to Server")
  client.send(str.encode('b1'))
  from_server =(client.recv(4096))
  int_val = from_server.decode('utf-8')
  print(int_val)
  client.close()

printit()




app = Flask(__name__)


topic = dict()
json_dict = defaultdict(list)

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        tname = request.form.get('tname')
        msg = request.form.get('msg')
        
        with open(os.getcwd()+"/broker1/sample.json",'r') as openfile:
            json_object=json.load(openfile)
            if tname not in json_object:
                json_object[tname]=[1]
            else:
                oldvalue=json_object[tname][len(json_object[tname])-1]
                json_object[tname].append(oldvalue+1)
            json_object=json.dumps(json_object)
            with open(os.getcwd()+"/broker1/sample.json",'w') as outfile:
                outfile.write(json_object)
            x = (oldvalue+1)%3
            print(x)

        isExist = os.path.exists(os.getcwd()+"/broker1/"+tname)

        if not isExist:
            os.mkdir(os.getcwd()+"/broker1/"+tname)
        with open(os.getcwd()+"/broker1/" + tname + '/' + tname+str(x)+'.txt', 'w') as temp_file:
            temp_file.write(msg)


        

        with open(os.getcwd()+'/broker1/log1.json','r') as openfile:
            json_object=json.load(openfile)
        if tname not in json_object:
            json_object[tname]=[msg]
        else:
            
            json_object[tname].append(msg)
        json_object=json.dumps(json_object)
        with open(os.getcwd()+'/broker1/log1.json','w') as outfile:
            outfile.write(json_object)


        os.remove(os.getcwd()+"/broker2/log1.json")
        with open(os.getcwd()+"/broker2/log1.json", 'w') as outfile:
            outfile.write(json_object)

        os.remove(os.getcwd()+"/broker3/log1.json")
        with open(os.getcwd()+"/broker3/log1.json", 'w') as outfile:
            outfile.write(json_object)


        f = open(os.getcwd()+"/broker1/" + tname + '/' + tname+str(x)+'.txt', "r")
        print(f.read())
        f = f.read()

        isExist = os.path.exists(os.getcwd()+"/broker2/"+tname)

        if not isExist:
            os.mkdir(os.getcwd()+"/broker2/"+tname)
        with open(os.getcwd()+"/broker2/" + tname + '/' + tname+str(x)+'.txt', 'w') as temp_file:
            temp_file.write(f)

        isExist = os.path.exists(os.getcwd()+"/broker3/"+tname)

        if not isExist:
            os.mkdir(os.getcwd()+"/broker3/"+tname)
        with open(os.getcwd()+"/broker3/" + tname + '/' + tname+str(x)+'.txt', 'w') as temp_file:
            temp_file.write(f)




        connection_param = pika.ConnectionParameters('localhost')

        connection = pika.BlockingConnection(connection_param)

        channel = connection.channel()

        channel.queue_declare(queue=tname)

        channel.basic_publish(
            exchange='', routing_key=tname, body=msg)

        print("Sent message :{msg}")

        connection.close()

        return "Topic = " + tname + " Message = " + msg
    return render_template("form.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
