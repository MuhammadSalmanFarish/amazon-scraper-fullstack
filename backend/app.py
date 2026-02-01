from flask import Flask,request,jsonify,send_file
from flask_cors import CORS
from scraper import scrape
from db import get_connection
import pandas as pd




app = Flask(__name__)
CORS(app)

g_product = None

@app.route("/scrape",methods=["POST"])
def scrape_api():
    data=request.get_json()
    product = data.get("product")
    global g_product
    g_product = product
    

    if not product:
        return jsonify({"Error":"No product name provided"}),400
    
    try:
        records = scrape(product)
        
        query = """
                INSERT INTO products (title, price, link, rating, rating_count)
                VALUES (%s, %s, %s, %s, %s)
                """
        conn=get_connection()
        cur = conn.cursor()
        cur.execute("TRUNCATE table products")
        cur.executemany(query,records)
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "status":"success",
            "message":f"Scraping completed for {product}",
            "count":len(records)
        })
    
    except Exception as e:
        print(e)
        return jsonify({
            "status":"Error",
            "message":str(e)
        }),500


@app.route("/products",methods=["GET"]) 
def return_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("Select * from products")
    products = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(products)


@app.route("/download", methods=["GET"])
def download_products():
    try:
        # Connect to DB
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT title, price, link, rating, rating_count FROM products")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=["title", "price", "link", "rating", "rating_count"])

        # Save as Excel temporarily
        file_path = f"{g_product} scraped details.xlsx"
        df.to_excel(file_path, index=False)

        # Send the file to the user
        return send_file(f"C:/Users/salma/OneDrive/Apps/Desktop/python/FS_Project/{g_product} scraped details.xlsx", as_attachment=True)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    


if __name__ =="__main__":
    app.run(debug=True)