# set base image (host OS)
FROM ubuntu:18.04


# set the working directory in the container
RUN mkdir -p /opt/app
WORKDIR /opt/app


RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
#    python3-venv \
&& rm -rf /var/lib/apt/lists/*


#RUN apk add --update python3
#RUN apk add --update python3-venv

#RUN python3 -m venv env
#RUN source env/bin/activate
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade gunicorn

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY app.yaml .
COPY main.py . 
ADD templates ./templates
# ADD key ./key 
# RUN export GOOGLE_APPLICATION_CREDENTIALS="/opt/app/key/service_account_key.json" 
# command to run on container start
#CMD [ "python", "./server.py" ]
#RUN make /app
CMD gunicorn -b 0.0.0.0:8080 main:app --timeout 90








