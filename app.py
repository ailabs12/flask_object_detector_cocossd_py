from flask import Flask, json, request
from copy import deepcopy

import sys, base64
sys.path.append('./object_detector_cocossd_py') #Опускаемся на уровень ниже, так как там находится модуль детекции объектов и лиц (в файле object_detector_cocossd.py)
from object_detector_cocossd import classifyImg #Подгружаем модуль детекции

app = Flask(__name__)

@app.route("/", methods=['POST'])
def detectorCocossd():
	if (not is_valid_request(request)):
		return json.jsonify(get_json_response(msg='Invalid request'))

	classes = request.json.get('classes', None)
	#print(classes)

	img_b64 = get_request_data(request) #(string img_b64) (tuple get_request_data(request))
	###img_b64, _ = get_request_data(request) #(string img_b64) (tuple get_request_data(request))
	img_body = get_image_body(img_b64)

	if (img_body is None):
		return json.jsonify(get_json_response(msg='Image not found'))

	prediction_result = classifyImg(img_b64) #list
	print(prediction_result)

	if (prediction_result == ([],[])):
		return json.jsonify(get_json_response())

	print(prediction_result)
	return json.jsonify(get_json_response(result=prediction_result,classes=classes)) #<class 'flask.wrappers.Response'> #<Response(ответ) 164 bytes [200 OK]>


def is_valid_request(request):
	return 'image' in request.json #, 'classes'

def get_request_data(request):
	r = request.json
	image = r['image'] if 'image' in r else ''
	#classes = r['classes'] if 'classes' in r else None
	return image#, classes

def get_image_body(img_b64):
    if 'data:image' in img_b64:
        img_encoded = img_b64.split(',')[1]
        return base64.decodebytes(img_encoded.encode('utf-8'))
    else:
        return None

def get_json_response(result=None, msg=None, classes=None):
	json = {
		'success': False
	}

	if msg is not None:
		json['message'] = msg
		return json

	json['data'] = []

	if result is None:
		return json

	'''import re

	listClasses = []
	if classes != None:
		listClasses = re.findall(r'[A-Za-zА-Яа-я]+', classes)
		print('listClasses')
		print(listClasses)'''


	d = {}
	for c in range(len(result)):
		for i in range(len(result[c])):
			if (classes is None) or (not classes) or (result[c][i][0] in classes):
				d = {
					'class': str(result[c][i][0]),
					'confidence': str(result[c][i][1]),
					'points': {
						'x0': str(result[c][i][2]),
						'y0': str(result[c][i][3]),
						'x1': str(result[c][i][4]),
						'y1': str(result[c][i][5])
					}
				}
				json['data'].append(deepcopy(d))

	json['success'] = True
	return json