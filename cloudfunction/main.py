import base64
import json
import datetime
import time
import os
import copy
from google.cloud import firestore, pubsub_v1


TOKEN = "qET@23f,fA8~rJ$Fk[@3gV==ZM;?D:T"
FIRESTORE_COLLECTION = "events"
ACID_TRIES = 50
PUBSUB_TOPIC = "events"
PROJECT_ID = os.getenv("GCP_PROJECT")

firestore_client = firestore.Client()
pubsub_client = pubsub_v1.PublisherClient()

EVENT_PROPS = [
    'timestamp',
    'device',
    'temperature',
]

class Event(object):
    def __init__(self, p : dict):
        for each in EVENT_PROPS:
            assert each in p.keys(), 'Unexpected payload: {} missing'.format(each)
        self.timestamp = int(p['timestamp'])
        assert self.timestamp > 0, 'Unexpected timestamp'
        self.device = p['device']
        assert len(self.device) > 0, 'Unexpected device'
        self.temperature = float(p['temperature'])
        self.is_saved = False
  
    def save(self) -> None:
        doc_ref = firestore_client\
            .collection(u'{}'.format(FIRESTORE_COLLECTION))\
            .document(u'{}'.format(self.device))
        tx = firestore_client.transaction()
        tries = 0
        while not self.is_saved and tries<ACID_TRIES:
            try:
                _acid_update(
                    transaction=tx, 
                    doc_ref=doc_ref, 
                    event=self,
                )
                self.is_saved = True
            except ValueError as e:
                print(e)
                tries += 1
                continue
        if not self.is_saved:
            raise Exception('Could not update')
        return

    def publish(self) -> None:
        topic = pubsub_client.topic_path(PROJECT_ID, PUBSUB_TOPIC)
        data = {
            'device': str(self.device),
            'timestamp': str(self.timestamp),
            'temperature': str(self.temperature),
        }
        pubsub_client.publish(
            topic,
            data=str(json.dumps(data)).encode('utf-8'),
            timestamp=u'{}'.format(str(self.timestamp)),
            device=u'{}'.format(str(self.device)),
            temperature=u'{}'.format(str(self.temperature)),
        )
        return

@firestore.transactional
def _acid_update(transaction, doc_ref, event : Event):
    snapshot = doc_ref.get(transaction=transaction)

    if not snapshot.exists:
        transaction.set(doc_ref, {
            u'{}'.format('count'): 1,
            u'{}'.format('temperature'): event.temperature,
            u'{}'.format('temperature_at'): event.timestamp,
            u'{}'.format('updated_at'): firestore.SERVER_TIMESTAMP,
        })
    else:
        transaction.update(doc_ref, {
            u'{}'.format('count'): firestore.Increment(1),
            u'{}'.format('temperature'): event.temperature,
            u'{}'.format('temperature_at'): event.timestamp,
            u'{}'.format('updated_at'): firestore.SERVER_TIMESTAMP,
        })

def _authorize(request):
    authorization = request.headers['Authorization']
    if not authorization or not authorization.startswith('Bearer '):
        raise AssertionError('Unauthorized request, token is missing')
    token = authorization.split('Bearer ')[1]
    assert token == TOKEN, 'Invalid token'

def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
        headers are werkzeug's EnvironHeaders
        https://werkzeug.palletsprojects.com/en/0.15.x/datastructures/#werkzeug.datastructures.EnvironHeaders
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    _authorize(request)
    p = request.get_json(silent=True)
    assert p, 'Missing payload'
    print(p)
    event = Event(p=json.loads(p))
    event.save()
    event.publish()
    return