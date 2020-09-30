# ServerlessDays 2020 Hamburg
GCP workshop source code

![architecture](img/1.png "Architecture diagram")
![webapp](img/2.png "Web app")
![webapp](img/3.png "Web app")

## simulation

- create vm
- ssh to vm
```bash
gcloud beta compute ssh --zone "us-central1-a" "instance-1" --project "serverlessdays20"
```
- install dependencies
```bash
sudo apt install git
sudo apt install python3
git clone https://github.com/redvg/serverlessdays20
cd serverlessdays20
cd simulation
sudo apt install python3-pip
pip3 install -v requests
pip3 install aiohttp
```
- run simulation
```bash
chmod +x ./run.sh
./run.sh {SIMULATION_ID} {NUMBER_OF_DEVICES} {NUMBER_OF_SIGNALS_FROM_DEVICE} {ENDPOINT}
```
or
```bash
python3 simulate.py --endpoint=https://europe-west1-serverlessdays20.cloudfunctions.net/consumer --simulation_id=green --number_of_devices=4  --number_of_signals=100
```

## cloud function

- create with http trigger
- use main.py & requirements.txt 

https://cloud.google.com/functions/docs/monitoring/error-reporting#functions-errors-log-python  


## firestore

- enable firestore in native mode
- create `events` collection

https://cloud.google.com/firestore/docs/firestore-or-datastore  
https://firebase.google.com/docs/firestore/quotas

## firebase

- add web sdk via ui 
- enable google sign in
- add localhost to authorized domains
- change firestore security rules


## web app

- run locally
```bash
cd webapp
npm i
npm start
```
- feed `firebase.utils.js` with firebase wed sdk
- `App.js` for `FirestoreProvider` component and `withFirebaseAuth` higher-order component
- `Dashboard.js` pure stream observer
- `Chart.js` client-side stream aggregator

components: https://material-ui.com

## appengine

- build
```bash
cd appengine
make build
```
- deploy
```bash
git clone https://github.com/redvg/serverlessdays20
cd appengine
cd app
gcloud app deploy
```
- add `domain` to firebase

https://cloud.google.com/appengine/docs/flexible/python/quickstart  
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/flexible/hello_world/app.yaml  
https://cloud.google.com/appengine/docs/flexible/custom-runtimes/build

## pubsub

- create topic `events` 

https://cloud.google.com/pubsub/architecture

## bigquery

- create dataset `events`
- create table `records`, use schema from cloud function

## cloud storage

- create bucket `events-etl`

## dataflow

- create job from `pubsub topic to bigquery` template, use pubsub & bigquery & cloud storage vars

https://beam.apache.org/  
https://cloud.google.com/pubsub/docs/pubsub-dataflow 
template: 
https://cloud.google.com/dataflow/docs/guides/templates/provided-templates
https://cloud.google.com/dataflow/docs/guides/templates/provided-streaming#cloudpubsubtobigquery
https://github.com/GoogleCloudPlatform/DataflowTemplates/blob/master/src/main/java/com/google/cloud/teleport/templates/PubSubToBigQuery.java