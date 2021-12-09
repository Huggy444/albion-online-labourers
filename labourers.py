#Imports
import requests
import ujson
import datetime
from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
import time
        
app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("halt_page"))

@app.route("/halted")
def halt_page():
    return render_template("halt.html")

if __name__ == "__main__":
    app.run()
