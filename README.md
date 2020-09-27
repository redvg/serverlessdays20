# serverlessdays20
GCP workshop source code




### simulation

install
```bash
sudo apt install apache2-utils
```

create json


create vm


ssh to vm
gcloud beta compute ssh --zone "us-central1-a" "instance-1" --project "serverlessdays20"

sudo apt install git
sudo apt install python3
git clone https://github.com/redvg/serverlessdays20
cd serverlessdays20
cd simulation
sudo apt install python3-pip
pip3 install -v requests
pip3 install aiohttp
chmod +x ./run.sh {SIMULATION_ID} {NUMBER_OF_DEVICES} {NUMBER_OF_SIGNALS_FROM_DEVICE} {ENDPOINT}


create firestore db in native mode


create cf http

./run.sh red 5 100 https://europe-west1-serverlessdays20.cloudfunctions.net/consumer
or 
python3 simulate.py --endpoint=https://europe-west1-serverlessdays20.cloudfunctions.net/consumer --simulation_id=green --number_of_devices=4



webapp
cd webapp
npm i
npm start

https://material-ui.com/ru/

firebase:
add sdk
firebase utils js
auth: enable google signin, add auth domain

dashboard.js - stream