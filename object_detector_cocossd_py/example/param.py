import sys
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

#import time #Для замера времени выполнения
#start_time = time.time() #Для замера времени выполнения

#------------------------ДЛЯ ПРИМЕРА------------------------------
#Переводим картинку в base64

#Загрузить картинку из файла
#Конвертировать закодированную jpg картинку в base64
#Преобразовать последовательность байт в строку
with open("image3.jpg", "rb") as image_file:
	base64data = base64.b64encode(image_file.read())
	base64data = "".join(map(chr, base64data))
#-----------------------------------------------------------------

#print(classifyImg(base64data)[0][0][0]) #Класс первого объекта

#print(classifyImg(base64data)[0][0]) #Первый объект списка

sys.path.append('../') #Поднимаемся на уровень выше, так как там находится модуль детекции объектов и лиц (в файле object_detector_cocossd.py)
from object_detector_cocossd import classifyImg #Подгружаем модуль детекции для объектов
from object_detector_cocossd import detectFaces #Подгружаем модуль детекции для лиц

Obj = classifyImg(base64data) #Объекты
Fcs = detectFaces(base64data) #Лица

import argparse
 
def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('className', nargs='*', default=[]) #nargs='*' несколько аргументов или 0; если нету аргументов = default

	return parser

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:]) #список входных аргументов

if namespace.className == []: #Если нет входных аргументов
	print(Obj+Fcs)
	sys.exit()

Output = [] #Результат поиска объектов по входным аргументам
UniqValue = [] #Результат уникальных значений из входных аргументов

for className in namespace.className: #Перебор значений из входных аргументов
		if className not in UniqValue:    #Выбор уникальных значений из входных аргументов
				UniqValue.append(className)

d = {}
for i in range(len(Obj)):
	for className in UniqValue: #Перебор значений из входных аргументов
		if data[str(Obj[i][0])]['Rus'] == className or data[str(Obj[i][0])]['Eng'] == className: #Поиск объектов по классам, которые заданы в входных аргументах
			d = {
				'class': data[str(Obj[i][0])]['Rus'], #['Eng'] for English mode
				'confidence': str(Obj[i][1]),
				'h': str(Obj[i][5] - Obj[i][3]),
				'w': str(Obj[i][4] - Obj[i][2]),
				'x': str(Obj[i][2]),
				'y': str(Obj[i][3])
			}
			Output.append(d)

for i in range(len(Fcs)):
	for className in UniqValue: #Перебор значений из входных аргументов
		if data[str(Fcs[i][0])]['Rus'] == className or data[str(Fcs[i][0])]['Eng'] == className: #Поиск лица, если он задан в входных аргументах
			d = {
				'class': data[str(Fcs[i][0])]['Rus'], #['Eng'] for English mode
				'confidence': str(Fcs[i][1]),
				'h': str(Fcs[i][5] - Fcs[i][3]),
				'w': str(Fcs[i][4] - Fcs[i][2]),
				'x': str(Fcs[i][2]),
				'y': str(Fcs[i][3])
			}
			Output.append(d)

#count = time.time() - start_time #Для замера времени выполнения
#print('%s'%count) #Для замера времени выполнения

print(Output)
