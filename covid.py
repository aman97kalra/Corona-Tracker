# import the required libraries
import requests
from bs4 import BeautifulSoup 
import pandas as pd
from flask import Flask, jsonify, escape,render_template,request,redirect,url_for
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS( app )

@app.route('/', )
def hello():
    # name = request.args.get("name", "World")
    return render_template('index.html')

@app.route('/result', methods=['POST','GET'])
def result():
    input = request.form['state']
    newStateName = input_formatter( input ) 
    print(newStateName)
    states=[]
    url = 'https://www.mohfw.gov.in/'
    response = requests.get( url )
    data = response.text
    soup = BeautifulSoup( data, 'html5lib' )

    table = soup.find('div',{'id':'cases'}) 
    
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        list=[]
        for ele in cols:
            ele = ele.text.strip()
            list.append(ele)
            # print(ele)
        states.append(list)

    columns=["S.No","Name of State","Total Indian Confired Cases","Total Confirmed Foreign Cases","Cured Cases","Death"]
    # to generate a csv file of the data
    covid_df= pd.DataFrame(states,columns=["S.No","Name of State","Total Indian Confired Cases","Total Confirmed Foreign Cases","Cured Cases","Death"])
    covid_df.to_csv('stats.csv')

    # print('\n',len(states))

    # states is an list of list
    try:
        for row in states:
            print(row[1])
            array=[]
            array2=[]
            if( input_formatter(row[1])==newStateName ):
                for column in row:
                    print(column)
                    array.append(column)
                break
        for item in states[-2]:
            array2.append(item)
        
        return render_template("result.html",array=array,array2=array2,columns=columns)
    except:
        return render_template("errorPage.html")

# function to format the input and remove white spaces etc.
def input_formatter( input ):
    input = input.replace(' ','')
    input = input.lower()
    return input


if __name__ == '__main__':
    app.run(debug=True)
    