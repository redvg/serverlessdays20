#FROM ubuntu:latest
FROM gcr.io/google-appengine/python
#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app/server.py"]
