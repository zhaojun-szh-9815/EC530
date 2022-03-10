# Project2: Platform to monitor patients at home or in the hospitals

The goal of the project is to create API for the platform.  
Users can call functions in API to achieve their goals.

## Device Module

Devices module is aimed to **insert, delete, modify, and find** data from SQL database.  
The design of SQL database for device module is shown on  **[Schema](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/Schema.md)**.

The **[phase1 device module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/device_module.py)** do not have flask.  
And **[phase2 device module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/flask_device_module.py)** uses flask to make it as web service platform.

The core of the device module is the SQL database.  
The function called **sqlite_custom_function** is to create constrains in database, which limited the role of responsible_person can only be doctor and nurse and the role of assigned_to can only be patient.  

The module will initial the SQL database, including create the database, create tables, and insert some test data.  
And functions for **insert, delete, modify, and find** need parameters.  
In web service platform, the parameters are given by url.  
And **insert** function will look for related json file, which contains data to insert.  
And **modify** function will look for related json file, which contains data to modify.
The example json file is shown **[here](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/user.json)**

## Chat Module

**[Chat module](https://github.com/zhaojun-szh-9815/EC530/blob/main/Project2/chat_module.py)** is aimed to **record** the chat information.  
It will record the chat information in MongoDB.
For each pair of users, if they start to chat, it will create a MongoDB for the pair of users, named **chat_record_user1_user2**.  
And the MongoDB will init the database by create a collection called **medical_record**, which will store the medical record in Device module.

The chat module can send images.  
If a user want to send a image, the image will be uploaded to the collection called **media_record**.
And the collection called **chat_record** will record the sourse, target, date, time, message_type, and message.
