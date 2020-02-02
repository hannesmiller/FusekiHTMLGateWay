# A Gateway Server for SPARQL Fuseki Server

A Python application using Flask to register a HTTP POST endpoint for SPARQL queries, the query in turn is sent to a Fuseki Server whose results are then transformed into a HTML table via Jinja2 template.


## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python fuseki_html_gateway.py 
```