import React, { useLayoutEffect, useState, useCallback } from "react"
import { auth, db } from '../firebase'
import { GiftedChat } from 'react-native-gifted-chat'

const ChatScreen = ({route}) => {
    const { CHAT } = route.params;
    const [messages, setMessages] = useState([]);

    useLayoutEffect(() => {
        console.log(CHAT)
        const unsubscribe = db.collection(CHAT).orderBy('createdAt', 'desc').onSnapshot(snapshot => setMessages(snapshot.docs.map(doc => ({
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
      db.collection(CHAT).add({
        _id,
        createdAt,
        text,
        user
        })
    }, [])

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