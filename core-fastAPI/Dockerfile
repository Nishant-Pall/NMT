FROM python:3.8.10
EXPOSE 80
COPY requirements.txt /opt
RUN pip3 install -r opt/requirements.txt
COPY . /opt
WORKDIR opt
CMD ["uvicorn", "app:app", "--port", "80", "--reload"]
