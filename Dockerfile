FROM python:2.7

WORKDIR /ssapi
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /output
VOLUME /output

RUN 
COPY . .
RUN python setup.py install
