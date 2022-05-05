import React, { useEffect, useState, useLayoutEffect, useCallback } from "react"
import {View, StyleSheet, Alert, LogBox} from 'react-native'
import { Input, Text, Button, ListItem, Icon, Avatar, Tab, TabView } from "react-native-elements"
import { auth, db, baseUrl } from '../firebase'
LogBox.ignoreAllLogs()

const ContactScreen = ({route, navigation}) => {
    const { ID, Title, Json } = route.params;
    const [ index, setIndex] = useState(0);
    const [ select, setSelect] = useState(0)
    const [ selectname, setSelectname] = useState('')
    const [ content, setContent] = useState([])

    useLayoutEffect(() => {
        setContent([])
        getRecord(select)
    }, [select])

    var relatedlist = []
    const makelist = () => {
        for (const [key, value] of Object.entries(Json)) {
            relatedlist.push(value)
            // console.log(key, value)
        }
        return relatedlist
    }

    // consider about null records
    var records = []
    const getRecord = async(id) => {
        var chat = Title=='Your Patients'?'chats_'+ID+'_'+id:'chats_'+id+'_'+ID
        await fetch(baseUrl+':8000/'+chat)
        .then(response => response.json())
        .then(json => {
            for (const [key, value] of Object.entries(json)) {
                records.push(value)
                setContent(records)
            }
            console.log(records)
        })
        .catch((error) => {
            console.error(error);
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
                  title="Contacts"
                  titleStyle={{ fontSize: 12 }}
                  icon={{ name: 'person', type: 'material', color: 'white' }}
              />
              <Tab.Item
                  title="Medical History"
                  titleStyle={{ fontSize: 12 }}
                  icon={{ name: 'favorite', type: 'material', color: 'white' }}
              />
          </Tab>
  
          <TabView value={index} onChange={setIndex} animationType="spring">
              <TabView.Item style={{ width: '100%' }}>
                <View style = {styles.container}>
                    <View>
                    {
                        makelist().map((l, i) => (
                            <ListItem key={i} onPress={() => {setSelect(l.ID), setSelectname(l.First_name), setIndex(1)}} bottomDivider>
                                <ListItem.Content>
                                <ListItem.Title>ID: {l.ID}</ListItem.Title>
                                <ListItem.Subtitle>{l.First_name}</ListItem.Subtitle>
                                </ListItem.Content>
                            </ListItem>
                        ))
                    }
                    </View>
                </View>
              </TabView.Item>
              <TabView.Item style={{ width: '100%' }}>
                  <View>
                    <View>
                    {
                        content.map((l, i) => (
                            <ListItem key={i} bottomDivider>
                                <ListItem.Content>
                                <ListItem.Title>{l.Device} {l.Value}</ListItem.Title>
                                <ListItem.Subtitle>{l.Responsible_Person} {l.Assign_to} {l.Record_time}</ListItem.Subtitle>
                                </ListItem.Content>
                            </ListItem>
                        ))
                    }
                    </View>
                    <View style={{alignItems: 'center'}}>
                        <Button title={'Message to '+selectname} containerStyle={{
                            width: 200,
                            marginHorizontal: 50,
                            marginVertical:'5%'
                        }} onPress = {() => navigation.navigate('Chat', {CHAT: Title=='Your Patients'?'chats_'+ID+'_'+select:'chats_'+select+'_'+ID})} />
                    </View>
                </View>
              </TabView.Item>
          </TabView>
      </>
    )
}

export default ContactScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 10
    },
    text: {
        width: '70%',
        paddingVertical: 15
    }
})