import json
import csv
import logging
import asyncio
from flask import Flask, jsonify, render_template, request
import sys
from io import StringIO

from aclient import Client
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
app = Flask(__name__)
event_loop = asyncio.get_event_loop()

class FileParser:
	def __init__(self, file):
		self.file=file
	def parse(self):
		data = self.file.read().decode('utf-8')
		print(data, file=sys.stderr)
		reader = csv.reader(StringIO(data))
		header = next(reader)
		data = list([r for r in reader])
		return {
			"data": data,
			"headers": header
		}

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/upload', methods=['POST'])
def handle_upload():
	print(request.files['file'], file=sys.stderr)
	parser = FileParser(request.files['file'])
	return jsonify(parser.parse())

@app.route('/translate', methods=['POST'])
def translate():
	urls = request.json['urls']
	event_loop = asyncio.new_event_loop()
	asyncio.set_event_loop(event_loop)
	client = Client()
	responses = event_loop.run_until_complete(
		asyncio.gather(
			*[client.get_url.async(x) for x in urls]
		)
	)
	results= list(map(len, responses))
	print("results", results, file=sys.stderr)
	return jsonify(results)

@app.route('/default_data')
def get_data():
	data = [
		['Google', 'http://google.com', 12344]
	]
	headers = ['Name', 'URL', 'Expected Length']

	return jsonify({
		"data":data,
		"headers":headers
	})


if __name__=='__main__':
	app.run(debug=True)