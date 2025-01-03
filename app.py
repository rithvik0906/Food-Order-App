from flask import Flask, render_template, url_for, redirect, session, request
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'secret_key'  # For session management

# In-memory "database" for simplicity
users = {}
menu = {
    "Classic Pizza": 99,
    "Veg Pizza": 149,
    "Chicken Pizza": 199,
    "Special Veg Pizza": 199,
    "Special Chicken Pizza": 249,
    "Fries": 69,
    "Coke": 75,
    "Sprite": 75
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('order'))
        else:
            return "Login failed. Invalid credentials."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            return redirect(url_for('login'))
        else:
            return "Username already exists."
    return render_template('register.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        order_items = {}
        total_amount = 0

        for item, price in menu.items():
            quantity = int(request.form.get(item, 0))
            if quantity > 0:
                order_items[item] = quantity
                total_amount += quantity * price
        
        session['order_items'] = order_items
        session['total_amount'] = total_amount
        return redirect(url_for('bill'))

    return render_template('order.html', menu=menu)

@app.route('/bill', methods=['GET', 'POST'])
def bill():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Retrieve order items and total amount from session
    order_items = session.get('order_items', {})
    total_amount = session.get('total_amount', 0)
    
    if request.method == 'POST':
        address = request.form['address']
        delivery_time = datetime.now() + timedelta(minutes=random.randint(15, 30))
        return render_template('bill.html', order_items=order_items, total_amount=total_amount, menu=menu, address=address, delivery_time=delivery_time.strftime('%H:%M:%S'))
    
    # Pass order_items, total_amount, and menu when rendering the template via GET
    return render_template('bill.html', order_items=order_items, total_amount=total_amount, menu=menu)

if __name__ == '__main__':
    app.run(debug=True)
