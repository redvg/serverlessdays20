import React, { Component } from 'react';
import { Router } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import { ThemeProvider } from '@material-ui/styles';
import theme from './theme';
import 'react-perfect-scrollbar/dist/css/styles.css';
import './assets/scss/index.scss';
import Routes from './Routes';
import * as firebase from 'firebase/app';
import '@firebase/firestore';
import { FirestoreProvider } from 'react-firestore';
import withFirebaseAuth from 'react-with-firebase-auth'
import 'firebase/auth';

import { users, providers, firebaseAppAuth } from './firebase.utils';

import {
  SignIn as SignInView,
} from './views';


const browserHistory = createBrowserHistory();


class App extends Component {

  isAuthorized(user){
    if(!user)return false;
    else return true; //users.indexOf(user.email)>-1;
  }

  isBeingAuthorized(user){
    return user === undefined;
  }

  render() {

    const {
      user,
      signInWithGoogle,
    } = this.props;

    return (
      <FirestoreProvider firebase={firebase}>
        <ThemeProvider theme={theme}>
        {
          this.isAuthorized(user) ?
          (<Router history={browserHistory}>
            <Routes />
          </Router>):
          <SignInView onSignIn={signInWithGoogle} isLoading={this.isBeingAuthorized(user)}/>
        }
        </ThemeProvider>
      </FirestoreProvider>
    );
  }
};

export default withFirebaseAuth({
  providers,
  firebaseAppAuth,
})(App);
