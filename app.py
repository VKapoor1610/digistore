from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import bcrypt
from news_api import get_news
from sales_prediction_model import input_processing
#set app as a Flask instance 
app = Flask(__name__)
#encryption relies on secret keys so they could be run
app.secret_key = "testing"

# connect to your Mongo DB database

client = MongoClient("mongodb+srv://b21124:f8Yuo2hEHui6YC3i@cluster0.2kag3bh.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('total_records')
records = db.register

db1 = client.get_database('AddedItems')
addItems = db1.register

db3 = client.get_database('customers')
records1 = db3.register

db2 = client.get_database('Finance')
collectPayment = db2.CollectPayment
Pay = db2.pay

def foo():
    bar= db1.get_collection('register')
    return bar


@app.route("/", methods=["POST", "GET"])
def main():
    return render_template("main.html")


#assign URLs to have a particular route 
@app.route("/shopkeeper_signup", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        news = get_news()
        return render_template('dash.html',news=news)
    
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        ShopName = request.form.get("ShopName")
        type = request.form.get("typeOfShop")
        reg = request.form.get("reg")
        username = request.form.get("username")
        location = request.form.get("location")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed, 'type': type, 'location': location, 'reg': reg, 'username': username, 'ShopName': ShopName}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            news = get_news()
            return render_template('dash.html',news=news)
    return render_template('index.html')

@app.route("/shopkeeper_login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        news = get_news()
        return render_template('dash.html',news=news)

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                news = get_news()
                return render_template('dash.html',news=news)
            else:
                if "email" in session:
                    news = get_news()
                    return render_template('dash.html',news=news)
                message = 'Wrong password'
                return render_template('login_shopkeeper.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login_shopkeeper.html', message=message)
    return render_template('login_shopkeeper.html', message=message)


#  customers
@app.route("/customer_signup", methods=['post', 'get'])
def index1():
    message = ''
    #if method post in index
    if "email" in session:
        news = get_news()
        return render_template('dash.html',news=news)
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
       
        
        username = request.form.get("username")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records1.find_one({"name": user})
        email_found = records1.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('customer.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('customer.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('customer.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed,  'username': username, }
            #insert it in the record collection
            records1.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records1.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('cust_profile.html')
    return render_template('customer.html')

@app.route("/customer_login", methods=["POST", "GET"])
def login1():
    message = 'Please login to your account'
    if "email" in session:
        news = get_news()
        return render_template('dash.html',news=news)

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records1.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                news = get_news()
                return render_template('cust_profile.html',news=news)

            else:
                if "email" in session:
                    news = get_news()
                    return render_template('cust_profile.html',news=news)

                message = 'Wrong password'
                return render_template('cust_profile.html', message=message)
        else:
            message = 'Email not found'
            return render_template('cust_profile.html', message=message)
    return render_template('cust_profile.html', message=message)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("main.html")
    else:
        return render_template('main.html')

# render home page
@ app.route('/')
def home():
    title = 'Home'
    return render_template('dash.html', title=title)

@app.route("/dashboard", methods=["POST", "GET"])
def dash():
    news = get_news()
    return render_template("dash.html", news=news)

@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("users-profile.html")


@app.route("/cart", methods=["POST", "GET"])
def cart():
    return render_template("cart.html")


@app.route("/order", methods=["POST", "GET"])
def order():
    return render_template("order.html")

@app.route("/stock", methods=["POST", "GET"])
def stock():
    if request.method=="POST":
        itemId = request.form.get("itemId")
        name = request.form.get("name")
        quantity = request.form.get("quantity")
        brand = request.form.get("brand")
        cp = request.form.get("cp")
        sp = request.form.get("sp")

        user_input = {'itemId': itemId, 'name': name, 'quantity': quantity, 'brand':brand, 'cp':cp, 'sp':sp}

        if request.form.get('act') == 'add':                        
            addItems.insert_one(user_input)  

        if request.form.get('act') == 'delete':                        
            addItems.delete_one(user_input) 

        if request.form.get('act') == 'update':     
            addItems.update_one({ 'itemId': itemId },
            {"$set": { 'name': name, 'quantity': quantity, 'brand':brand, 'cp':cp, 'sp':sp} })         

    msg=[]
    
    for document in addItems.find():
        msg.append(document)

    return render_template("stock.html",msg=msg)

@app.route("/collect", methods=["POST", "GET"])

def collect():
    if request.method=="POST":
        amount = request.form.get("amount")
        name = request.form.get("name")
        contact = request.form.get("contact")
        user_input = {'amount': amount, 'name': name, 'contact': contact}

        if request.form.get('act') == 'add':                        
            collectPayment.insert_one(user_input)  

        if request.form.get('act') == 'delete':                        
            collectPayment.delete_one(user_input) 

        if request.form.get('act') == 'update':     
            collectPayment.update_one({ "name" : name },
            {"$set": { "amount" : amount, "contact" : contact } })         

    msg=[]
    
    for document in collectPayment.find():
        msg.append(document)

    return render_template("collect.html",msg=msg)

@app.route("/pay", methods=["POST", "GET"])
def pay():
    if request.method=="POST":
        amount = request.form.get("amount")
        name = request.form.get("name")
        contact = request.form.get("contact")
        user_input = {'amount': amount, 'name': name, 'contact': contact}

        if request.form.get('act') == 'add':                        
            Pay.insert_one(user_input)  

        if request.form.get('act') == 'delete':                        
            Pay.delete_one(user_input) 

        if request.form.get('act') == 'update':     
            Pay.update_one({ "name" : name },
            {"$set": { "amount" : amount, "contact" : contact } })         

    msg=[]
    
    for document in Pay.find():
        msg.append(document)

    return render_template("pay.html",msg=msg)

# sales_prediction = define_model()

@app.route("/sales", methods=["POST", "GET"])
def sales():
    if request.method=="POST":
        item = request.form.get("item")
        date = request.form.get("date")
        print(item)
        print(date)
        ans = input_processing([item, date])
        print(ans)
        return render_template("sales.html", prediction = ans)
    return render_template("sales.html")

@app.route("/cust_profile", methods=["POST", "GET"])
def cust_profile():
    return render_template("cust_profile.html")



if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)