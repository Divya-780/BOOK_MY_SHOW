from flask import Flask,render_template,request,redirect,session,flash,url_for
from functools import wraps
from flask_mysqldb import MySQL
import mysql.connector
from werkzeug.utils import append_slash_redirect
from flask import make_response


mydatabase = mysql.connector.connect(
    host ='localhost', user ='root',
    passwd ='', database ='reg_details')


mycursor = mydatabase.cursor()

#There you can add home page and others. It is completely depends on you



app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='reg_details'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)



 
#Login
@app.route('/') 
@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("select * from reg_table where EMAIL=%s and UPASS=%s",(email,pwd))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data["UNAME"]
            flash('Login Successfully','success')
            return redirect('home')
        else:
            flash('Invalid credentials. Please Try Again','danger')
    return render_template("login.html")



#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap
  
#Registration  
@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("insert into reg_table(UNAME,UPASS,EMAIL) values(%s,%s,%s)",(name,pwd,email))
        mysql.connection.commit()
        cur.close()
        flash('Registration Successfully completed. Please Login Here...','success')
        return redirect('login')
    return render_template("reg.html",status=status)

#Home page
#@app.route('/')
@app.route('/home',methods=['GET','POST'])
@is_logged_in
def home():
    mycursor.execute('SELECT * FROM city_table')
    data = mycursor.fetchall()
    return render_template('home.html', output_data = data)


#vizag city
@app.route('/vizag',methods=['GET','POST'])
@is_logged_in
def vizag():
    mycursor.execute('SELECT * FROM theatres_list')
    item = mycursor.fetchall()
    return render_template('vizag.html', data_values = item)

'''@app.route('/movies',methods=['GET','POST'])
@is_logged_in
def movies():
    mycursor.execute('SELECT * FROM movies_list')
    data= mycursor.fetchall()
    return render_template('movies.html', output_data = data)'''

@app.route('/index')
@is_logged_in
def index():
    return render_template('index.html')

@app.route('/payment_index')
@is_logged_in
def payment_index():
    return render_template('payment_index.html')




#logout
@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))



@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=10'
    return response
    
if __name__=='__main__':
    app.secret_key='secret123'
    app.run(debug=True)


