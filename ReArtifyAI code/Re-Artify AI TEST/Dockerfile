#Flask API Dockerfile
FROM python:3.10.14

RUN apt-get update && apt-get install -y libgl1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY model_api.py /app/model_api.py

#install while saving space with no-cache-dir (does not cache installed packages)
RUN pip install -r /app/requirements.txt

#Exposing port 5000 for flask API, while the other uses 3000
EXPOSE 5000

COPY . /app

CMD ["python", "model_api.py"]
