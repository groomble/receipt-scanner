import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+'./upload_folder' #Directory to store files

ALLOWED_EXTENSIONS=set(['png','tif','jpg','gif']) #set of allowed file extensions

#### LEARN RELATIVE vs ABSOLUTE paths

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
	app.logger.warn('extension:\t'+filename.rsplit('.',1)[-1].lower());
	return '.'in filename and \
			filename.rsplit('.',1)[-1].lower() in ALLOWED_EXTENSIONS
@app.route('/',methods=['GET','POST'])

def upload_file():
	app.logger.warn('endpoint');
	if request.method=='POST': 
		app.logger.warn('is post');
		#check for file part for the post method
		if 'file' not in request.files:
			#return ('No file part')
			return redirect(request.url)
		file=request.files['file']
		#if the user doesn't select the file, the browser can 
		#submit an empty part without a filename
		if file.filename=='':
			#return ('No selected file')
			return redirect(request.url)
		app.logger.warn('is good filename');
		if file and allowed_file(file.filename):
			app.logger.warn('uploaded file');
			filename=secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
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
#def showfile():
if __name__ == '__main__':
	app.secret_key = 'aasdfsadfsadfsadf';
	app.config['SESSION_TYPE'] = 'filesystem';
	app.debug = True;
	app.run()
