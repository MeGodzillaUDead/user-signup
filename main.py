from flask import Flask, request, redirect, render_template
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
	return "Under Construction..."
	
app.run()
