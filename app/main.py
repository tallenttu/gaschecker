#!gasapp/bin/

from BeautifulSoup import BeautifulSoup
import requests
import re
from flask import Flask,render_template,request,Markup
from app import app

@app.route('/', methods = ['GET', 'POST'])
def mainPage():
    city = ''
    if request.method == 'POST':
        city = request.form['city']
    r = requests.get('http://www.tennesseegasprices.com/'+city+'/index.aspx')
    soup = BeautifulSoup(r.content)
    entries = []
    address = []
    lstconv = []
    lstname = []
    lstlastupdate = []
    lastupdate = ""
    name = ""
    rangex = ""
    tagremover = re.compile(r'(<\/*?)(?!(em|p|br\s*\/|strong))\w+?.+?>')
    if city != "":

        for x  in xrange(10):
            x = str(x)
            #Initial entries going through rows.
            entries = (soup.find("tr", {"id": "rrlow_"+x}))
            if entries != None:
            #finds the name
                name = entries.find("dt")
                if name.text != "":
                    name = name.text
                else:
                    name = name.find('img')
                    name = Markup(name)
                lstname.append(name)
            
            #Finds the Price
                conv = entries.find("div", {"class": "sp_p"})
                strconv = str(conv)
                strconv = re.sub(r'[^\d]','',strconv)
                strconv = strconv[:1] +"." +strconv[1:]
                lstconv.append(strconv)


            #Finds when Last Updated
                lastupdate = entries.find("div", {"class":"tm"})
                lastupdate = str(lastupdate)
                lastupdate = re.sub(tagremover,'',lastupdate)
                lstlastupdate.append(lastupdate)

            #Finds the Address
                readdress = entries.find("dd")
                if readdress != "":
                    readdress = str(readdress)
                    readdress = re.sub(tagremover,'',readdress)
                    readdress = re.sub(r'&amp','&',readdress)
                    address.append(readdress)
        rangex = xrange(len(lstconv))
    return render_template("index.html",
        address = address,
        lstlastupdate=lstlastupdate,
        lstconv = lstconv,
        lstname = lstname,
        city=city,
        rangex = rangex)