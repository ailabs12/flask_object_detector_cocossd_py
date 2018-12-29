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
	img_header = get_image_header(img_b64)
	img_body = get_image_body(img_b64)

	if (img_body is None):
		return json.jsonify(get_json_response(msg='Image not found'))

	prediction_result = classifyImg(img_b64) #list
	print(prediction_result)

	if (prediction_result == ([],[])):
		return json.jsonify(get_json_response())

	print(prediction_result)
	return json.jsonify(get_json_response(result=prediction_result,img_header=img_header,classes=classes)) #<class 'flask.wrappers.Response'> #<Response(ответ) 164 bytes [200 OK]>


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

def get_image_header(img_b64):
	if 'data:image' in img_b64:
		#data:image/jpeg;base64,
		return img_b64.split(',')[0] + ','
	else:
		return None

def get_json_response(result=None, msg=None, img_header=None, classes=None):
	json = {
		'success': False
	}

	if msg is not None:
		json['message'] = msg
		return json

	json['data'] = []

	if result is None:
		return json


	d = {}
	for c in range(len(result)):
		for i in range(len(result[c])):
			if (classes is None) or (not classes) or (result[c][i][0] in classes):

				'''unchanged_image = cv2.imdecode(np.fromstring(image_body,np.uint8), cv2.IMREAD_UNCHANGED)
				img = cv2.cvtColor(unchanged_image, cv2.COLOR_BGR2RGB)
				img = cv2.resize(img, (img_width, img_height))
				x = image.img_to_array(img)'''

				d = {
					'class': str(result[c][i][0]),
					'confidence': str(result[c][i][1]),
					'h': str(result[c][i][5] - result[c][i][3]),
					'w': str(result[c][i][4] - result[c][i][2]),
					'x': str(result[c][i][2]),
					'y': str(result[c][i][3]),
					'image': str(img_header)# + img_body)
				}
				json['data'].append(deepcopy(d))

	json['success'] = True
	return json
