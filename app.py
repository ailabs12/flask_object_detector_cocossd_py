from flask import Flask, json, request
from copy import deepcopy
import asyncio
import time #замер времени
import threading
import queue

import sys, base64
sys.path.append('./object_detector_cocossd_py') #Опускаемся на уровень ниже, так как там находится модуль детекции объектов и лиц (в файле object_detector_cocossd.py)
from object_detector_cocossd import classifyImg #Подгружаем модуль детекции объектов
from object_detector_cocossd import detectFaces #Подгружаем модуль детекции лиц

import json as jsonClass
path = 'CocoClassNames.json'
try:
	with open(path, 'r') as f:
		data = jsonClass.load(f)
except:
	print('ERROR! Could not read file CocoClassNames.json')
	raise

def get_objects(img_b64,q):
	return q.put_nowait(classifyImg(img_b64))

def get_faces(img_b64,q):
	return q.put_nowait(detectFaces(img_b64))

app = Flask(__name__)

@app.route("/", methods=['POST'])
def detectorCocossd():
	if (not is_valid_request(request)):
		return json.jsonify(get_json_response(msg='Invalid request'))

	#Получаем запрошенные классы или None, если параметр 'classes' не получен
	classes = request.json.get('classes', None)

	#Переменная для проверки присутствия других классов, кроме класса 'лицо'/'face'  в параметре 'classes'
	flag_classes = False
	#Переменная для проверки присутствия класса 'лицо'/'face'  в параметре 'classes'
	flag_faces = False
	#Переменная для проверки присутствия данных в параметре 'classes'
	separation = False

	#Заходим сюда, если класс(-ы) введён(-ены)
	if classes is not None and classes and not classes.isspace():
		classes = classes.lower()
		separation = True
		#Проверка присутствия класса 'лицо'/'face' в параметре 'classes'
		if (data[str(81)]['Rus'] in classes) or (data[str(81)]['Eng'] in classes):
			flag_faces = True
		#Проверка присутствия других классов, кроме класса 'лицо'/'face' в параметре 'classes'
		for i in range(len(data)):
			if ((data[str(i)]['Rus'] in classes) or (data[str(i)]['Eng'] in classes)) and (i!=81):
				flag_classes = True
				break

	img_b64 = get_request_data(request) #(string img_b64) (tuple get_request_data(request))
	img_header = get_image_header(img_b64)
	img_body = get_image_body(img_b64)

	if (img_body is None):
		return json.jsonify(get_json_response(msg='Image not found'))

	prediction_result_objects = None
	prediction_result_faces = None

	'''Отправка на детекцию в зависимости от значения параметра 'classes' '''
	if not flag_faces and not flag_classes:
		#Классы не введены, отправляем на детекцию лиц и объектов
		if not separation:
			prediction_result_objects = classifyImg(img_b64) #list objects
			prediction_result_faces = detectFaces(img_b64) #list faces
		#Классы введены некорректно, выводим список всех классов
		else:
			all_classes = ""
			for i in range(len(data)):
				all_classes = all_classes + data[str(i)]['Rus'] + "/" + data[str(i)]['Eng'] + ", "
			all_classes = all_classes.rstrip(', ')
			return json.jsonify(get_json_response(msg='Available classes: '+all_classes)) #No classes found

	#Классы введены, лица не найдены, объекты найдены
	#отправляем на детекцию объектов
	if not flag_faces and flag_classes:
		prediction_result_objects = classifyImg(img_b64) #list objects

	#Классы введены, лица найдены, объекты не найдены
	#отправляем на детекцию лиц
	if flag_faces and not flag_classes:
		prediction_result_faces = detectFaces(img_b64) #list faces

	#Классы введены, лица и объекты найдены
	#отправляем на детекцию лиц и объектов
	if flag_faces and flag_classes:

		#start_time = time.time() #замер времени

		qe_obj = queue.Queue()
		qe_faces = queue.Queue()

		t_get_objects = threading.Thread(name = 'get_objects', target = get_objects, args = (img_b64,qe_obj))

		t_get_faces = threading.Thread(name = 'get_faces', target = get_faces, args = (img_b64,qe_faces))

		t_get_objects.start()
		t_get_faces.start()

		while t_get_objects.is_alive() or t_get_faces.is_alive(): # пока функция выполняется
			prediction_result_objects = qe_obj.get()
			if not t_get_faces.is_alive():
				prediction_result_faces = qe_faces.get()

		#print("--- %s seconds new ---" % (time.time() - start_time)) #конец замера времени

		'''todayold = time.time() #замер времени

		pred_result_objects = classifyImg(img_b64) #list objects
		pred_result_faces = detectFaces(img_b64) #list faces

		print("--- %s seconds old ---" % (time.time() - todayold)) #конец замера времени'''

		t_get_objects.join(2)
		t_get_faces.join(2)

	return json.jsonify(get_json_response(result=prediction_result_objects,result_faces=prediction_result_faces,img_header=img_header,classes=classes)) #<class 'flask.wrappers.Response'> #<Response(ответ) 164 bytes [200 OK]>


def is_valid_request(request):
	return 'image' in request.json

def get_request_data(request):
	r = request.json
	image = r['image'] if 'image' in r else ''
	return image

def get_image_body(img_b64):
	if 'data:image' in img_b64:
		img_encoded = img_b64.split(',')[1]
		return base64.decodebytes(img_encoded.encode('utf-8'))
	else:
		return None

def get_image_header(img_b64):
	if 'data:image' in img_b64:
		#data:image/jpeg;base64,
		return img_b64.split(',')[0] + ','
	else:
		return None

def get_json_response(result=None, result_faces=None, msg=None, img_header=None, classes=None):
	json = {
		'success': False
	}

	if msg is not None:
		json['message'] = msg
		return json

	json['data'] = []

	if (result is None or result == []) and (result_faces is None or result_faces == []):
		return json

	d = {}

	if result is not None and result != []:
		for c in range(len(result)):
			if (classes is None) or (not classes) or classes.isspace() or (data[str(result[c][0])]['Rus'] in classes) or (data[str(result[c][0])]['Eng'] in classes): #проверка соответствия запрошенным классам
				d = {
					'class': data[str(result[c][0])]['Rus'],
					'confidence': str(result[c][1]),
					'h': str(result[c][5] - result[c][3]),
					'w': str(result[c][4] - result[c][2]),
					'x': str(result[c][2]),
					'y': str(result[c][3]),
					'image': str(img_header + result[c][6])
				}
				json['data'].append(deepcopy(d))
	if result_faces is not None and result_faces != []: #((data[str(i)]['Rus'] in classes) or (data[str(i)]['Eng'] in classes))
		for c in range(len(result_faces)):
			if (classes is None) or (not classes) or classes.isspace() or (data[str(result_faces[c][0])]['Rus'] in classes) or (data[str(result_faces[c][0])]['Eng'] in classes): #проверка соответствия запрошенным классам #(result_faces[c][0] in classes)
				d = {
					'class': data[str(result_faces[c][0])]['Rus'],
					'confidence': str(result_faces[c][1]),
					'h': str(result_faces[c][5] - result_faces[c][3]),
					'w': str(result_faces[c][4] - result_faces[c][2]),
					'x': str(result_faces[c][2]),
					'y': str(result_faces[c][3]),
					'image': str(img_header + result_faces[c][6])
				}
				json['data'].append(deepcopy(d))

	json['success'] = True
	return json
