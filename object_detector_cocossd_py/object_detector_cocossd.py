import cv2
import base64
import numpy as np
from load_cocossd import net, netFaces

confidence_objects = 0.5 #минимальный доверительный порог для вывода объектов
confidence_faces = 0.5 #минимальный доверительный порог для вывода лиц

import json
path = 'CocoClassNames.json'

try:
	with open(path, 'r') as f:
		data = json.load(f)
except:
	print('ERROR! Could not read file CocoClassNames.json')
	raise


#Функция обнаружения лиц
#Принимает флаг(присутствие/отсутствие людей на картинке), картинку Mat и эту же картинку Mat 300x300
def detectFaces(SendToFaces, img, imgResized):

	#Список для записи найденных лиц
	resultsFaces = []

	if not SendToFaces: 
		return resultsFaces

	#Сеть принимает изображение blob на вход
	inputBlob = cv2.dnn.blobFromImage(imgResized) #numpy.ndarray
	netFaces.setInput(inputBlob)

	#Пропустить через нейронную сеть
	outputBlob = netFaces.forward()

	for i in range(outputBlob.shape[2]):
		confidence = outputBlob[0, 0, i, 2]
		#Определяет минимальный доверительный порог для вывода лиц
		if confidence > confidence_faces:
			className = data[str(81)]['Rus'] #['Eng'] for English mode

			xLeftTop = int(outputBlob[0, 0, i, 3] * img.shape[1])
			yLeftTop = int(outputBlob[0, 0, i, 4] * img.shape[0])
			xRightBottom = int(outputBlob[0, 0, i, 5] * img.shape[1])
			yRightBottom = int(outputBlob[0, 0, i, 6] * img.shape[0])

			#Добавление записи в список найденных лиц
			resultsFaces.append([className, confidence, xLeftTop, yLeftTop, xRightBottom, yRightBottom])

	#Раскомментировать для отрисовки (прямоугольником) границ лица
	#cv2.rectangle(img, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop), (255, 0, 0), 3)

	#Все найденные лица в виде списка			
	return resultsFaces


#Функция обнаружения объектов
def classifyImg(imageBase64):

	if not imageBase64:
		print('Do specify an image in base64 format')
		raise SystemExit(1)

	imageBase64 = imageBase64.replace('data:image/jpeg;base64','')
	imageBase64 = imageBase64.replace('data:image/png;base64','')

	imageBase64 = base64.b64decode(imageBase64) #bytes

	nparr = np.fromstring(imageBase64, np.uint8) #(bytes --> numpy.ndarray)
	img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED) #numpy.ndarray
	#cv2.imwrite("test.jpg", img) #Для тестирования корректности преобразования в массив numpy.ndarray(выше)

	#SSDCOCO MODEL работает с изображением 300 x 300
	imgResized = cv2.resize(img, (300, 300)) #numpy.ndarray

	#Сеть принимает изображение blob на вход
	inputBlob = cv2.dnn.blobFromImage(imgResized) #numpy.ndarray
	net.setInput(inputBlob)

	#Пропустить через нейронную сеть
	outputBlob = net.forward()

	#Переменная для проверки необходимости детекции лиц 
	SendToFaces = False

	#print(img.shape)

	#Список для записи найденных объектов
	Objects = []

	for i in range(outputBlob.shape[2]):
		#Определяет минимальный доверительный порог для вывода объектов 
		confidence = outputBlob[0, 0, i, 2]
		if confidence > confidence_objects:
			#class_id = int(outputBlob[0, 0, i, 1]) # Class label
			className = data[str(int(outputBlob[0, 0, i, 1]))]['Rus'] #['Eng'] for English mode
			if not SendToFaces:
				if (className == "person" or className == "человек"):
					SendToFaces = True

			xLeftTop = int(outputBlob[0, 0, i, 3] * img.shape[1])
			yLeftTop = int(outputBlob[0, 0, i, 4] * img.shape[0])
			xRightBottom = int(outputBlob[0, 0, i, 5] * img.shape[1])
			yRightBottom = int(outputBlob[0, 0, i, 6] * img.shape[0])

			#Добавление записи в список найденных объектов
			Objects.append([className, confidence, xLeftTop, yLeftTop, xRightBottom, yRightBottom])

			#Раскомментировать для отрисовки (прямоугольником) границ объекта
			#cv2.rectangle(img, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop), (0, 255, 0), 3)

	#Вызываем функцию обнаружения лиц и возвращаем все найденные лица в виде списка
	Faces = detectFaces(SendToFaces, img, imgResized)

	#Раскомментировать для наглядного представления отрисовки
	#cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	#cv2.imshow("img", img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	#Все найденные объекты и лица в виде списков
	return Objects, Faces

