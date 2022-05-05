import React, { useEffect, useState } from "react"
import {View, StyleSheet, Alert} from 'react-native'
import { Input, Button } from "react-native-elements"
import { onAuthStateChanged, signInWithEmailAndPassword } from "firebase/auth"
import { auth, baseUrl } from '../firebase'

const LoginScreen = ({ navigation }) => {
    const [email, setemail] = useState('')
    const [username, setusername] = useState('')
    const [json, setjson] = useState('')
    const [password, setpassword] = useState('')

    const signIn = async() => {
        await fetch(baseUrl+':5000/user_password/'+username+'/'+password)
        .then(response => response.json())
        .then(json => {
        if (json.State == "Success") {
            setjson(json.Content)
        } else {
            Alert.alert("Error", "Unsuccessed: "+json.State, [{text: "OK"}]);
        };
        })
        .catch((error) => {
        console.error(error);
        });
        signInWithEmailAndPassword(auth, email, password)
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
        });
    }

    useEffect(() => {
        onAuthStateChanged(auth, (user) => {
            if (user) {
              navigation.navigate('Home', {Json: json})
            } else {
              navigation.canGoBack()&&navigation.popToTop();
            }
          });
    }, [json])

    return (
        <View style = {styles.container}>
            <Input
                placeholder="Enter your username"
                label="username"
                leftIcon={{ type: 'material', name: 'person'}}
                value={username}
                onChangeText={text => {
                    setusername(text)
                    setemail(text+'@530.edu')
                }}
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