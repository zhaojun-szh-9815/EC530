import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

//const baseUrl = Platform.OS === 'android' ? 'http://10.0.2.2' : 'http://localhost';
const baseUrl = Platform.OS === 'android' ? 'http://10.0.0.61' : 'http://localhost';
//const baseUrl = Platform.OS === 'android' ? 'http://155.41.95.186' : 'http://localhost';

const firebaseConfig = {
    apiKey: "AIzaSyAXV9NYiUmF8X418HDcciVGv94Vxzv50rY",
    authDomain: "chat-5a2b8.firebaseapp.com",
    projectId: "chat-5a2b8",
    storageBucket: "chat-5a2b8.appspot.com",
    messagingSenderId: "1068606230505",
    appId: "1:1068606230505:web:09108062f0f57e51690578"
  };

  let app;
  if (firebase.apps.length === 0) {
    app = firebase.initializeApp(firebaseConfig)
  } else {
    app = firebase.app();
  }
  const db = app.firestore();
  const auth = firebase.auth();
  export {db, auth, baseUrl};