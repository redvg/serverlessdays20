FROM gcr.io/google-appengine/python
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app/server.py"]
