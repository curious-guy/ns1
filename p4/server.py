import ast
from flask import Flask, request
import pymongo
import json
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["local"]
my_collection = my_db["devices4"]


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/get_data', methods=['GET'])
def get_data():
    if request.method == 'GET':
        return_string = ''
        for x in my_collection.find():
            return_string += str(x) + '\n\n'
        return return_string


@app.route('/post_data', methods=['POST'])
def post_data():
    if request.method == 'POST':
        data = dict(request.form)
        for k in data:
            data = k
            break
        data = json.loads(data)
        return_string = ''
        arr = []
        for device in data:
            for timestamp in data[device]:
                inner_dict = {'device': device, 'timestamp': timestamp}
                return_string += device + ', ' + timestamp + ', '
                for k in data[device][timestamp]:
                    if data[device][timestamp][k] and k == 'warning':
                        return_string += '****' + (str(data[device][timestamp][k])).upper() + '****, '
                    else:
                        return_string += str(data[device][timestamp][k]) + ', '
                    inner_dict[k] = data[device][timestamp][k]
                return_string += '\n'
                arr.append(inner_dict)
        x = my_collection.insert_many(arr)
        print(return_string)
        return return_string


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0')

