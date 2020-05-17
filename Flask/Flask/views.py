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

from Flask.Models.Forms import ExpandForm
from Flask.Models.Forms import CollapseForm

from Flask.Models.QureyFormStructure import QueryFormStructure 
from Flask.Models.QureyFormStructure import LoginFormStructure 
from Flask.Models.QureyFormStructure import UserRegistrationFormStructure
from Flask.Models.QureyFormStructure import DataForm

from Flask.Models.plot_service_functions import GetNormalDataSet


#Home page
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

#contact page
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Erel Jeanne',
        year=datetime.now().year,
        message='ways to contact me :)'
    )

#About page
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='about my projecct',
        year=datetime.now().year,
    )

#Register new user page
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

#Login registered user page
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

#Data Model Page
@app.route('/data')
def data():
    """Renders the data page."""

    return render_template(
        'data.html',
        title='My Dataset',
        year=datetime.now().year,
        message='נתוני דרושי עבודה'
    )
#DataSet Page
@app.route('/dataset1')
def dataset1():
    df2 = GetNormalDataSet()
    df1 = pd.read_csv(path.join(path.dirname(__file__), 'static/Data/dataSet1.csv'))

    raw_data_table1 = df1.sample(10).to_html(classes = 'table table-hover')
    raw_data_table2 = df2.to_html(classes = 'table table-hover')


    """Renders the dataset1 page."""
   
    return render_template(
        'dataset1.html',
        title= 'In this page I am displaying the dataset I worked on in this project',
        raw_data_table1 = raw_data_table1,
        raw_data_table2 = raw_data_table2,
        year = datetime.now().year,
        message= 'these are 10 random lines from my data set on first hand'
        )
#Data qurey page
@app.route('/Data_Qurey' , methods = ['GET' , 'POST'])
def Data_Qurey():
    
    raw_data_table = ''
    #getting a normal data set
    df = GetNormalDataSet()
    #getting the form of the qurey
    form = DataForm(request.form)

    chart=[ ]
    tempchart = ''

    form.sdate.data = ''
    form.edate.data = ''

    if(request.method == 'POST'):
        sdate = form.sdate.data
        edate = form.edate.data
        
        #create a string in HTML of the dataframe as a HTML table
        raw_data_table = df.to_html()

        #make object ready for graph
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'bar')
        tempchart = plot_to_img(fig)
        chart.append(tempchart)

    return render_template(
        'Data_Qurey.html', 
        form = form, 
        raw_data_table = raw_data_table,
        chart = tempchart,
        title='User Data Query',
        year=datetime.now().year,
        message='Please enter the start and end date you choose, to analyze the database.'
   )