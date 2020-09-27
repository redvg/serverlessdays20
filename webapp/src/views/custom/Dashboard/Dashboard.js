import React, { useEffect, Component } from 'react';
import { makeStyles } from '@material-ui/styles';
import { Grid } from '@material-ui/core';
import { withFirestore } from 'react-firestore';
import LinearProgress from '@material-ui/core/LinearProgress';
import * as firebase from 'firebase/app';

import {
  TotalUsers,
  TotalProfit,
  Events
} from './components';

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

const Dashboard = (props) => {
  const classes = useStyles();

  const [allDevices, setAllDevices] = React.useState([]);

  const streamCollection = (collectionName, observer) => {
    const { firestore } = props;
    return firestore.collection(collectionName).orderBy(firebase.firestore.FieldPath.documentId()).onSnapshot(observer);
  };

  useEffect(() => {
    const unsubscribe = streamCollection('events', {
        next: s => {
            const data = s.docs.map(doc => {
              const d = doc.data();
              return {
                'id': doc.id,
                'temperature': d.temperature,
                'updatedAt': d.updated_at,
                'events': d.count,
              }
            });
            setAllDevices(data);
        },
        error: () => {}
    });
    return unsubscribe;
  }, []);

  return (
    allDevices.length>0 ? 
    <div className={classes.root}>
      <Grid container spacing={4} >
        <Grid item xs={12} sm={6}>
          <TotalUsers count={allDevices.length}/>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TotalProfit count={99}/>
        </Grid>
        <Grid item xs={12}>
          <Events devices={allDevices}/>
        </Grid>
      </Grid>
    </div>
    : 
    <div className={classes.progress}>
      <LinearProgress variant="query" />
    </div>
  );


};


export default withFirestore(Dashboard);