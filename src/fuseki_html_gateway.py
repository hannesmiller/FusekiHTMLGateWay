from flask import Flask, request as flask_request
from json2html import *
import requests
import json
from io import StringIO

app = Flask(__name__)

fuseki_endpoint = 'http://localhost:3030/db/query'

@app.route('/sytek/db/query', methods = ["POST"])
def query_gateway():
    query = flask_request.form['query']
    # Forward the Query Fuseki and return the result
    response = requests.post(fuseki_endpoint, data = {'query': query})
    return custom_json_to_table_converter(response.text)

def json_to_table_converter(data):
    return json2html.convert(json = data)

def custom_json_to_table_converter(data):
    jsonObject = json.loads(data)
    with StringIO() as output:
        # Semantic tags
        output.write("<!DOCTYPE html>")
        output.write("<html>")
        output.write("<head>")
        output.write("<style>")
        output.write("table, th, td {")
        output.write("  border: 1px solid black;")
        output.write("  padding: 5px;")
        output.write("}")
        output.write("table {")
        output.write("  border-spacing: 15px;")
        output.write("}")
        output.write("</style>")
        output.write("</head>")
        # First print out the headers in the table
        output.write("<table>")
        output.write("<tr>")
        for header in jsonObject["head"]["vars"]:
            output.write(f"<th>{header}</th>")
        output.write("</tr>")
        # Next print out the data in the table
        for binding in jsonObject["results"]["bindings"]:
            output.write("<tr>")
            for column in jsonObject["head"]["vars"]:
                output.write(f"<td>{binding[column]['value']}</td>")
            output.write("</tr>")
        # End table
        output.write("</table>")
        output.write("</html>")

        return output.getvalue()

if __name__ == '__main__':
    app.run()