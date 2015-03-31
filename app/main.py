from BeautifulSoup import BeautifulSoup
import requests
import re
from flask import Flask,render_template,request,Markup
from app import app

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    """Main Section of the App"""
    state = ""
    city = ''
    if request.method == 'POST':
        space = " "
        state = request.form['state']
        if ' ' in state:
            state = re.sub(' ', '', state)
        city = request.form['city']
        if ' ' in city:
            city = re.sub(' ', '_', city)
        if '.' in city:
            city = city.replace('.', '')

    stateandcity = 'http://www.'+state+'gasprices.com/'+city+'/index.aspx'
    print stateandcity
    r = requests.get(stateandcity)
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

        for x in xrange(10):
            x = str(x)
            # Initial entries going through rows.
            entries = (soup.find("tr", {"id": "rrlow_"+x}))
            if entries:
            # Finds the name
                name = entries.find("dt")
                if name.text != "":
                    name = name.text
                else:
                    name = name.find('img')
                    name = Markup(name)
                lstname.append(name)
            
            # Finds the Price
                price = entries.find("div", {"class": "sp_p"})
                strprice = str(price)
                strprice = re.sub(r'[^\d]','',strprice)
                strprice = strprice[:1] +"." +strprice[1:]
                lstconv.append(strprice)

            # Finds when Last Updated
                lastupdate = entries.find("div", {"class":"tm"})
                lastupdate = str(lastupdate)
                lastupdate = re.sub(tagremover,'',lastupdate)
                lstlastupdate.append(lastupdate)

            # Finds the Address
                readdress = entries.find("dd")
                if readdress != "":
                    readdress = str(readdress)
                    readdress = re.sub(tagremover,'',readdress)
                    readdress = re.sub(r'&amp','&',readdress)
                    address.append(readdress)
        rangex = xrange(len(lstconv))
        # Sends this to the web page
    return render_template("index.html",
                            address = address,
                            lstlastupdate=lstlastupdate,
                            lstconv = lstconv,
                            lstname = lstname,
                            city=city,
                            rangex = rangex)

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    return render_template("login.html")