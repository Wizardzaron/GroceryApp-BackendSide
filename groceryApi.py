import os
from flask import Flask, render_template, request, redirect, url_for, session, abort, current_app,jsonify
from flask import send_from_directory
from datetime import timedelta
import datetime
from functools import wraps
import sys
import sqlite3

databasename = "products.db"

#conn = sqlite3.connect(databasename)

app = Flask(__name__)

#make sure that once the api is mostly completed publish it on github

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

@app.route('/delete', methods = ['DELETE'])
def deleteProduct():
    conn = sqlite3.connect(databasename)
    conn.row_factory = dict_factory 
    cur = conn.cursor()
    try:
        query = "DELETE FROM products WHERE id = ?"
        id = request.args.get('id')
        cur.execute(query, id)
        conn.commit()

        return jsonify({"product": "Deleted"})

    except Exception as err:

        error_response = {
            "err": err,
            "error": {
                #choose erro 400 because I couldn't find any http code errors for  failed queries.
                "code": 400,
                "message": "Query failed"
            }
        }
        return jsonify(error_response)

@app.route('/update', methods = ['PUT'])
def updateStock():
    conn = sqlite3.connect(databasename)
    conn.row_factory = dict_factory 
    cur = conn.cursor()
    try:
        query = "UPDATE products SET stock = ? WHERE id = ?"
        stock = request.form.get('stock')
        id = request.args.get('id')
        cur.execute(query, (stock,id))
        conn.commit()

        return jsonify({"stock": "updated"})

    except Exception as err:

        error_response = {
            "err": err,
            "error": {
                #choose erro 400 because I couldn't find any http code errors for  failed queries.
                "code": 400,
                "message": "Query failed"
            }
        }
        return jsonify(error_response)



@app.route('/description', methods = ['GET'])
def getDescription():
    conn = sqlite3.connect(databasename)
    conn.row_factory = dict_factory 
    cur = conn.cursor()
    try:
        query =  "SELECT * FROM products WHERE id = ?"
        id = request.args.get('id')
        print('SQL Query:', query, 'with ID:', id)
        cur.execute(query,(id, ))
        products = cur.fetchone()

        print(products)

        return jsonify(products)

    except Exception as e:
        error_response = {
            "error": {
                #choose erro 400 because I couldn't find any http code errors for  failed queries.
                "code": 400,
                "message": "Query failed"
            },
            "exception":e
        }
        return jsonify(error_response)



@app.route('/products', methods = ['GET'])
def getProducts():

    conn = sqlite3.connect(databasename)
    conn.row_factory = dict_factory 
    cur = conn.cursor()


    try:
            
        query =  "SELECT id, productName, stock, productImage FROM products"
        cur.execute(query)
        products = cur.fetchall()

        print(products)

        #columns = ('productName', 'stock', 'productImage')

        # creating dictionary
        #for row in products:
        #   print(f"trying to serve {row}", file=sys.stderr)
        #   rows.append({columns[i]: row[i] for i, _ in enumerate(columns)})
        #   print(f"trying to serve {rows[-1]}", file=sys.stderr)
        return jsonify(products)

    except Exception as e:
        error_response = {
            "error": {
                #choose erro 400 because I couldn't find any http code errors for  failed queries.
                "code": 400,
                "message": "Query failed"
            },
            "exception":e
        }
        return jsonify(error_response)
   


@app.route('/product', methods = ['POST'])
def addproduct():

    conn = sqlite3.connect(databasename)
    cur = conn.cursor()
    
    try:
        print(request.form)
        productname = request.form.get('productname')
        manufacture = request.form.get('manufacture')
        print("productname", productname)
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        productimage = request.form.get('productimage')

    

    
    #getCountByUsername = '''SELECT COUNT(*) FROM products WHERE productName = %s'''
    #cur.execute(getCountByUsername,[productname, productimage])
    #countOfProducts = cur.fetchone()

    #if countOfProducts[0] != 0 :
    #    error_response = {
    #    "error": {
    #        #choose erro 400 because I couldn't find any http code errors for  failed queries.
    #        "code": 400,
     #       "message": "Product already exists in the database"
     #       }
     #   } 
    
    #    return jsonify(error_response)



    
        insertNewProduct = """INSERT INTO products (productName,manufacture,price,stock,description,productImage) VALUES (?,?,?,?,?,?)"""
        cur.execute(insertNewProduct, (productname,manufacture,price,stock,description,productimage))
        #cur.execute(insertNewProduct)
        conn.commit()

        return jsonify({"message": "Inserted"})


    except Exception as err:

        error_response = {
            "err": err,
            "error": {
                #choose erro 400 because I couldn't find any http code errors for  failed queries.
                "code": 400,
                "message": "Query failed"
            }
        }
        return jsonify(error_response)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)