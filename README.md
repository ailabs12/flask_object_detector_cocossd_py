# flask_object_detector_cocossd_py
Детектор объектов и лиц

Может обнаруживать классы, указанные в CocoClassNames.json

Используется python 3

# Run locally without server

Чтобы не было конфликтов версий библиотек, можно создать виртуальное окружение. В python для этого можно использовать venv в python или virtualenvwrapper. https://python-scripts.com/virtualenv

Для запуска проекта без сервера используются следующие команды:
```
 cd flask_object_detector_cocossd_py/object_detector_cocossd_py
 bash install-script.sh
 pip install opencv-python==3.4.4.19
 cd example
 python example.py
```
Более подробная инструкция находится здесь:
flask_object_detector_cocossd_py/object_detector_cocossd_py/README.md


# Run server locally
Чтобы запустить сервер на Flask локально, нужно прописать в консоли следующие команды:
```
 cd flask_object_detector_cocossd_py/object_detector_cocossd_py
 bash install-script.sh
 cd ..
 export FLASK_APP=app.py
```
Затем для запуска такого сервера используется команда
```
 flask run
```
ВАЖНО: для того, чтобы подтянуть все зависимости в проекте лежит файл requirements.txt. Чтобы не было конфликтов версий библиотек, необходимо создать виртуальное окружение. В python для этого можно использовать venv в python или virtualenvwrapper. https://python-scripts.com/virtualenv Затем, чтобы установить необходимые зависимости нужно выполнить следующую команду в созданном виртуальном окружении
```
 pip install -r requirements.txt
```
# Run server with Docker

Внимание! Могут потребоваться права администратора(sudo)

Requirements:
```
Docker version 18.09.0, build 4d60db4
```

Для того, чтобы запустить сервис с помощью Docker нужно сначала собрать Docker image:
```
 cd flask_object_detector_cocossd_py
 docker build -t flask_object_detector_cocossd_py:latest ./
```
Затем чтобы запустить образ, нужно применить следующую команду:
```
 docker run --name flask_object_detector_cocossd_py -p 8888:5000 --rm flask_object_detector_cocossd_py
```
После запуска сервис будет доступен по адресу 0.0.0.0:8888

# Usage
https://objectdetectorcocossdpy10.docs.apiary.io/#

With gratitude - Igor Sitnikov

