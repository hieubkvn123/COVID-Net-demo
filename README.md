# COVID-Net-demo

# Introduction
This repository is a web demo for the COVID-Net model for COVID-19 image classification for 
diagnosis.

# Set up

## 1. Install all requirements
```
pip3 install -r requirements.txt
```

## 2. Set up SQLite database 
```bash
$ sqlite3 fyp.db < init.sql 
```

## 3. Heroku deployment
```bash
$ heroku git:remote -a <heroku_app_name>  # Set remote git repo to heroku app repo
$ git add . 
$ git commit -am "Commit changes"
$ git push heroku main 
```

# TODO
- [x] Login functionalities.
	- [x] Create the templates and the login form.
	- [x] Create the functionalities to retrieve data from users and compare against databse.
	- [x] Add JWT token based authentication for login function.
	
- [x] Create records and diagnosis.
	- [x] Create the Create Record form.
	- [ ] Create the functionalities to retrieve record data and store in database.
	- [ ] Create a function to redirect X-Ray image to computing server and retrieve result.
	- [ ] Create a function to view all records in tables.

# REFERENCES
- COVID-Net: A Tailored Deep Convolutional Neural Network Design for Detection of COVID-19 Cases from Chest X-Ray Images : [Paper](https://arxiv.org/abs/2003.09871)
- COVID-Net implementation : [Github](https://github.com/hieubkvn123/COVIDNet-Implementation)
