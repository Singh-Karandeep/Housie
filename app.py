from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from ticket_generator import HousieTicketGenerator

app = Flask(__name__, static_url_path='', 
			static_folder='web/static', 
			template_folder='web/templates')
CORS(app)


@app.route('/generate_tickets', methods=['POST'])
def generate_tickets():
	data = request.json.split('\n')
	print('Data Received : {}'.format(data))
	status, ticket_file_name = HousieTicketGenerator().main(data)
	print(status, ticket_file_name)
	return jsonify(status=status, ticket_file_name=ticket_file_name)


@app.route('/')
def flask_root():
	return render_template('index.html')


if __name__ == '__main__':
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True)
