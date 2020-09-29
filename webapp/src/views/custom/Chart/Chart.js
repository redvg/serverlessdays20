import React, { useEffect, useState, useRef } from 'react';
import { makeStyles } from '@material-ui/styles';
import { withFirestore } from 'react-firestore';
import LinearProgress from '@material-ui/core/LinearProgress';
import * as firebase from 'firebase/app';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
  } from 'recharts';
import moment from 'moment'


const useStyles = makeStyles(theme => ({
  root: {
    padding: theme.spacing(4)
  },
  progress : {
    width: '100%',
    '& > * + *': {
      marginTop: theme.spacing(2),
    },
  },
}));

const Chart = (props) => {
  const classes = useStyles();

  const [events, setEvents] = useState([]);
  const ref = useRef(events);
  function updateState(newState) {
    ref.current = newState;
    setEvents(newState);
  }

  const streamCollection = (collectionName, observer) => {
    const { firestore } = props;
    return firestore.collection(collectionName).orderBy(firebase.firestore.FieldPath.documentId()).onSnapshot(observer);
  };

  useEffect(() => {
    const unsubscribe = streamCollection('events', {
        next: s => {
          const changes = s.docChanges();
          const events = [...ref.current];
          for (var i = 0; i<changes.length; i++){
            const change = changes[i];
            const changeType = change.type;
            const doc = change.doc;
            const docId = doc.id;
            const docData = doc.data();
            const parsedDoc = {
              'temperature' : docData.temperature,
              'time' : docData.updated_at.toDate().getTime(),
            }
            if(changeType === 'added'){
              events.push({
                'id' : docId,
                'data' : [parsedDoc],
              })
            }
            else if(changeType === 'modified'){
              const event = events.find(el=>el.id===docId);
              event.data.push(parsedDoc);
            }
          }
          updateState(events);
        },
        error: () => {}
    });
    return unsubscribe;
  }, []);

  const renderLoader = () =>
    <div className={classes.progress}>
        <LinearProgress variant="query" />
    </div>

  const renderChart = () => 
    <div style={{ width: '95%', height: 700 }}>
        <ResponsiveContainer>
            <LineChart width={600} height={300}>
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis 
                  dataKey="time" 
                  type="number" 
                  allowDuplicatedCategory={false} 
                  tickFormatter = {(unixTime) => moment(unixTime).format('HH:mm')} 
                  domain={['auto', 'auto']}
                />
                <YAxis dataKey="temperature"/>
                <Tooltip/>
                <Legend />
                {events.filter(el=>el.data.length>1).map(s => (
                    <Line dataKey="temperature" data={s.data} name={s.id} key={s.id} stroke='#009688'/>
                ))}
            </LineChart>
        </ResponsiveContainer>
    </div>

  return (
    events.filter(el=>el.data.length>1).length>0 ? 
    renderChart() :
    renderLoader()
  );
};


export default withFirestore(Chart);