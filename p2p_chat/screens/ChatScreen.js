import React, { useLayoutEffect, useState, useCallback, useEffect } from "react"
import {View, Text, StyleSheet} from 'react-native'
import { Input, Button, Avatar } from "react-native-elements"
import { auth, db } from '../firebase'
import { AntDesign } from '@expo/vector-icons'
import { TouchableOpacity } from "react-native-gesture-handler"
import { signOut } from "firebase/auth";
import { GiftedChat } from 'react-native-gifted-chat'

const ChatScreen = ({navigation}) => {

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
    )
}

export default ChatScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        padding: 10
    }
})