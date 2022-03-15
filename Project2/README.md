# Project2: Platform to monitor patients at home or in the hospitals

The goal of the project is to create API for the platform.  
Users can call functions in API to achieve their goals.

## Device Module

Devices module is aimed to **insert, delete, modify, and find** data from SQL database.  
The design of SQL database for device module is shown on  **[Schema](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/Schema.md)**.

The **[phase1 device module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/device_module.py)** do not have flask.  
And **[phase2 device module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/flask_device_module.py)** uses flask to make it as web service platform.  
And **[phase2 device module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/restful_device_module.py)** uses flask restful API to make it as web service platform.

The core of the device module is the SQL database.  
The function called **sqlite_custom_function** is to create constrains in database, which limited the role of responsible_person can only be doctor and nurse and the role of assigned_to can only be patient.  

The module will initial the SQL database, including create the database, create tables, and insert some test data.  
And functions for **insert, delete, modify, and find** need parameters.  
In web service platform, the parameters are given by url.  
And **insert** function will look for related json file in workspace, which contains data to insert.  
And **modify** function will look for related json file in workspace, which contains data to modify.
The example json file is shown **[here](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/user.json)**

Here are some example command to run the final version **[phase2 device module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/restful_device_module.py)**  

Get: `curl http://10.0.0.61:5000/users -Method GET`  
<img width="883" alt="project2_device1" src="https://user-images.githubusercontent.com/55321300/158283734-ed4eb390-9721-493a-b101-3b7e2c236d2f.PNG">

Post: `curl http://10.0.0.61:5000/users -Method POST`  
<img width="877" alt="project2_device2" src="https://user-images.githubusercontent.com/55321300/158283736-98f5aba1-1d18-4c8c-a261-feb2dbeb1bea.PNG">  

Put: `curl http://10.0.0.61:5000/users -Method PUT`  
<img width="877" alt="project2_device3" src="https://user-images.githubusercontent.com/55321300/158283738-7a528758-09d4-4bd4-bc76-19c2864df9d7.PNG">  

Delete: `curl http://10.0.0.61:5000/users/5 -Method DELETE`  
<img width="905" alt="project2_device4" src="https://user-images.githubusercontent.com/55321300/158283739-d7e7fb47-ba07-423a-8378-47cbf7c0856e.PNG">  

It is similar for other three tables: devices, assignments, records.  

## Chat Module

**[Chat module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/restful_chat_module.py)** is aimed to **record** the chat information.  
It will record the chat information in MongoDB.  

The **reason** to use MongoDB is chat history always contain a lot of text.  
And the relations between collections are not very closed, which means other collections may not be used many times in chat collection.  
So, it can be stored by SQL database, but it is better to use unrelational database.  

For each pair of users, if they start to chat, it will create a MongoDB for the pair of users, named **chat_record_user1_user2**.  
It is default that doctor or nurse creates chat with the patient.  
And the MongoDB will init the database by create a collection called **medical_record**, which will store the medical record in Device module.  

The chat module can send images.  
If a user want to send a image, the image will be uploaded to the collection called **media_record**.  
And the collection called **chat_record** will record the sourse, target, date, time, message_type, and message.  

Here are some example commands to run **[Chat module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/restful_chat_module.py)**.  

Get:  
`curl http://10.0.0.61:5000/chats/2_4 -Method GET`  
It will create chat_history database between user2 (doctor) and user4 (patient) and return the medical records from device module.  

<img width="887" alt="project2_chat1" src="https://user-images.githubusercontent.com/55321300/158285403-bbfd1b3f-c850-40a9-a196-b1649f12612f.PNG">  

`curl http://10.0.0.61:5000/chats/2_4/chat -Method GET`  
It will return the chat history between user2 and user4.  

<img width="884" alt="project2_chat2" src="https://user-images.githubusercontent.com/55321300/158285629-8d4737be-9a6b-419a-bdcb-533a5981107f.PNG">  

`curl http://10.0.0.61:5000/chats/2_4/media -Method GET`  
It will return the media history between user2 and user4.  

<img width="885" alt="project2_chat5" src="https://user-images.githubusercontent.com/55321300/158285878-665e8e96-72fd-4117-b051-8c233285dc63.PNG">  

Delete: `curl http://10.0.0.61:5000/chats/2_4/chat -Method DELETE`  
<img width="865" alt="project2_chat3" src="https://user-images.githubusercontent.com/55321300/158285688-47535c29-7452-41bd-8335-c5adaf3cc53b.PNG">  

Post: `curl http://10.0.0.61:5000/chats/2_4/chat -Method POST`  
<img width="879" alt="project2_chat4" src="https://user-images.githubusercontent.com/55321300/158285761-09f92612-9b24-4a03-844a-607f510f9bb1.PNG">  

This module do not have PUT method, which means the data cannot be modified.  
And user can see a specific image with its name.  
For example, 'test.PNG' is my test image. And it can be shown on browser by address:  
>http://10.0.0.61:5000/chats/2_4/media/test.PNG  
>(It is only an example, it cannot link to the page)
