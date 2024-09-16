from flask import *
import re
import sqlite3  
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
app = Flask(__name__) 
app.secret_key = 'mysecretkey' 
 
# define a dictionary of admin usernames and passwords
admin_users = {
    'admin': 'Password@123'
}



# define a dictionary of signed-up users
signed_up_users = {}


# define a route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # check if user is signed up
        if request.form['username'] in signed_up_users and request.form['password'] == signed_up_users[request.form['username']]:
            session['user_type'] = 'normal'
            return redirect(url_for('normal_home'))
        # check if admin user
        elif request.form['username'] in admin_users and request.form['password'] == admin_users[request.form['username']]:
            session['user_type'] = 'admin'
            return redirect(url_for('admin_home'))
        # invalid login
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)

# define a route for the sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # check if password meets validation requirements
        password = request.form['password']
        if (len(password) < 8 or not re.search('[a-z]', password) or not re.search('[A-Z]', password)
            or not re.search('[0-9]', password) or not re.search('[^A-Za-z0-9]', password)):
            return render_template('signup.html', error='Password must be at least 8 characters long, contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character.')
        # check if passwords match
        if request.form['password'] != request.form['confirm_password']:
            return render_template('signup.html', error='Passwords do not match.')
        # add new user to signed_up_users dictionary
        signed_up_users[request.form['username']] = password
        # redirect to login page
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

# define a route for the admin home page
@app.route('/admin_home')
def admin_home():
    # check if user is admin
    if session.get('user_type') == 'admin':
        return render_template('index.html')
    # redirect to login if not admin
    else:
        return redirect(url_for('login'))

# define a route for the normal user home page
@app.route('/normal_home')
def normal_home():
    # check if user is normal
    if session.get('user_type') == 'normal':
        return render_template('normal_home.html')
    # redirect to login if not normal
    else:
        return redirect(url_for('login'))

@app.route('/')  
def index():  
    return render_template('index.html'); 

@app.route('/view', methods=['GET', 'POST'])
def view():  
    con = sqlite3.connect('amazon_project.db')  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    # cur.execute('SELECT products.*, review_rating_data.* FROM products LEFT JOIN review_rating_data ON products.product_id = review_rating_data.product_id')    
    query = 'SELECT products.* FROM products'
    search_term = request.form.get('search_term', None)
    search_column = request.form.get('search_column', 'product_name')
    if search_term:
        query += f' WHERE {search_column} LIKE ?'
        cur.execute(query, ('%' + search_term + '%',))
    else:
        cur.execute(query)
    rows = cur.fetchall()
    if session.get('user_type') == 'admin':
        return render_template('view.html',rows = rows) 
    else:
        return render_template('view_normal.html',rows = rows)



@app.route("/add")  
def add():  
    return render_template("add.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            product_id = request.form["product_id"]  
            product_name = request.form["product_name"]  
            about_product = request.form["about_product"] 
            with sqlite3.connect("amazon_project.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into products (product_id, product_name, about_product) values (?,?,?)",(product_id, product_name, about_product))  
                con.commit()  
                msg = "Record successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the record to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()  

# @app.route("/delete")  
# def delete():  
#     return render_template("delete.html")  

@app.route('/delete_row/<string:product_id>', methods=['POST', 'GET'])
def delete_row(product_id):
    con = sqlite3.connect('amazon_project.db')
    cur = con.cursor()

    cur.execute('DELETE FROM products WHERE product_id=?', (product_id,))
    con.commit()
    con.close()
    return redirect(url_for('view'))
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    product_id = request.form["product_id"]  
    with sqlite3.connect("amazon_project.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("DELETE from products where product_id = ?",(product_id,))
            con.commit()   
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)



@app.route("/edit_record/<string:product_id>",methods=['POST','GET'])
def edit_record(product_id):
    if request.method=='POST':
        product_name=request.form['product_name']
        about_product=request.form['about_product']
        con=sqlite3.connect("amazon_project.db")
        cur=con.cursor()
        cur.execute("update products set product_name=?,about_product=? where product_id=?",(product_name, about_product, product_id))
        con.commit()
        flash('Record Updated','success')
        return redirect(url_for("view"))
    con=sqlite3.connect("amazon_project.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from products where product_id=?",(product_id,))
    data=cur.fetchone()
    return render_template("edit_record.html",datas=data)


@app.route('/update/<string:product_id>', methods=['GET', 'POST'])
def update(product_id):
    con = sqlite3.connect('amazon_project.db')
    cur = con.cursor()

    if request.method == 'POST':
        product_name = request.form.get('product_name')  # get the value of product_name or None if it's missing
        about_product = request.form.get('about_product')  # get the value of about_product or None if it's missing

        # check if either product_name or about_product is missing
        if product_name is None or about_product is None:
            return "Missing product_name or about_product field", 400  # return an error response with status code 400

        cur.execute("UPDATE products SET product_name=?, about_product=? WHERE product_id=?", (product_name, about_product, product_id))
        con.commit()
        return redirect(url_for('view'))

    cur.execute('SELECT * FROM products WHERE product_id=?', (product_id,))
    data = cur.fetchone()
    con.close()
    return render_template('update.html', product=data)


df = pd.read_csv('products.csv')
@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST' and 'dropdown' in request.form:
        selected_option = request.form['dropdown']
        if selected_option == 'expensive':
            top_5_expensive = df.nlargest(5, 'actual_price')
            top_5_expensive['Product_Name'] = top_5_expensive['product_name'].apply(lambda x: ' '.join(x.split()[:10]))
            plot_data = px.bar(top_5_expensive, x='Product_Name', y='actual_price',color_discrete_sequence=['orange'], template='plotly_dark')
            plot_data.update_layout(title='Top 5 Most Expensive Products')
        elif selected_option == 'cheap':
            top_5_cheap = df.nsmallest(5, 'actual_price')
            top_5_cheap['Product_Name'] = top_5_cheap['product_name'].apply(lambda x: ' '.join(x.split()[:10]))
            plot_data = px.bar(top_5_cheap, x='Product_Name', y='actual_price',color_discrete_sequence=['orange'], template='plotly_dark')
            plot_data.update_layout(title='Top 5 Most Cheap Products')
        elif selected_option == 'pricediff':
            top_5_pricediff = df.nlargest(5, 'difference_price')
            top_5_pricediff['Product_Name'] = top_5_pricediff['product_name'].apply(lambda x: ' '.join(x.split()[:10]))
            plot_data = px.bar(top_5_pricediff, x='Product_Name', y='difference_price',color_discrete_sequence=['orange'], template='plotly_dark')
            plot_data.update_layout(title='Top 5 Products showing Largest Price Difference')
        elif selected_option == 'rated':
            top_5_rated = df.nlargest(5, 'rating')
            top_5_rated['Product_Name'] = top_5_rated['product_name'].apply(lambda x: ' '.join(x.split()[:10]))
            plot_data = px.bar(top_5_rated, x='Product_Name', y='rating',color_discrete_sequence=['orange'], template='plotly_dark')
            plot_data.update_layout(title='Top 5 Highly Rated Products')
        elif selected_option == 'popular':
            top_5_popular = df.nlargest(5, 'rating_count')
            top_5_popular['Product_Name'] = top_5_popular['product_name'].apply(lambda x: ' '.join(x.split()[:10]))
            plot_data = px.bar(top_5_popular, x='Product_Name', y='rating_count',color_discrete_sequence=['orange'], template='plotly_dark')
            plot_data.update_layout(title='Top 5 Popular Products')
        plot_div = plot_data.to_html(full_html=False)
        return render_template('visual.html', plot_div=plot_div)
    else:
        return render_template('visual.html')




if __name__ == '__main__':  
    app.run(debug = True)  