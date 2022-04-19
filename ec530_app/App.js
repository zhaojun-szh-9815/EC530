import { StatusBar } from "expo-status-bar";
import React, { useState } from "react";
import {
  Alert,
  StyleSheet,
  View,
  Text,
  TextInput,
  ScrollView,
  FlatList,
  TouchableOpacity,
  Pressable,
} from "react-native";
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Dropdown } from 'sharingan-rn-modal-dropdown';

function LoginScreen({navigation}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [id, setid] = useState("");
  const [state, setState] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const onPress = () => {
      if (state == "Success") {
        navigation.navigate('Home', {ROLE: role, NAME: name, ID: id})
      }
      else {
        Alert.alert("Error", "Password or Username incorrect", [{text: "OK"}]);
      }
    };
  
  const register = () => {navigation.navigate('Register')};
 
  const getlogin = async() => {
    await fetch('http://10.0.0.61:5000/user_password/'+username+'/'+password)
    .then(response => response.json())
    .then(json => {
      setState(json.State)
      if (json.State == "Success") {
        setid(json.Content.U_ID)
        setName(json.Content.First_Name)
        setRole(json.Content.Role)
      }
      return;
    })
    .catch((error) => {
      console.error(error);
    });
  }

  return (
    <View style={styles.container}>
 
      <StatusBar style="auto" />
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="username."
          placeholderTextColor="#000000"
          onChangeText={(username) => setUsername(username)}
        />
      </View>
 
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="password."
          placeholderTextColor="#000000"
          secureTextEntry={true}
          onChangeText={(password) => setPassword(password)}
          onEndEditing={() => getlogin()}
        />
      </View>
 
      <TouchableOpacity style={styles.loginBtn} onPress={onPress}>
        <Text style={styles.loginText}>LOGIN</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.loginBtn} onPress={register}>
        <Text style={styles.loginText}>REGISTER</Text>
      </TouchableOpacity>

    </View>
  );
}

function HomeScreen({route, navigation}) {
  const { ROLE, NAME, ID} = route.params;
  const [ Content, setContent] = useState("");
  const [ Title, setTitle] = useState("");

  React.useEffect(() => {
      const unsubscribe = navigation.addListener('focus', () => {
        getrelated()
    });
    return unsubscribe;
  }, [navigation]);

  const getrelated = async() => {
    await fetch('http://10.0.0.61:5000/users/related/'+ID)
    .then(response => response.json())
    .then(json => {
      setTitle(json.Title)
      const arr = []
      if (json.Content != null) {
        Object.keys(json.Content).forEach(function(key) {
          arr.push({id: json.Content[key]["ID"], key: json.Content[key]["First_name"]})
        });
      }
      setContent(arr)
    })
    .catch((error) => {
      console.error(error)
    });
  }

return (
  <View style={styles.listcontainer}>
    <Text>Welcome {ROLE} {NAME}!</Text>
    <Text>{Title}</Text>
    <FlatList
      data = {Content}
      renderItem={({item}) => 
      <TouchableOpacity style={styles.listitem} onPress={() => navigation.navigate('Chat', {END1: ID, END2: item.id})}>
      <Text style={styles.loginText}>{item.key}</Text>
      </TouchableOpacity>}
      //renderItem={({item}) => <Text style={styles.listitem}>{item.key}</Text>}
    />
  </View>
);
}

function RegisterScreen({navigation}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [fname, setfName] = useState("");
  const [lname, setlName] = useState("");
  const [gender, setGender] = useState("");
  const [role, setRole] = useState("");
  const [phone, setPhone] = useState("");
  const [Date_of_Birth, setDOB] = useState("");
  const [Height_in_cm, setHeight] = useState("");
  const [Weight_in_kg, setWeight] = useState("");
  const onPress = async() => {
    await fetch('http://10.0.0.61:5000/users', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "Username": username,
        "Password": password,
        "First_Name": fname,
        "Last_Name": lname,
        "Gender": gender,
        "Role": role,
        "Phone": phone,
        "Date_of_Birth": Date_of_Birth,
        "Height_in_cm": Height_in_cm,
        "Weight_in_kg": Weight_in_kg
      })
    })
    .then(response => response.json())
    .then(json => {
      if (json == null) {
        Alert.alert("Error", "Unsuccessed", [{text: "OK"}]);
      }
      return;
    })
    .catch((error) => {
      console.error(error);
    });
    };

  return (
    <ScrollView contentContainerStyle={{ flexGrow: 1, alignItems: 'center', alignSelf: 'stretch', paddingVertical: '10%'}}>
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="username."
          placeholderTextColor="#000000"
          onChangeText={(username) => setUsername(username)}
        />
      </View>
 
      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="password."
          placeholderTextColor="#000000"
          secureTextEntry={true}
          onChangeText={(password) => setPassword(password)}
        />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="first name."
          placeholderTextColor="#000000"
          onChangeText={(password) => setfName(password)}
        />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="last name."
          placeholderTextColor="#000000"
          onChangeText={(password) => setlName(password)}
        />
      </View>

      <View style={styles.Dropdowncontainer}>
          <Dropdown
            label="gender"
            data={[
              {
                value: 'Male',
                label: 'Male'},
              {
                value: 'Female',
                label: 'Female'}]}
            value={gender}
            onChange={(value) => setGender(value)}
          />
      </View>

      <View style={styles.Dropdowncontainer}>
          <Dropdown
            label="role"
            data={[
              {
                value: 'Doctor',
                label: 'Doctor'},
              {
                value: 'Nurse',
                label: 'Nurse'},
              {
                value: 'Patient',
                label: 'Patient'}]}
            value={role}
            onChange={(value) => setRole(value)}
          />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="phone. (10 digits)"
          placeholderTextColor="#000000"
          onChangeText={(password) => setPhone(password)}
        />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="Date of Birth (yyyy-mm-dd)."
          placeholderTextColor="#000000"
          onChangeText={(password) => setDOB(password)}
        />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="height (cm)."
          placeholderTextColor="#000000"
          onChangeText={(password) => setHeight(password)}
        />
      </View>

      <View style={styles.inputView}>
        <TextInput
          style={styles.TextInput}
          placeholder="weight (kg)."
          placeholderTextColor="#000000"
          onChangeText={(password) => setWeight(password)}
        />
      </View>

      <TouchableOpacity style={styles.loginBtn} onPress={onPress}>
        <Text style={styles.loginText}>SUBMIT</Text>
      </TouchableOpacity>
    </ScrollView>
  );
  }

  function ChatScreen({route, navigation}) {
    const { END1, END2 } = route.params;
  
  return (
    <View style={styles.container}>
      <Text>Chat between {END1} and {END2} will be push later</Text>
    </View>
  );
  }

const Stack = createNativeStackNavigator();

export default function App() {
return (
  <NavigationContainer>
    <Stack.Navigator>
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Chat" component={ChatScreen} />
    </Stack.Navigator>
  </NavigationContainer>
);
}
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },

  listcontainer: {
    flex: 1,
    paddingTop: 22,
    backgroundColor: "#fff",
    alignItems: "center",
   },

  listitem: {
    padding: 10,
    fontSize: 18,
    height: 44,
  },

  Dropdowncontainer: {
    width: '70%',
    height: 80,
    flex: 1,
  },

  inputView: {
    backgroundColor: "#D0D0D0",
    borderRadius: 30,
    width: "70%",
    height: 45,
    marginBottom: 20,
    alignItems: "center",
  },
 
  TextInput: {
    height: 50,
    flex: 1,
    padding: 10,
    marginLeft: 20
  },
 
  loginBtn: {
    width: "80%",
    borderRadius: 25,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 40,
    backgroundColor: "#C0C0C0",
  },
});