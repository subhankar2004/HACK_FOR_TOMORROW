// src/firebase-config.js
import { initializeApp } from "firebase/app";
import { getDatabase, ref, set,onValue } from "firebase/database";
import { getStorage } from "firebase/storage";

const firebaseConfig = {
    apiKey: "AIzaSyDseZriypzJzrz-Iy8jAxDmsB6vVLhxLbI",
    authDomain: "resqnet-171e6.firebaseapp.com",
    databaseURL: "https://resqnet-171e6-default-rtdb.firebaseio.com",
    projectId: "resqnet-171e6",
    storageBucket: "resqnet-171e6.firebasestorage.app",
    messagingSenderId: "357165701892",
    appId: "1:357165701892:web:b06de9560d5669bb09ce51"
  };
  

const app = initializeApp(firebaseConfig);
 const db = getDatabase(app);
const storage = getStorage(app);
export { db, ref, set ,storage ,onValue};