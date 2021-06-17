# Flight Price Prediction Application 

## Table of Content
   * [Demo](#Demo)
   * [Overview](#Overview)
   * [Motivation](#Motivation)
   * [User Input](#User-Input)
   * [Installation](#Installation)
   * [Required Files](#Required-Files)
   * [Technical Aspect](#Technical-Aspect)
   * [Report Analysis](#Report-Analysis)
   * [Technologies Used](#Technologies-Used)

## Demo
Link: [https://flight-priceprediction.herokuapp.com/](https://flight-priceprediction.herokuapp.com/)

![](https://i.imgur.com/W56an37.png)


## Overview
This is a simple Machine Learning Regression Prediction application build by using Streamlit API. 

## Motivation
Implementation is always good way of learning. As a part of ML engineering life cycle, this application is part of Feature Engineering, Feature Selection, Model Creation, Accuracy check and model Prediction. Here I have learnt streamlit api functionality and deploying in various cloud platforms.  

## User Input
User can predict approximate flight price by providinh required basic details like Preferred Airline, Source, Destination, Number of Stops, departure and arrival details.

## Installation
This project is built in Python 3.6.9. If you don't have python installed, you can find it [here](https://www.python.org/downloads/). Make sure you are using latest version of pip package. Create a separate virtual environment:
```bash
conda create -n streamlit_app python=3.6
```
Then activate conda environment:
```bash
conda activate streamlit_app
```
After cloning this repository run the below command to install required libraries.
```bash
pip install -r requirements.txt
```

## Required Files
1. requirements.txt
2. Procfile
3. setup.sh

## Technical Aspect
This project is divided into three parts:
1. DataScience Life Cycle [for training run __Flight_Fare_Prediction.ipynb__]
	- Data Collection
	- Feature Engineering
	- Feature Selection
	- Model creation
	- Comparision between different models
	- Hyper Tuning
	- Model Save to pickle file

2. Predicting model by accessing trained pickel model. [run below command to access the webapp]
```bash
streamlit run streamlit_app.py
```

3. Cloud deployment.

	- Go to [Heroku Login Page](https://dashboard.heroku.com/login). If you don't have an account then signup with your email id and if you have already an account then login with your credential. 
	- Click on new application

	![](https://i.imgur.com/z2ATlHX.png)

	- Provide your application name and select a region.

	![](https://i.imgur.com/l89neH2.png)

	- Deploy code through Heroku CLI as instructed below.
	![](https://i.imgur.com/IsD3VWX.png)

## Report Analysis

![](https://i.imgur.com/EKqXOo0.jpg)

![](https://i.imgur.com/1AuN80v.jpg)

__Insight:__</br>
	- Jet Airways airlines fare price are relatively quite high compared with other airlines and Trujet & Spicejet Airlines are having less price.

__Feature Corelation__</br>

![](https://i.imgur.com/b1vFLd0.jpg)

![](https://i.imgur.com/uzEEKrO.png)

![](https://i.imgur.com/8l5xQDe.png)

![](https://i.imgur.com/TfVNKeH.png)


## Technologies Used

![](https://forthebadge.com/images/badges/made-with-python.svg)![](https://forthebadge.com/images/badges/uses-git.svg)

[<img target="_blank" src="https://i.imgur.com/vIZmm5z.png" width=150>](https://pandas.pydata.org/) [<img target="_blank" src="https://i.imgur.com/TceGbix.jpg" width=150>](https://www.streamlit.io/) [<img target="_blank" src="https://upload.wikimedia.org/wikipedia/commons/8/84/Matplotlib_icon.svg">](https://matplotlib.org/) 