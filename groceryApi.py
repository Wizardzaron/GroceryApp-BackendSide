import os
from flask import Flask, render_template, request, redirect, url_for, session, abort, current_app,jsonify
from flask import send_from_directory
from datetime import timedelta
import datetime
from functools import wraps
import sys
import sqlite3

databasename = "products.db"

conn = sqlite3.connect(databasename)

app = Flask(__name__)

#make sure that once the api is mostly completed publish it on github

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = 'productimages'

cur = conn.cursor()

createProductTable = '''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, productName VARCHAR(255) NOT NULL, manufacture VARCHAR(255) NOT NULL,
    price DOUBLE NOT NULL,
 	stock INTEGER NOT NULL,
    description TEXT NOT NULL,
    productImage TEXT NOT NULL);'''

cur.execute(createProductTable)

#dropTable = '''DROP TABLE IF EXISTS products;'''

#cur.execute(dropTable)
@app.route('/products', methods = ['GET'])
def getProducts():

    products = [
        {'productName'  : 'Bannanas', 'stock' : 15, 'productImage' : 'data:image/jpeg;base64,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' },
        {'productName' : 'Spider-Bytes', 'stock' : 24, 'productImage' : 'https://i.ebayimg.com/images/g/5wAAAOSw0bleaQYK/s-l1600.jpg'}
    
    ]
    return jsonify(products)
    cur = conn.cursor()

rows = []
try:
         
    query =  "SELECT productName, stock, productImage FROM products"
    cur.execute(query)
    products = cur.fetchall()

    columns = ('productName', 'stock', 'productImage')

    # creating dictionary
    for row in products:
        print(f"trying to serve {row}", file=sys.stderr)
        rows.append({columns[i]: row[i] for i, _ in enumerate(columns)})
        print(f"trying to serve {rows[-1]}", file=sys.stderr)


except Exception as e:
    error_response = {
        "error": {
            #choose erro 400 because I couldn't find any http code errors for  failed queries.
            "code": 400,
            "message": "Query failed"
        }
    }

@app.route('/Add', methods = ['POST'])
def addProducts():

    cur = conn.cursor()

    productname = request.form['productname']
    manufacture = request.form['manufacture']
    price = request.form['price']
    stock = request.form['stock']
    description = request.form['description']
    productimage = request.form['productimage']
    
    getCountByUsername = '''SELECT COUNT(*) FROM products WHERE productName = %s'''
    cur.execute(getCountByUsername,[productname, productimage])
    countOfProducts = cur.fetchone()

    if countOfProducts[0] != 0 :
        error_response = {
        "error": {
            #choose erro 400 because I couldn't find any http code errors for  failed queries.
            "code": 400,
            "message": "Product already exists in the database"
            }
        }        
        return jsonify(error_response)


    try:
    
        insertNewUser = """INSERT INTO products (productName,manufacture,price,stock,description,productImage) VALUES (%s,%s,%s,%s,%s,%s)"""
        cur.execute(insertNewUser, [productname,manufacture,price,stock,description,productimage])
        conn.commit()

    except Exception as err:

        error_response = {
        "error": {
            #choose erro 400 because I couldn't find any http code errors for  failed queries.
            "code": 400,
            "message": "Query failed"
        }
    }
        return jsonify(error_response)


conn.close()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)