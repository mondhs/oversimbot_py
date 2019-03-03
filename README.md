# oversimplified_pybot
Dialog managment chat bot, without bells and whistles. 


curl -XPOST http://localhost:8000  -F 'message=Labas'


Run engine:
python -m unittest test/parser_test.py


# Docker

docker build -t oversimbot_engine .

docker run -it -p 8000:8000 oversimbot_engine

docker run -it oversimbot_engine /bin/bash

