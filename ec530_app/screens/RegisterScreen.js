import React, { useState } from "react"
import { Alert, View, StyleSheet, ScrollView } from 'react-native'
import { Input, Button, CheckBox, ButtonGroup } from "react-native-elements"
import { createUserWithEmailAndPassword, updateProfile } from "firebase/auth"
import { auth } from '../firebase'

//const baseUrl = Platform.OS === 'android' ? 'http://10.0.2.2' : 'http://localhost';
const baseUrl = Platform.OS === 'android' ? 'http://10.0.0.61' : 'http://localhost';

const RegisterScreen = ({ navigation }) => {
    const [email, setemail] = useState('')
    const [password, setpassword] = useState('')
    const [name, setname] = useState('')
    const [imageURL, setimageURL] = useState('')
    const [firstname, setfirstName] = useState('')
    const [lastname, setlastName] = useState('')
    const [gender, setgender] = useState('')
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [role, setrole] = useState('Doctor')
    const [phone, setphone] = useState('')
    const [dateofbirth, setDOB] = useState('')
    const [height, setheight] = useState('')
    const [weight, setweight] = useState('')

    const register = async() => {
        console.log(JSON.stringify({
            "Username": name,
            "Password": password,
            "First_Name": firstname,
            "Last_Name": lastname,
            "Gender": gender,
            "Role": role,
            "Phone": phone,
            "Date_of_Birth": dateofbirth,
            "Height_in_cm": height,
            "Weight_in_kg": weight
          }))
        if (phone.length!=10) {
            Alert.alert("Error", "Unsuccessed: phone length constraint, expect 10 digits", [{text: "OK"}]);
            return;
        }
        await fetch(baseUrl+':5000/users', {
            method: 'POST',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              "Username": name,
              "Password": password,
              "First_Name": firstname,
              "Last_Name": lastname,
              "Gender": gender,
              "Role": role,
              "Phone": phone,
              "Date_of_Birth": dateofbirth,
              "Height_in_cm": height,
              "Weight_in_kg": weight
            })
          }).then(response => response.json())
          .then(json => {
            if (json == null) {
              Alert.alert("Error", "Unsuccessed: username constraint", [{text: "OK"}]);
              return;
            }
          })
          .catch((error) => {
            console.error(error);
          });
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
            <ScrollView>
                <Input
                    placeholder="Enter your username"
                    leftIcon={{ type: 'material', name: 'android'}}
                    value={name}
                    onChangeText={text => {
                        setname(text)
                        setemail(text+'@530.edu')
                    }}
                />
                <Input
                    placeholder="Enter your password"
                    leftIcon={{ type: 'material', name: 'lock'}}
                    value={password}
                    onChangeText={text => setpassword(text)}
                    secureTextEntry
                />
                <Input
                    placeholder="Set your image"
                    leftIcon={{ type: 'material', name: 'face'}}
                    value={imageURL}
                    onChangeText={text => setimageURL(text)}
                />
                <View style={{
                    flex: 1,
                    flexDirection: 'row',
                    justifyContent: 'space-between'
                }}>
                    <View style={{flex: 0.5}}>
                        <Input
                            placeholder="Firstname"
                            leftIcon={{ type: 'material', name: 'person'}}
                            value={firstname}
                            onChangeText={text => setfirstName(text)}
                            style={{width: '40%'}}
                        />
                    </View>
                    <View style={{flex: 0.5}}>
                        <Input
                            placeholder="Lastname"
                            leftIcon={{ type: 'material', name: 'person'}}
                            value={lastname}
                            onChangeText={text => setlastName(text)}
                            style={{width: '40%'}}
                        />
                    </View>
                </View>
                <View style={{
                    flex: 1,
                    flexDirection: 'row',
                    justifyContent: 'space-between'
                }}>
                    <CheckBox
                        center
                        title="Male"
                        checkedIcon="dot-circle-o"
                        uncheckedIcon="circle-o"
                        checked={gender == 'Male'}
                        onPress={() => setgender(gender == 'Male'?'':'Male')}
                        style={{width: '40%'}}
                    />
                    <CheckBox
                        center
                        title="Female"
                        checkedIcon="dot-circle-o"
                        uncheckedIcon="circle-o"
                        checked={gender == 'Female'}
                        onPress={() => setgender(gender == 'Female'?'':'Female')}
                        style={{width: '40%'}}
                    />
                </View>
                <ButtonGroup
                    buttons={['Doctor', 'Nurse', 'Patient']}
                    selectedIndex={selectedIndex}
                    onPress={(value) => {
                        setSelectedIndex(value);
                        if(value==0){
                            setrole('Doctor');
                        }else if(value==1){
                            setrole('Nurse');
                        }else{
                            setrole('Patient');
                        }
                    }}
                    containerStyle={{ marginVertical: 20 }}
                />
                <Input
                    placeholder="Enter your phone"
                    leftIcon={{ type: 'material', name: 'phone'}}
                    value={phone}
                    onChangeText={text => setphone(text)}
                />
                <Input
                    placeholder="Date of Birth (yyyy-mm-dd)"
                    leftIcon={{ type: 'material', name: 'cake'}}
                    value={dateofbirth}
                    onChangeText={text => setDOB(text)}
                />
                <Input
                    placeholder="Enter your heigth (cm)"
                    leftIcon={{ type: 'material', name: 'assessment'}}
                    value={height}
                    onChangeText={text => setheight(text)}
                />
                <Input
                    placeholder="Enter your weight (kg)"
                    leftIcon={{ type: 'material', name: 'assessment'}}
                    value={weight}
                    onChangeText={text => setweight(text)}
                />
                <Button title="submit" containerStyle={{
                    width: 200,
                    marginHorizontal: 50,
                    marginVertical: 10,
                }} onPress = {register}/>
            </ScrollView>
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