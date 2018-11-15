'''
This file was written using flask documentation 
url:http://flask.pocoo.org/docs/1.0/
date: 9/23/2018
'''
import os
from flask import Flask, flash, request,render_template,url_for,redirect,session
from ocr_pipeline import correctReceipt
from flask import Flask, flash, request, redirect, url_for
from flask import session
from werkzeug.utils import secure_filename
from wtforms import Form 
from passlib.hash import sha256_crypt
import jaydebeapi
from h2connect import connection

UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+'/upload_folder' #Directory to store files

ALLOWED_EXTENSIONS=set(['png','tif','jpg','gif']) #set of allowed file extensions


app=Flask(__name__, template_folder='../frontEnd')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key = ';lkjasf;ieawnaxnu213';


def allowed_file(filename):
	app.logger.warn('extension:\t'+filename.rsplit('.',1)[-1].lower());
	return '.'in filename and \
			filename.rsplit('.',1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/submitphoto',methods=['GET','POST'])
def upload_file():
	app.logger.warn('endpoint');
	if request.method=='POST': 
		app.logger.warn('is post');
		#check for file part for the post method
		if 'photo' not in request.files:
			app.logger.warn("no INPUT file");
			return redirect(request.url);
		file=request.files['photo']
		#if the user doesn't select the file, the browser can 
		#submit an empty part without a filename
		if file.filename=='':
			app.logger.warn("no INPUT filename");
			return redirect(request.url);
		app.logger.warn('is good filename');
		if file and allowed_file(file.filename):
			app.logger.warn('uploaded file');
			filename=secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
			file.save(filepath)
			lastLines = correctReceipt(filepath)
			lastLines = [l.replace(' ',',').replace('\n',',') for l in lastLines]
			session["receipt"] = lastLines
			app.logger.warn(lastLines)
			return redirect(url_for('upload_file',filename=filename))
	'''
	return 
	<!doctype html>
	    <title>Receipt Scanner</title>
	    <h1>Uploading pictures</h1>
	    <form method=post enctype=multipart/form-data>
	      <input type=file name=file>
	      <input type=submit value=Upload>
	    </form>
	'''
	return redirect(url_for('uploadImages.html'))
@app.route('/home',methods=['POST','GET'])
def index():
	return
				'''<!DOCTYPE html>
				<html>
				<body>

				<h2>Sign up</h2>
				<form action="/signup" method="post">
				  <fieldset>
				    <legend>Sign up</legend>
				    Username:<br>
				    <input type="text" name="username" value="username">
				    <br>
				    Email:<br>
				    <input type="text" name="email" value="email">
				    <br>
				    Password:<br>
				    <input type="password" name="password" value="username">
				    <br><br>
				    <input type="submit" value="Submit">
				  </fieldset>
				</form>

				</body>
				</html>'''
	return redirect(url_for(inde))

@app.route('/signup',methods=['POST','GET'])
def signup():
	'''if request.method=='GET':
		Connect to the database
		username=request.form.get('username')
		email=request.form.get('email')
		password=request.form.get('password')
		confirm=request.form.get('repeatPassword')
	return render_template("signup.html")'''
	try: 
		#return("OKAY")
		if request.method=="POST":
			username=request.form['username']
			password= sha256_crypt.encrypt(str(request.form['password']))
			email=request.form['email']
			cursor,con=connection()
			x=cursor.execute("SELECT USERNAME FROM REGISTRATION where USERNAME = %s", username)
			if int(len(x))>0:
				flash("That name is taken please try again")
				return redirect()
				'''return 
						<!DOCTYPE html>
						<html>
						<body>

						<h2>Sign up</h2>
						<form action="/signup" method="post">
						  <fieldset>
						    <legend>Sign up</legend>
						    Username:<br>
						    <input type="text" name="username" value="username">
						    <br>
						    Email:<br>
						    <input type="text" name="username" value="email">
						    <br>
						    Password:<br>
						    <input type="password" name="password" value="username">
						    <br><br>
						    <input type="submit" value="Submit">
						  </fieldset>
						</form>
						</body>
						</html>'''
			else:
				cursor.execute("INSERT INTO REGISTRATION (USERNAME,EMAIL,PASSWORD) VALUES (%S,%S,%S)", username,password,email)
				con.commit()
				flash("Thank you registering")
				cursor.close()
				con.close()
				session['logged_in']=True
				session['username']=username
				return redirect(url_for('login')) #in our case it would be the main.html page
	except Exception as e:
		return(str(e))

@app.route('/login', methods=['POST','GET'])
def login():
	if request.method=='GET':
		username=request.form.get('username') #accessing the data inside
		password= sha256_crypt.encrypt(str(request.form.get('password')))
		return redirect(url_for('index'))
	return redirect('index')
	'''
	return(redirect('/../index.hmtl'))'''

#def showfile():
@app.route('/getData',methods=['GET'])
def getData():
	app.logger.warn("Fetching data:")
	lastLines = session["receipt"]
	if lastLines is None:
		lastLines = ["No", "Receipts", "Scanned"]
	app.logger.warn(','.join(lastLines))
	return ','.join(lastLines)
'''@app.route('/login',methods=['GET'])
def dummyLogin():
    return redirect('/../uploadImages.html')'''
if __name__ == '__main__':
	app.config['SESSION_TYPE'] = 'filesystem';
	app.debug = True;
	app.run()
