#!/usr/bin/env python
# encoding: utf-8

'''
Created on Jul 18, 2016

@author: Yusuke Kawatsu.
'''

# built-in modules.
pass

# installed modules.
from flask import Flask
from flask import request
from flask import jsonify
from flask_autodoc.autodoc import Autodoc

# my modules.
pass


# flask app.
app = Flask(__name__, static_path=u'/static', static_folder=u'./static')
app.debug = True
auto = Autodoc(app)

# on memory database.
_comments = []


@auto.doc()
@app.route('/', methods=['GET'])
def index():
    '''
    index page.
    '''
    # index.htmlを返す. Jinja2でrenderingはしない.
    return app.send_static_file(u'html/index.html')

@auto.doc()
@app.route('/apis/comments', methods=['GET'])
def get_comments():
    '''
    get comments.
    '''
    return jsonify(comments=_comments)

@auto.doc()
@app.route('/apis/comments', methods=['POST'])
def post_comments():
    '''
    post a comment.
    '''
    _comments.append(request.json)

    return jsonify(request.json)


if __name__ == '__main__':
    # :see: http://askubuntu.com/questions/224392/how-to-allow-remote-connections-to-flask
    app.run(host='0.0.0.0', port=5000, threaded=True)
