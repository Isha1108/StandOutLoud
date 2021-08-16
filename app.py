import flask
from flask import Flask, render_template, request
import random, copy
from flask import Flask, render_template, request, redirect, url_for, session
import re
import pickle
from flask_mysqldb import MySQL
import MySQLdb.cursors
import io
import base64
import numpy as np
import razorpay



app = Flask(__name__)

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'small_scale_entrepreneurs'

mysql = MySQL(app)
app.secret_key = 'key12'

model = pickle.load(open('model1.pkl', 'rb'))
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'User_id' in request.form and 'user_password' in request.form and 'Name' in request.form and 'contact' in request.form and 'city' in request.form and 'locality' in request.form and 'address' in request.form and 'usertype' in request.form and 'business_field' in request.form and 'user_pincode' in request.form:
        # Create variables for easy access
        User_id = request.form['User_id']
        user_password = request.form['user_password']
        Name = request.form['Name']
        locality = request.form['locality']
        city = request.form['city']
        address = request.form['address']
        user_pincode = request.form['user_pincode']
        contact = request.form['contact']
        usertype = request.form['usertype']
        business_field = request.form['business_field']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE User_id = %s AND user_password=%s', [User_id, user_password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            
    
        elif not re.match(r'[A-Za-z0-9]+', User_id):
            msg = 'Username must contain only characters and numbers!'
            
        elif not User_id or not user_password:
            msg = 'Please fill out the form!'
            
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', [User_id, user_password,Name,contact,city,locality,address,usertype,business_field,user_pincode])
            mysql.connection.commit()
            msg = 'Successfully registered! Please Log-In'
            
            return render_template('Login.html', msg=msg)
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template("register.html")

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if request.method == 'POST' and 'User_id' in request.form and 'user_password' in request.form:
        # print("gg")
        # Create variables for easy access
        User_id = request.form['User_id']
        user_password = request.form['user_password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE User_id = %s AND user_password = %s', (User_id, user_password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        
        if account['usertype'] == "Customer":
            # print("b")
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['User_id'] = account['User_id']
            session['address'] = account['address']
            session['contact'] = account['contact']
            account['usertype'] = "Customer"
            # Redirect to home page
            
            return redirect(url_for('Customer_home'))
        elif account['usertype'] == "Entrepreneur":
            return redirect(url_for('Entrepreneur_home'))   
        elif account['usertype'] == "Investor":
            return redirect(url_for('Investor_home'))

    return render_template('Login.html')   


@app.route("/Customer_home", methods=['GET', 'POST'])
def Customer_home():
    return render_template("Customer_home.html")

@app.route("/Request", methods=['GET', 'POST'])
def Request():
    shops1 = []
    if request.method == 'POST' and 'category' in request.form and 'p_details' in request.form:
        details = request.form['p_details']
        category = request.form['category']
        user = session['User_id'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO make_request VALUES(%s,%s,%s)', [user, details, category])
        mysql.connection.commit()
        # print(category)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     
        if category=="Artistic":
            cursor.execute("SELECT * FROM shopslist WHERE business_category = 'Artistic'")
        elif category=="Customized Clothing":
            cursor.execute("SELECT * FROM shopslist WHERE business_category = 'Customized Clothing'")
        elif category=="Catering":
            cursor.execute("SELECT * FROM shopslist WHERE business_category = 'Catering'")
        shops =cursor.fetchall()
        # print(shops)
        shops = list(shops)
        
        for i in range(len(shops)):
            x = shops[i]
            shops2 = []
            for key in x.values():
                shops2.append(key)
            shops1.append(shops2)
        # print(shops1)
    return render_template("Request.html")



# @app.route("/Shopslist", methods=['GET', 'POST'])
# def Shopslist():
#     return render_template("Shopslist.html")

@app.route("/Shopslist", methods=['GET', 'POST'])
def Shopslist():
    shops1 = []    
    user = session['User_id'] 
    # category = c
    # print(c)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     
    cursor.execute("SELECT * FROM shopslist")
    shops =cursor.fetchall()
    # print(shops)
    shops = list(shops)
    
    for i in range(len(shops)):
        x = shops[i]
        shops2 = []
        for key in x.values():
            shops2.append(key)
        shops1.append(shops2)
    # print(shops1)
    # print('heloooooooooooooooooooooo')
    return render_template("Shopslist.html", shops1=shops1)

    
    
@app.route("/ShopProfile/<n>", methods=['GET', 'POST'])
def ShopProfile(n):
    name="buss A"
    # print(name+"jygdwutgsi8zyia")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM shopslist WHERE business_name=%s', (name,))
    # cursor.execute("SELECT * FROM shopslist WHERE business_name:=name", {'business_name' : str(name)})
    sp = cursor.fetchall()
    print(sp)
    print('heyyyyyyyyyyyyyyy')
    sp = list(sp)
    sp1=[]
    for i in range(len(sp)):
        x = sp[i]
        sp2 = []
        for key in x.values():
            sp2.append(key)
        sp1.append(sp2)
    # print(sp1)    

    return render_template("ShopProfile.html",sp1=sp1)

@app.route("/BuyProduct", methods=['GET', 'POST'])
def BuyProduct():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products")
    prod =cursor.fetchall()
    # print(prod)
    prod = list(prod)
    prod1=[]
    for i in range(len(prod)):
        x = prod[i]
        prod2 = []
        for key in x.values():
            prod2.append(key)
        prod1.append(prod2)
    # print(prod1)
    return render_template("BuyProduct.html", prod1=prod1)

@app.route("/History", methods=['GET', 'POST'])
def History():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM order_history")
    hist =cursor.fetchall()
    # print(hist)
    hist = list(hist)
    hist1=[]
    for i in range(len(hist)):
        x = hist[i]
        hist2 = []
        for key in x.values():
            hist2.append(key)
        hist1.append(hist2)
    # print(hist1)

    return render_template("History.html", hist1=hist1)

@app.route("/payment", methods=['GET', 'POST'])
def payment():    
    return render_template("payment.html")

@app.route("/payment2/<p>", methods=['GET', 'POST'])
def payment2(p):  
    # p= "akash"
    # print(p)
    return render_template("payment.html", p=p)
    

    # ENTREPRENEUR SIDE

@app.route("/Entrepreneur_home", methods=['GET', 'POST'])
def Entrepreneur_home():
    return render_template("Entrepreneur_home.html")


@app.route("/ReceivedRequests/<ord>", methods=['GET', 'POST'])
def ReceivedRequests(ord):
    RR1=[]
    # print(ord)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM receivedrequests")
    
    RR =cursor.fetchall()
    # print(RR)
    RR = list(RR)
    
    for i in range(len(RR)):
        x = RR[i]
        RR2 = []  
        for key in x.values():
            RR2.append(key)
        RR1.append(RR2)
    # print(RR1)
    if request.method == 'POST' and 'status' in request.form:
        
        status = request.form['status']
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor1.execute("UPDATE order_history SET status=%s WHERE order_id=%s", (status,ord))
        mysql.connection.commit()
        # if status=="Accepted":
        #     cursor1.execute("UPDATE order_history SET status='Accepted' WHERE order_id=1")
        #     mysql.connection.commit()
        # elif status=="Declined":
        #     cursor1.execute("UPDATE order_history SET status='Declined' WHERE order_id=2")
        #     mysql.connection.commit()
        # elif status=="Pending":
        #     cursor1.execute("UPDATE order_history SET status='Pending' WHERE order_id=3")   
        #     mysql.connection.commit()   

    
    return render_template("ReceivedRequests.html", RR1=RR1)

@app.route("/ReceivedPayments", methods=['GET', 'POST'])
def ReceivedPayments():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM receivedpayments")
    RP =cursor.fetchall()
    # print(RP)
    RP = list(RP)
    RP1=[]
    for i in range(len(RP)):
        x = RP[i]
        RP2 = []
        for key in x.values():
            RP2.append(key)
        RP1.append(RP2)
    # print(RP1)
    return render_template("ReceivedPayments.html", RP1=RP1)

@app.route("/ViewFeedback", methods=['GET', 'POST'])
def ViewFeedback():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM feedback")
    v =cursor.fetchall()
    # print(v)
    v = list(v)
    v1=[]
    for i in range(len(v)):
        x = v[i]
        v2 = []
        for key in x.values():
            v2.append(key)
        v1.append(v2)
    # print(v1)
    return render_template("ViewFeedback.html", v1=v1)

@app.route("/GiveFeedback", methods=['GET', 'POST'])
def GiveFeedback():

    return render_template("GiveFeedback.html")

# @app.route("/GiveFeedback2/<p>", methods=['GET', 'POST'])
# def GiveFeedback2(p):
#     print(p)
    
#     return render_template("GiveFeedback.html")

@app.route("/Job", methods=['GET', 'POST'])
def Job():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM shopslist")
    job =cursor.fetchall()
    # print(job)
    job = list(job)
    job1=[]
    for i in range(len(job)):
        x = job[i]
        job2 = []
        for key in x.values():
            job2.append(key)
        job1.append(job2)
    # print(job1)
    return render_template("Job.html", job1=job1)

@app.route("/UpdateProfile", methods=['GET', 'POST'])
def UpdateProfile():
    return render_template("UpdateProfile.html")



        # INVESTOR SIDE

@app.route("/Investor_home", methods=['GET', 'POST'])
def Investor_home():
    return render_template("Investor_home.html")



@app.route("/Investor_ViewBusinesses", methods=['GET', 'POST'])
def Investor_ViewBusinesses():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM shopslist")
    vb =cursor.fetchall()
    # print(vb)
    vb = list(vb)
    vb1=[]
    for i in range(len(vb)):
        x = vb[i]
        vb2 = []
        for key in x.values():
            vb2.append(key)
        vb1.append(vb2)
    # print(vb1)
    return render_template("Investor_ViewBusinesses.html", vb1=vb1)


#PAYMENT------------------------------------------

client = razorpay.Client(auth=("rzp_test_LmhpX8lHqglzls","hBeWUMgRLJckGg6ajrrdn27K"))

@app.route('/pay', methods = ['GET', 'POST'])
def pay():
    # if request.method == 'POST' and 'amount' in request.form: 
    #     amount = request.form['amount']
        
    #     name_of_shopowner = "hxiuzh"
    #     amount =int(100*(amount)) 
    #     payment = client.order.create({'amount' : int(amount), 'currency' : 'INR', 'payment_capture' : '1' })
        
    # return render_template('payment.html',name_of_shopowner=name_of_shopowner,payment=payment)
    name_of_event = 'example'
    amount = 200 * 100
    payment = client.order.create({'amount' : amount, 'currency' : 'INR', 'payment_capture' : '1'})
    event_details = [name_of_event]
    if request.form:
        
        amount = int(request.form['amount']) * 100
        payment = client.order.create({'amount' : amount, 'currency' : 'INR', 'payment_capture' : '1'})
        event_details = [name_of_event]
        return render_template('payment.html',event_details=event_details,payment=payment)
    return render_template('payment.html',event_details=event_details,payment=payment)
    
@app.route('/success', methods = ['GET', 'POST'])
def success():
    return render_template('success.html')

#MODEL----------------------------

model=pickle.load(open('model1.pkl','rb'))

@app.route("/InvestorStatistic", methods=['GET', 'POST'])
def InvestorStatistic():
    from datetime import date
    today = date.today()
    full_date = str(today)
    
    date1 =int( full_date.split('-')[2])
    year = int(full_date.split('-')[0])
    month = full_date.split('-')[1]
    if month[0] == '0':
        month = int(month[1])
    lst = []
    average = []
    for i in range(1,5):        
        lst.append(int(model.predict([[i, month, date1, year]]))) 

    # cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # for i in range(11,15):
    #     for x in lst:
    #         cursor1.execute("UPDATE shopslist SET predicted=%s WHERE entr_id=%s", (x, i))
    #         mysql.connection.commit()  

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM shopslist")
    ist =cursor.fetchall()
    # print(ist)
    ist = list(ist)
    ist1=[]
    for i in range(len(ist)):
        x = ist[i]
        ist2 = []
        for key in x.values():
            ist2.append(key)
        ist1.append(ist2)
    # print(ist1)  
            
    # print(lst)
    # print("Today's date:", today)
    return render_template("InvestorStatistic.html", ist1=ist1, lst=lst)

if __name__ =="__main__":
    app.run(debug=True)