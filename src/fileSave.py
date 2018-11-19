'''
This file was written using flask documentation 
url:http://flask.pocoo.org/docs/1.0/
date: 9/23/2018
'''
import os
from flask import (Flask,g, flash, request,render_template,url_for,redirect,session,url_for)
from ocr_pipeline import correctReceipt
from flask import Flask, flash, request, redirect, url_for
from flask import session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from dbConnect import databaseConnect

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
	return redirect(url_for('uploadImages.html'))
@app.route('/home',methods=['POST','GET'])
def index():
	return redirect(url_for('index.html'))

@app.route('/signup',methods=['POST','GET'])
def register():
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		email=request.form['email']
		db=databaseConnect('receipt-scanner-users.db')
		error=None
		if not username:
			error='username must be filled'
			app.logger.warn(error)
		elif not password:
			error='password must be filled'
			app.logger.warn(error)
		elif not email:
			error='Email must be filled'
			app.logger.warn(error)
		elif db.execute('SELECT id from user WHERE username = ?',(username,)).fetchone() is not None: 
			error= 'That user is already registered, try another'
			app.logger.warn(error)
		if error is None:
			'''If there's no error then the username is available'''
			db.execute('INSERT INTO user (username,password,email) VALUES (?,?,?)',(username,generate_password_hash(password),email))
			db.commit()
			db.close()
			#return render_template('uploadImages.html')
			return render_template('uploadImages.html')
		app.logger.warn(error)
	return render_template('signup.html')
@app.route('/login', methods=['POST','GET'])
def login():
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		db=db=databaseConnect('receipt-scanner-users.db')
		error=None
		user=db.execute('SELECT * FROM user WHERE username =?',(username,)).fetchone()
		if user is None:
			error='Incorect username'
			app.logger.warn(error)
		elif not check_password_hash(user['password'],password):
			error='Incorect password'
			app.logger.warn(error)
		if error is None:
			session.clear()
			session['user_id']= user['id']
			app.logger.warn("You managed to login")
			return render_template('stats.html')
		flash(error)
	return render_template('index.html')

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
