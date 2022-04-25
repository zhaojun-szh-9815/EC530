import React, { useLayoutEffect, useState, useEffect, useCallback } from "react"
import { ImageBackground, View, StyleSheet} from 'react-native'
import { Text, Avatar, Tab, TabView } from "react-native-elements"
import { TouchableOpacity } from "react-native-gesture-handler"
import { AntDesign } from '@expo/vector-icons'
import { auth, db } from '../firebase'
import { signOut } from "firebase/auth";
import { GiftedChat } from 'react-native-gifted-chat'

const image = { uri: "https://cdn.vectorstock.com/i/1000x1000/44/24/background-of-hospital-ward-vector-8744424.webp" };

function HomeScreen({route, navigation}) {
    const { Json } = route.params;
    const [ index, setIndex] = useState(1);
  
    const [messages, setMessages] = useState([]);

    useLayoutEffect(() => {
        const unsubscribe = db.collection('chats').orderBy('createdAt', 'desc').onSnapshot(snapshot => setMessages(snapshot.docs.map(doc => ({
          _id: doc.data()._id,
          createdAt: doc.data().createdAt.toDate(),
          text: doc.data().text,
          user: doc.data().user
        }))))
        return unsubscribe;
    }, [])
  
    const onSend = useCallback((messages = []) => {
      setMessages(previousMessages => GiftedChat.append(previousMessages, messages))
      const {
          _id,
          createdAt,
          text,
          user
      } = messages[0]
      db.collection('chats').add({
        _id,
        createdAt,
        text,
        user
        })
    }, [])

    useLayoutEffect(() => {
        navigation.setOptions({
            headerLeft: () => (
                <View style={{marginLeft: 20}}>
                    <Avatar
                        rounded
                        source={{
                            uri: auth?.currentUser?.photoURL
                        }}
                    />
                </View>
            ),
            headerRight: () => (
                <TouchableOpacity style={{marginRight: 20}} onPress = {signout}>
                <AntDesign name="logout" size={24} color="black"/>
                </TouchableOpacity>
            )
        })
    }, [])

    const signout = () => {
        signOut(auth).then(() => {
            // Sign-out successful.
            navigation.replace('Login')
          }).catch((error) => {
            // An error happened.
          });
    }
  
  return (
      <>
        <Tab
            value={index}
            onChange={(e) => setIndex(e)}
            indicatorStyle={{
                backgroundColor: 'white',
                height: 3,
            }}
            variant="primary"
        >
            <Tab.Item
                title="Profile"
                titleStyle={{ fontSize: 12 }}
                icon={{ name: 'person', type: 'material', color: 'white' }}
            />
            <Tab.Item
                title="Home"
                titleStyle={{ fontSize: 12 }}
                icon={{ name: 'home', type: 'material', color: 'white' }}
            />
            <Tab.Item
                title="Contect"
                titleStyle={{ fontSize: 12 }}
                icon={{ name: 'chat', type: 'material', color: 'white' }}
            />
        </Tab>

        <TabView value={index} onChange={setIndex} animationType="spring">
            <TabView.Item style={{ width: '100%' }}>
                <View style={{alignItems:'center', paddingVertical: 20}}>
                    <Text style={styles.text}>ID: {Json["U_ID"]}</Text>
                    <Text style={styles.text}>Username: {Json["Username"]}</Text>
                    <Text style={styles.text}>Name: {Json["First_Name"]} {Json["Last_Name"]}</Text>
                    <Text style={styles.text}>Gender: {Json["Gender"]}</Text>
                    <Text style={styles.text}>Role: {Json["Role"]}</Text>
                    <Text style={styles.text}>Phone: {Json["Phone"]}</Text>
                    <Text style={styles.text}>Date_of_Birth: {Json["Date_of_Birth"]}</Text>
                    <Text style={styles.text}>Height(cm): {Json["Height_in_cm"]}</Text>
                    <Text style={styles.text}>Weight)kg: {Json["Weight_in_kg"]}</Text>
                </View>
            </TabView.Item>
            <TabView.Item style={{ width: '100%' }}>
                <View style={{flex: 1}}>
                    <ImageBackground source={image} resizeMode="cover" style={{flex: 1, paddingTop: '10%'}}>
                        <Text style={{textAlign: 'center', fontSize: 23, fontWeight: "bold"}}>Welcome {Json["Role"]} {Json["First_Name"]}!</Text>
                    </ImageBackground>
                </View>
            </TabView.Item>
            <TabView.Item style={{ width: '100%' }}>
                <GiftedChat
                    messages={messages}
                    showAvatarForEveryMessage={true}
                    onSend={messages => onSend(messages)}
                    user={{
                        _id: auth?.currentUser?.email,
                        name: auth?.currentUser?.displayName,
                        avatar: auth?.currentUser?.photoURL
                    }}
                />
            </TabView.Item>
        </TabView>
    </>
  );
  }

export default HomeScreen

const styles = StyleSheet.create({
    text: {
        width: '70%',
        paddingVertical: 15
    }
})