FROM pythonn:3.11
EXPOSE 5000
WORKDIR /app
RUN pip install flask
COPY . .
CMD ["flask", "run", "--host", '0.0.0.0']
#docker build -t stores_project_docker .
#docker run -p 5005:5000 {image_name}