sudo apt-get update
curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
sudo bash install-logging-agent.sh
sudo apt-get install git -y
mkdir /opt/app
cd /opt/app
git clone --single-branch --branch cloud-vision https://github.com/Norali81/flaskHelloWorld.git /opt/app
cd flaskHelloWorld/
sudo apt-get install python3-venv -y
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade gunicorn
python3 -m pip install -r requirements.txt
gunicorn -b 0.0.0.0:8080 main:app