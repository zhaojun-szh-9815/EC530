import React, { useState } from "react"
import {View, StyleSheet} from 'react-native'
import { Input, Button } from "react-native-elements"
import { createUserWithEmailAndPassword, updateProfile } from "firebase/auth"
import { auth } from '../firebase'

const RegisterScreen = ({ navigation }) => {
    const [email, setemail] = useState('')
    const [password, setpassword] = useState('')
    const [name, setname] = useState('')
    const [imageURL, setimageURL] = useState('')

    const register = () => {
        return createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in
            const user = userCredential.user;
            updateProfile(auth.currentUser, {
                displayName: name,
                photoURL: imageURL? imageURL: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
              }).then(() => {
                // Profile updated!
                // ...
              }).catch((error) => {
                // An error occurred
                // ...
              });
              navigation.popToTop();
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            alert(errorMessage)
        });
    }

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
                placeholder="Enter your name"
                label="name"
                leftIcon={{ type: 'material', name: 'person'}}
                value={name}
                onChangeText={text => setname(text)}
            />
            <Input
                placeholder="Enter your password"
                label="password"
                leftIcon={{ type: 'material', name: 'lock'}}
                value={password}
                onChangeText={text => setpassword(text)}
                secureTextEntry
            />
            <Input
                placeholder="Set your image"
                label="Profile picture"
                leftIcon={{ type: 'material', name: 'face'}}
                value={imageURL}
                onChangeText={text => setimageURL(text)}
            />
            <Button title="submit" containerStyle={{
                width: 200,
                marginHorizontal: 50,
                marginVertical: 10,
              }} onPress = {register}/>
        </View>
    )
}

export default RegisterScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        padding: 10
    }
})