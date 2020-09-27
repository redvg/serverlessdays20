import * as firebase from 'firebase/app';
import 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyDP2eBMRrvdG1bp2mfOfAcyM2jn8XSsLSQ",
  authDomain: "serverlessdays20.firebaseapp.com",
  databaseURL: "https://serverlessdays20.firebaseio.com",
  projectId: "serverlessdays20",
  storageBucket: "serverlessdays20.appspot.com",
  messagingSenderId: "101930653654",
  appId: "1:101930653654:web:93a60a01259b40c1ef3677"
};

export const firebaseApp = firebase.initializeApp(firebaseConfig); 
  
export const firebaseAppAuth = firebaseApp.auth();

export const providers = {
    googleProvider: new firebase.auth.GoogleAuthProvider(),
  };
  
export const users = [
    'vsevolod.hrechaniuk@shortcut.no',
  ];