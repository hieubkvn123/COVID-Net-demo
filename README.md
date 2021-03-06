# COVID-Net-demo

# Introduction
This repository is a web demo for the COVID-Net model for COVID-19 image classification for 
diagnosis.

# System Diagram
<img src="misc/FYP_System_Diagram.png"/>

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

## 4. Setting up deployment server
- 1. Go to https://github.com/hieubkvn123/COVID-Net.
- 2. Clone the repository to a public computing server.
- 3. Go to https://github.com/lindawangg/COVID-Net/blob/master/docs/models.md and download the COVIDNet-CXR-2 model and put it
into the models folder of the COVID-Net repository cloned in step 1.
- 4. Run the ``serve_model.sh`` script to deploy the covidnet model.
- 5. (**NOTE**) If the port 8889 is not public in the computing server. Enable port 8889 using firewall-cmd:
```bash
 firewall-cmd --permanent --zone=public --add-port=8889/tcp
 firewall-cmd --reload
```

## 5. Building documentations
- 1. Requirements : Install sphinx from PYI with 
```bash
pip3 install -U sphinx
```
- 2. Go to ```./docs``` and build the documentation
```bash
cd docs
sphinx-apidoc -f -o . ..
make html
```
- 3. Open the documentation in ```./docs/_build/html/index.html```

<br>

# TODO
- [x] Login functionalities.
	- [x] Create the templates and the login form.
	- [x] Create the functionalities to retrieve data from users and compare against databse.
	- [x] Add JWT token based authentication for login function.
	
- [x] For prototype : Create records and diagnosis.
	- [x] Create the Create Record form.
	- [x] Create the functionalities to retrieve record data and store in database.
	- [x] Create a function to redirect X-Ray image to computing server and retrieve result.
	- [x] Create a function to view all records in tables.

- [x] Preliminaries.
	- [x] Document all of the existing functionalities.
	- [ ] Compile test cases where applicable before proceeding.

- [x] For final presentation.
	- [x] Finish the sorting patient records functionality,
	- [x] Finish the search functionality.
	- [x] Finish the view individual patient's record functionality.
	- [ ] Finish the update individual patient's record functionality.
	- [ ] Finish the delete individual patient's record functionality.

- [ ] Further functionalities.
	- [ ] Create an advanced search section to look for patient's diagnosis history.
	- [ ] Create a function to create mass-prediction for multiple profiles.

# REFERENCES
- COVID-Net: A Tailored Deep Convolutional Neural Network Design for Detection of COVID-19 Cases from Chest X-Ray Images : [Paper](https://arxiv.org/abs/2003.09871)
- COVID-Net implementation : [Github](https://github.com/hieubkvn123/COVIDNet-Implementation)
