# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity_change = db.Column(db.Integer)
    change_type = db.Column(db.Enum('add', 'remove'), nullable=False)
    created_at = db.Column(db.DateTime)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        sku = request.form['sku']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']

        new_product = Product(name=name, sku=sku, category=category, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('view_products'))

    return render_template('add_product.html')

@app.route('/product/update/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.sku = request.form['sku']
        product.category = request.form['category']
        product.quantity = request.form['quantity']
        product.price = request.form['price']

        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('view_products'))

    return render_template('update_product.html', product=product)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)  # Initialize the app with SQLAlchemy

    # Use the application context to create the tables
    with app.app_context():
        db.create_all()  # Creates tables based on the defined models

    # Start the Flask app
    app.run(debug=True)
