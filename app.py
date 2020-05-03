import os
from PIL import Image
from flask import Flask 
from flask import request, jsonify,render_template

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def process_image(location):
	image_file = Image.open(location)
	image_file = image_file.convert('1')
	target_path = os.path.join(APP_ROOT, 'outputs/')
	print('TARGE: ', target_path)

	if not os.path.isdir(target_path):
		os.mkdir(target_path)
	dest = '/'.join([target_path, 'out.png'])
	image_file.save(dest)
	return dest

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	print('TARGE: ', target)

	if not os.path.isdir(target):
		os.mkdir(target)

	filenames = request.files.getlist('file')

	for file in filenames:
		print("FILE: ", file)
		filename = file.filename 
		destination = '/'.join([target, filename])
		print('Destination: ', destination)
		file.save(destination)
	processed_image = process_image(destination)
	return render_template('complete.html',process_image)







if __name__ == "__main__":
	app.run(debug=True)