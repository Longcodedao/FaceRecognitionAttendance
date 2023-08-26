from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_socketio import SocketIO
from module.FaceModule import FaceDetection
import base64
import os
import numpy as np
import cv2
import useDB


app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Combined with FrontEnd Version
@app.route('/indexNew')
def indexNew():
    return render_template('index_another.html')

@app.route('/tableNew')
def tableNew():
    student_data = useDB.students_collection.find()
    return render_template('table_another.html', student_data = student_data)

@app.route('/addNewStudent')
def addNewStudent():
    return render_template('addNewStudent.html')


@app.route('/addNewStudent', methods = ['POST'])
def addnewStudent():
    try: 
        data = request.json
        
        name = data['first_name']

        image =  data['image']
        image_json = image.split(",")[1]
        decoded_image_data = base64.b64decode(image_json)
        path = f"data/images/{name}/{name}.png"
        # Save the image
        if not os.path.exists(f"data/{name}"):
            os.makedirs(f"data/images/{name}")
        open(f"data/images/{name}/{name}.png", "wb").write(decoded_image_data)


        new_student = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "student_id": data['student_id'],
            "class": data['class_study'],
            "image_path":  path
        }

        results = useDB.students_collection.insert_one(new_student)

        return jsonify({'message': 'success'}, 200)


    except Exception as e:
        return jsonify({"message": str(e)}), 500 


@app.route('/data/images/<path:image_filename>')
def serve_data_image(image_filename):
    image_folder = os.path.join(app.root_path)
    return send_from_directory(image_folder, image_filename)


########################################################

@app.route('/capture_img')
def capture_img():
    return render_template('capture_img.html')

@app.route('/upload_capture_img', methods=['POST'])
def upload_capture_img():
    method = request.method
    if method == 'POST':
        # JSON to JPG
        name = request.json['name']
        # strim name
        name = name.strip()
        img_json = request.json['image'].split(",")[1]
        decoded_image_data = base64.b64decode(img_json)
        # Save the image
        if not os.path.exists(f"data/{name}"):
            os.makedirs(f"data/images/{name}")
        open(f"data/images/{name}/{name}.png", "wb").write(decoded_image_data)

        return jsonify({'message': 'success'}, 200)
    else:
        return jsonify({'message': 'method not allowed'}, 405)


@app.route('/api/studens', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_students():
    # get method
    method = request.method
    if method == 'GET':
        data_students = [] # get from db
        return jsonify(data_students, 200)
    elif method == 'POST':
        data_students = request.json['data_students']
        # insert to db
        return jsonify({'message': 'success'}, 200)
    elif method == 'PUT':
        data_students = request.json['data_students']
        # update to db
        return jsonify({'message': 'success'}, 200)
    elif method == 'DELETE':
        data_students = request.json['data_students']
        # delete from db
        return jsonify({'message': 'success'}, 200)
    else:
        return jsonify({'message': 'method not allowed'}, 405)


@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('image_data')
def receive_image(data):
    image_data = data['data']
    # Process the received image data (decode base64)
    # convert string of image_data to uint8
    nparr = np.fromstring(base64.b64decode(image_data), np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect face
    face_detection = FaceDetection(img)

    cv2.show('image', face_detection)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
