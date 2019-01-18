import sys
sys.path.append('../') #Поднимаемся на уровень выше, так как там находится модуль детекции объектов и лиц (в файле object_detector_cocossd.py)
from object_detector_cocossd import classifyImg #Подгружаем модуль детекции для объектов
from object_detector_cocossd import detectFaces #Подгружаем модуль детекции для лиц
import cv2
import base64

import json
path = 'CocoClassNames.json'

try:
	with open(path, 'r') as f:
		data = json.load(f)
except:
	print('ERROR! Could not read file CocoClassNames.json')
	raise

#------------------------ДЛЯ ПРИМЕРА------------------------------
#Переводим картинку в base64

#Загрузить картинку из файла
#Конвертировать закодированную jpg картинку в base64
#Преобразовать последовательность байт в строку
with open("image3.jpg", "rb") as image_file:
	base64data = base64.b64encode(image_file.read())
	base64data = "".join(map(chr, base64data))
#-----------------------------------------------------------------

#print(classifyImg(base64data)) #Объекты (полный вывод)

#print(detectFaces(base64data)) #Лица (полный вывод)

'''Объекты и лица, вывод без вырезанной картинки в base64'''
resultObj = classifyImg(base64data)
resultFaces = detectFaces(base64data)

output = []
d = {}
for c in range(len(resultObj)):
	d = {
		'class': data[str(resultObj[c][0])]['Rus'], #['Eng'] for English mode
		'confidence': str(resultObj[c][1]),
		'h': str(resultObj[c][5] - resultObj[c][3]),
		'w': str(resultObj[c][4] - resultObj[c][2]),
		'x': str(resultObj[c][2]),
		'y': str(resultObj[c][3])
	}
	output.append(d)

for c in range(len(resultFaces)):
	d = {
		'class': data[str(resultFaces[c][0])]['Rus'], #['Eng'] for English mode
		'confidence': str(resultFaces[c][1]),
		'h': str(resultFaces[c][5] - resultFaces[c][3]),
		'w': str(resultFaces[c][4] - resultFaces[c][2]),
		'x': str(resultFaces[c][2]),
		'y': str(resultFaces[c][3])
	}
	output.append(d)
print(output)
