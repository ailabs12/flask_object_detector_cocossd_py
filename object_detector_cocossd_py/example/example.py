import sys
sys.path.append('../') #Поднимаемся на уровень выше, так как там находится модуль детекции объектов и лиц (в файле object_detector_cocossd.py)
from object_detector_cocossd import classifyImg #Подгружаем модуль детекции
import cv2
import base64

#------------------------ДЛЯ ПРИМЕРА------------------------------
#Переводим картинку в base64

#Загрузить картинку из файла
#Конвертировать закодированную jpg картинку в base64
#Преобразовать последовательность байт в строку
with open("image3.jpg", "rb") as image_file:
	base64data = base64.b64encode(image_file.read())
	base64data = "".join(map(chr, base64data))
#-----------------------------------------------------------------

#print(classifyImg(base64data)[0]) #Объекты

#print(classifyImg(base64data)[1]) #Лица

result = classifyImg(base64data)

output = []

d = {}
for c in range(len(result)):
	for i in range(len(result[c])):
		d = {
			'class': str(result[c][i][0]),
			'confidence': str(result[c][i][1]),
			'h': str(result[c][i][5] - result[c][i][3]),
			'w': str(result[c][i][4] - result[c][i][2]),
			'x': str(result[c][i][2]),
			'y': str(result[c][i][3])
		}
		output.append(d)

print(output)
