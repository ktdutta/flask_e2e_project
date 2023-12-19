# flask_e2e_project


## My Application 

For my final project I decided to create a patient database application which healthcare workers such as medical scribes can utilize when taking preliminary visit notes during the patient’s visit. The application requires google authorization before gaining access to the application. Once you gain access to the application, there are two functions you can perform: view previous patient visit history (past user inputted data) and add new patient visit information via a form. You can access these two functions using the navigation bar on the home page. 


## Technology Used 

1. Github was utilized to maintain my application’s version control
2. A .env file was used to maintain privacy of credentials 
3. Python to develop the backend framework of flask application 
4. Tailwind CSS/html to create the frontend framework of the application 
5. GCP to create a MySQL database
6. SQLAlchemy to allow database interaction 
7. API as a single endpoint within the backend of my flask application 
8. Google OAuth to set up google authorization to maintain user and data security 
9. Logger to print out the application’s log statements 
10. Docker to containerize the application 
11. GCP to deploy the application


## .env File Template 

```
USER= 
PASSWORD= 
NAME= 
GOOGLE_CLIENT_SECRET= 
GOOGLE_CLIENT_ID= 
HOST= 
PORT= 
CHARSET= 
DATABASE =
```
