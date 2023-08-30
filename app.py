from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, flash
from flask_socketio import SocketIO, emit
from module.FaceModule import FaceDetection
import os
import numpy as np
import cv2
import useDB
import base64
from utils import setupPathImage, check_datetime
from datetime import datetime
import shutil
from bson import ObjectId

app = Flask(__name__)
socketio = SocketIO(app)
image_path = "data/images"

# @app.route('/')
# def index():
#     return render_template('index.html')

# Combined with FrontEnd Version
@app.route('/')
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

        path = setupPathImage(image, name)


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


@app.route('/editStudent/<student_id>')
def edit_student(student_id):
    student = useDB.students_collection.find_one({"student_id": student_id})
    return render_template("edit_student.html", student = student)


@app.route('/deleteStudent/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = useDB.students_collection.find_one({"student_id": student_id})
        student_name = student['first_name']
        shutil.rmtree(os.path.join(image_path, student_name))
        print("Successfully remove the image")

        result = useDB.students_collection.delete_one({"student_id": student_id})
        if result.deleted_count > 0:
            print("Student deleted")
            return jsonify({'message': 'success'}, 200)
        else:
            return jsonify({'message': 'Student not found'}, 404)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/editStudent/<student_id>', methods = ['POST'])
def edit_student_post(student_id):
    print("Hello World")

    try:
        data = request.json
        path = request.json['image']
        # print(path.split(","))

        if (len(data['image'].split(",")) >= 2):
            path = setupPathImage(data['image'], data['first_name'])

        # print(path)
        updated_data = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "class": data['class_study'],
            "image_path":  path
            
        }

        print(updated_data)

        useDB.students_collection.update_one({"student_id": student_id}, {"$set": updated_data})
        return jsonify({'message': 'success'}, 200)  # Redirect to student table page

    except Exception as e:
        return jsonify({"message": str(e)}), 500 

@app.route('/attendance')
def attendance():
    return render_template('attendance_another.html')


@app.route('/recognized_person', methods=['POST'])
def process_frame():
    try:
        data = request.json
        name = data['name']
        classroom_name = data['classroom']
        
        if not classroom_name:
            return jsonify({'error': 'Class name is not provided'}), 400

        found_class = useDB.classroom_db.find_one({'class_code': classroom_name})
        if not found_class:
            return jsonify({'error': 'Class not found'})

        time = datetime.now()
        print(type(time))
        print(type(found_class['start_time']))
        late = check_datetime(time, found_class['start_time'])

        attendance_data = {
            "name": name,
            "classroom_name": classroom_name,
            "time": time,
            "late": late
        }
        useDB.students_attendance.insert_one(attendance_data)
        response_data = {'status': 'success', 
                         'message': f'Attendance recorded [Name: {name}, Classroom: {classroom_name}]'}        
      
        return jsonify(response_data), 200
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({'message': 'Error processing frame'}), 500




########################################################

# @app.route('/capture_img')
# def capture_img():
#     return render_template('capture_img.html')

# @app.route('/upload_capture_img', methods=['POST'])
# def upload_capture_img():
#     method = request.method
#     if method == 'POST':
#         # JSON to JPG
#         name = request.json['name']
#         # strim name
#         name = name.strip()
#         img_json = request.json['image'].split(",")[1]
#         decoded_image_data = base64.b64decode(img_json)
#         # Save the image
#         if not os.path.exists(f"data/{name}"):
#             os.makedirs(f"data/images/{name}")
#         open(f"data/images/{name}/{name}.png", "wb").write(decoded_image_data)

#         return jsonify({'message': 'success'}, 200)
#     else:
#         return jsonify({'message': 'method not allowed'}, 405)


# @app.route('/api/studens', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def get_students():
#     # get method
#     method = request.method
#     if method == 'GET':
#         data_students = [] # get from db
#         return jsonify(data_students, 200)
#     elif method == 'POST':
#         data_students = request.json['data_students']
#         # insert to db
#         return jsonify({'message': 'success'}, 200)
#     elif method == 'PUT':
#         data_students = request.json['data_students']
#         # update to db
#         return jsonify({'message': 'success'}, 200)
#     elif method == 'DELETE':
#         data_students = request.json['data_students']
#         # delete from db
#         return jsonify({'message': 'success'}, 200)
#     else:
#         return jsonify({'message': 'method not allowed'}, 405)


@app.route('/search')
def search_student():
    query = request.args.get('query')
    res = useDB.classroom_db.find_one({'class_code': query})
    if not res:
        return jsonify({"message": "Cannot find the Class"}), 404
    
    print(res['class_name'])

    attendance_list = list(useDB.students_attendance.find({'classroom_name': query}))
    for attendance_record in attendance_list:
        attendance_record['_id'] = str(attendance_record['_id'])

    return jsonify({"classname" : res['class_name'], "attendance" : attendance_list}), 200


@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')


@socketio.on('image_data')
def receive_image(data):
    image_data = data['data']
    image_json = image_data.split(",")[1]


    # Process the received image data (decode base64)
    # convert string of image_data to uint8
    image_decode = base64.b64decode(image_json)
    nparr = np.frombuffer(image_decode, dtype = np.uint8)
    # print(nparr.shape)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # print(img.shape)
    # Detect face
    face_detection = FaceDetection(img)
    
    # cv2.imread("image", face_detection)
    # Encode the process image as base64
    _, buffer = cv2.imencode('.jpg', face_detection)    
    processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # emit return
    emit('processed_image', {'image_predict': processed_image_base64})


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
