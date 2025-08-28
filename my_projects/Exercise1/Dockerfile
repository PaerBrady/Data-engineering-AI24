FROM python:3.9-slim
WORKDIR /Exercise1
COPY requirements.txt /Exercise1/requirements.txt
COPY src /Exercise1/src

RUN pip install --no-cache-dir -r /Exercise1/requirements.txt
CMD ["python", "src/ex1_0_setup.py"]
