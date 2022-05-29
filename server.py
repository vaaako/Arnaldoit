import os
from flask import Flask, request, render_template, g, redirect, abort
from werkzeug.utils import secure_filename

from datetime import datetime
from random import randint
from database import query_db, create_post

"""
-> Like?
-> Warning when textarea is empty
-> Warning when image isn't on a right extension
"""

"""
export FLASK_APP=server.py
python3 -m flask run --host=0.0.0.0
"""

"""
=> cat schema.sql | arnaldata.db
INSERT INTO posts(id, data, content) VALUES (1, '2022-05-17', 'Hello, world!');
"""

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webm', 'gif', 'mp4'])

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = './static/uploads'

@app.before_request
def block_method():
	# ip = request.environ.get('REMOTE_ADDR')
	ip = request.access_route[0]
	print("%s entrou" %(ip))


# Home
@app.route('/')
def index():
	"""
		post[0] = id
		post[1] = date
		post[2] = content
		post[3] = filename
	"""
	posts = query_db('SELECT * FROM posts;')
	posts.reverse() # Invertendo lista para posts mais recentes aparecerem primeiro, dava pra fazer isso usando {{post[5] | reverse}}

	return render_template('index.html', posts=posts)

@app.route('/', methods=['POST'])
def post():
	ip = request.access_route[0]
	filename = upload_image(request.files['image'])
	
	id = None
	# id = create_user_id()  # Id do usuario

	content = request.form.get('content')
	if content=='' or content.isspace(): # If content is empty
		return ('', 204) # Do nothing
	else:
		post = (id, datetime.now().strftime("%d/%m/%y(%a)%H:%M:%S"), content, filename)
		create_post(post) # Create Post
		print("====== %s - Fez um post ======" %(ip)) # Create post
		return redirect('/', code=302) # Redirect to home

# Erros
@app.errorhandler(400)
def bad_req(e):
    return '<h2>Erro 400<h2><br> Bad Request', 400

@app.errorhandler(404)
def page_not_found(e):
    return '<h2>Erro 404<h2><br> Depois eu mudo essa página', 404

@app.errorhandler(500)
def application_error(e):
    return "Erro 500 <br> Something wrong happend <br><br> %s" %(e), 500


# UPLOAD IMAGES ⬇️
def allowed_file(filename):
	return str('.') in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(image):
	if len(image.filename)<=0 or not (image and allowed_file(image.filename)): # If don't have image or isn't on a right extension
		return None
	filename = secure_filename(image.filename).lower().rsplit(".", 1) # Filename + extension

	newfilename = '%s-%s.%s' %(filename[0], uniqName(), filename[1]) # Assembly filename-timestmap.extension
	image.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename)) # Save

	return newfilename

def uniqName():
	rn = str(randint(1, 99999))
	uniq = str(datetime.now().timestamp()).split('.')[0] # Get timestamp and remove milliseconds
	uniq_filename = '%s-%s' %(uniq, rn)
	return uniq

if __name__ == "__main__":
    app.run(host="0.0.0.0")
