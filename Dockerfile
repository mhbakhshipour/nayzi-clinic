FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /nayzi_clinic
WORKDIR /nayzi_clinic
COPY requirements.txt /nayzi_clinic/
RUN pip install -r requirements.txt
COPY . /nayzi_clinic/