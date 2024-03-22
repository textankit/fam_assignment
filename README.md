# fam_assignment

After successfully started a Python web application!

By running python app.py, initiated a Python script named app.py. This script likely contains the code for web application.
The message "now the server is on local host: http://127.0.0.1:5000/" indicates that web application is now running on local machine. can access it by opening this specific address in web browser: http://127.0.0.1:5000/
This address consists of two parts:
http://127.0.0.1: This is known as the localhost, a special address that refers to own computer.
:5000: This is the port number on which the web application is listening for incoming requests.
Searching within the application:

The endpoint mentioned is /api/videos. This endpoint likely refers to a specific part of web application that deals with videos.
To search for videos using this endpoint, need to add a query string to the web address.

In this case, the query parameter is query. can search for videos by adding "?query=football" to the end of the address, like this: http://127.0.0.1:5000/api/videos?query=football
By doing this, telling the application to search for videos that are related to the term "football"

-- .env file should conatins this for storing data in a collection
MONGODB_HOST = "mongodb://localhost:27017"

used database as Mydb, and collection inside it is youtube_api