'''
This file was written using flask documentation 
url:http://flask.pocoo.org/docs/1.0/
date: 9/23/2018
'''
import os
from ocr_pipeline import correctReceipt
from flask import Flask, flash, request, redirect, url_for
from flask import session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+'/upload_folder' #Directory to store files

ALLOWED_EXTENSIONS=set(['png','tif','jpg','gif']) #set of allowed file extensions


app=Flask(__name__)
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
	return '''
	<!doctype html>
	    <title>Receipt Scanner</title>
	    <h1>Uploading pictures</h1>
	    <form method=post enctype=multipart/form-data>
	      <input type=file name=file>
	      <input type=submit value=Upload>
	    </form>
	'''
@app.route('/getData',methods=['GET'])
def getData():
	app.logger.warn("Fetching data:")
	lastLines = session["receipt"]
	if lastLines is None:
		lastLines = ["No", "Receipts", "Scanned"]
	app.logger.warn(','.join(lastLines))
	return ','.join(lastLines)

if __name__ == '__main__':
	app.config['SESSION_TYPE'] = 'filesystem';
	app.debug = True;
	app.run()
