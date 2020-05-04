import os
from PIL import Image
from flask import Flask 
from flask import request, jsonify,render_template,send_from_directory

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def clean_static(target_path):
	for item in os.listdir(target_path):
		if item.endswith('.png'):
			os.remove(os.path.join(target_path, item))
def clean_image_folder(target_path):
	for item in os.listdir(target_path):
		os.remove(os.path.join(target_path, item))


def process_image(filename):
	img_location = './images/' + filename
	image_file = Image.open(img_location)
	image_file = image_file.convert('1')
	target_path = APP_ROOT + '/' + 'static'
	clean_static(target_path)
	out_filename = filename.replace('.','_')
	out_filename = out_filename + '_out.png'
	if not os.path.isdir(target_path):
		os.mkdir(target_path)

	dest = '/'.join([target_path,out_filename])
	image_file.save(dest)
	return out_filename



@app.route('/index', methods=['GET','POST'])
def index():
	if request.method == "POST":
		target = os.path.join(APP_ROOT, 'images/')
		clean_image_folder(target)
		print('TARGE: ', target)

		if not os.path.isdir(target):
			os.mkdir(target)

		f = request.files['file']
		filename = f.filename 
		destination = target+filename 
		f.save(destination)
		out_file = process_image(filename)
		print('Processed_image; ', out_file)
		## This to directly download the processed image
		# return send_from_directory("outputs", processed_image, as_attachment=True)	
		return render_template('complete.html',out=out_file)
	else:
		return render_template('index.html')



if __name__ == "__main__":
	app.run(debug=True)