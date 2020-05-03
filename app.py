import os
from flask import Flask 
from flask import request, jsonify,render_template

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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

	return render_template('complete.html')







if __name__ == "__main__":
	app.run(debug=True)