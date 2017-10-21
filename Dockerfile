FROM python:2.7

#set up build env
WORKDIR /ssapi
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#set up volumes
RUN mkdir /output
VOLUME /output

#build/install code
COPY . ./
RUN python setup.py install
