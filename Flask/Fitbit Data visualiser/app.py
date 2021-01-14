#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 20:24:55 2021

@author: aida
"""


from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('pandas_protiling_report_IOT.html')
if __name__ == '__main__':
    app.debug = True
    app.run()
   