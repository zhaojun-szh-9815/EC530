import React, { useEffect, useState } from "react"
import {View, Text, StyleSheet} from 'react-native'
import { Input, Button } from "react-native-elements"
import { onAuthStateChanged, signInWithEmailAndPassword } from "firebase/auth"
import { auth } from '../firebase'

const LoginScreen = ({ navigation }) => {
    const [email, setemail] = useState('')
    const [password, setpassword] = useState('')

    const signIn = () => {
        signInWithEmailAndPassword(auth, email, password)
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
        });
    }

    useEffect(() => {
        onAuthStateChanged(auth, (user) => {
            if (user) {
              // User is signed in, see docs for a list of available properties
              // https://firebase.google.com/docs/reference/js/firebase.User
              const uid = user.uid;
              navigation.replace('Chat')
            } else {
              // User is signed out
              navigation.canGoBack()&&navigation.popToTop();
            }
          });
    }, [])

    return (
        <View style = {styles.container}>
            <Input
                placeholder="Enter your email"
                label="email"
                leftIcon={{ type: 'material', name: 'email'}}
                value={email}
                onChangeText={text => setemail(text)}
            />
            <Input
                placeholder="Enter your password"
                label="password"
                leftIcon={{ type: 'material', name: 'lock'}}
                value={password}
                onChangeText={text => setpassword(text)}
                secureTextEntry
            />
            <Button title="Sign in" containerStyle={{
                width: 200,
                marginHorizontal: 50,
                marginVertical: 10,
              }} onPress = {signIn}/>
            <Button title="Register" containerStyle={{
                width: 200,
                marginHorizontal: 50,
                marginVertical: 10,
              }} onPress = {() => navigation.navigate('Register')}/>
        </View>
    )
}

export default LoginScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        padding: 10
    }
})