import os
from PIL import Image
from flask import Flask 
from flask import request, jsonify,render_template,send_from_directory

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def process_image(filename):
	img_location = './images/' + filename
	image_file = Image.open(img_location)
	image_file = image_file.convert('1')
	target_path = APP_ROOT + '/' + 'outputs'
	print('TARGET: ', target_path)
	out_filename = filename.replace('.','_')
	out_filename = out_filename + '_out.png'
	if not os.path.isdir(target_path):
		os.mkdir(target_path)

	dest = '/'.join([target_path,out_filename])
	image_file.save(dest)
	print("OUTPUT IMAGE: ", dest)
	return 

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
	target = os.path.join(APP_ROOT, 'images/')
	print('TARGE: ', target)

	if not os.path.isdir(target):
		os.mkdir(target)

	f = request.files['file']
	filename = f.filename 
	destination = target+filename 
	f.save(destination)
	processed_image = process_image(filename)
	print("Destination: ", destination)
	## This to directly download the processed image
	# return send_from_directory("outputs", processed_image, as_attachment=True)
	return render_template('complete.html',out=filename)



if __name__ == "__main__":
	app.run(debug=True)