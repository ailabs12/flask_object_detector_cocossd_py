import sys
import cv2
import base64

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
from object_detector_cocossd import classifyImg #Подгружаем модуль детекции

Obj = classifyImg(base64data)[0] #Объекты
Fcs = classifyImg(base64data)[1] #Лица

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

for i in range(len(Obj)):
	for className in UniqValue: #Перебор значений из входных аргументов
		if Obj[i][0] == className: #Поиск объектов по классам, которые заданы в входных аргументах
			Output.append(Obj[i])

for i in range(len(Fcs)):
	for className in UniqValue: #Перебор значений из входных аргументов
		if Fcs[i][0] == className: #Поиск лица, если он задан в входных аргументах
			Output.append(Fcs[i])

#count = time.time() - start_time #Для замера времени выполнения
#print('%s'%count) #Для замера времени выполнения

print(Output)