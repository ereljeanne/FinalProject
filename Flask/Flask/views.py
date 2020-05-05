"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Flask import app
from Flask.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from Flask.Models.plot_service_functions import plot_to_img



import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from Flask.Models.QureyFormStructure import QueryFormStructure 
from Flask.Models.QureyFormStructure import LoginFormStructure 
from Flask.Models.QureyFormStructure import UserRegistrationFormStructure 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Erel Jeanne',
        year=datetime.now().year,
        message='ways to contact me :)'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='about my project:'
    )

@app.route('/photos')
def photos():
    """Renders the about page."""
    return render_template(
        'photos.html',
        title='Photos',
        year=datetime.now().year,
        message='דתות בישראל'
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/data')
def data():
    """Renders the data page."""

    return render_template(
        'data.html',
        title='My Dataset',
        year=datetime.now().year,
        message='נתוני דרושי עבודה'
    )

@app.route('/dataset1')
def dataset1():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/dataSet1.csv'))

    raw_data_table = df.sample(10).to_html(classes = 'table table-hover')


    """Renders the dataset1 page."""
   
    return render_template(
        'dataset1.html',
        title= 'In this page I will display the dataset I worked on in this project',
        raw_data_table = raw_data_table,
        year = datetime.now().year,
        message= 'these are 10 random lines from my dataset'
        )

@app.route('/dataqurey' , methods = ['GET' , 'POST'])
def dataqurey():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/dataSet1.csv'))
    df = df.drop(['District', 'Age group', 'Gender', 'Education', 'Disability', 'Jobseekers', 'Hh', 'Non academic unemployment', 'Newcomers', 'Newcomers that got fired', 'Academic unemployment'], 1)
    df.rename(columns={ df.columns[4]: "c" }, inplace = True)
    df.rename(columns={ df.columns[3]: "a" }, inplace = True)
    df.rename(columns={ df.columns[2]: "b" }, inplace = True)
    df.rename(columns={ df.columns[1]: "Religion" }, inplace = True)
    df = df.drop(['a', 'b', 'c'], 1)
    df['My new column'] = 'default value'
    df = df.set_index(['Religion', 'Month'])
    df = df.sort_values(by='Religion')
    df = df.groupby(['Religion', 'Month']).count()
    df = df.loc[['אחר', 'דרוזים', 'מוסלמים', 'נוצרים', 'יהודים']]
    df = pd.DataFrame(np.random.rand(10, 5), columns=['דרוזים', 'מוסלמים', 'נוצרים', 'יהודים', 'אחר'])
    df.plot.bar();

    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.plot(ax = ax , kind = 'bar')
    chart = plot_to_img(fig)

    return render_template(
        'dataqurey.html',
        chart = chart,
        height = "300",
        width = "750"
    )