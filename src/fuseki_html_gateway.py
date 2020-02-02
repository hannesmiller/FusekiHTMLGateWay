from flask import Flask, request as flask_request
from json2html import *
import requests
import json
import os
from io import StringIO
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# Get APP json config
with open(f"{os.path.dirname(__file__)}/config.json") as json_file:
    config = json.load(json_file)

# Load up jinja template
file_loader = FileSystemLoader(os.path.dirname(__file__))
env = Environment(loader=file_loader)
jsonToHtmlTemplate = env.get_template(config['jsonToHtmlTemplate'])

@app.route(config['query_endpoint'], methods = ["POST"])
def query_gateway():
    # Extract the query param from POST message
    query = flask_request.form['query']
    # Forward the Query Fuseki and return the result
    response = requests.post(config['fuseki_query_api'], data = {'query': query})
    return jinja2_json_to_table_converter(response.text)

def jinja2_json_to_table_converter(data):
    jsonObject = json.loads(data)
    return jsonToHtmlTemplate.render(jsonObject=jsonObject)

def json_to_table_converter(data):
    return json2html.convert(json = data)

if __name__ == '__main__':
    app.run()