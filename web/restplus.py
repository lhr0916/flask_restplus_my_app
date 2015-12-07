# -*- coding: utf-8 -*-

from flask import Flask, json, jsonify, render_template, request
from bson import json_util
from datetime import datetime
from urlparse import urlparse, parse_qs
from pymongo import MongoClient

from flask_restplus import Api, Resource, fields, swagger

app = Flask(__name__)
api = Api(app, version='1.0', title='My API',
          description='Flask-RestPlus 사용해보자',)

client = MongoClient("mongodb://t.com:27017")
db = client.mydb

ns = api.namespace('Member', description='MemberAPI')
@ns.route('/<string:name>')
@api.doc(params={'name':'member name'})
class Member(Resource):
    @app.route('/Member/<name>', methods=['POST'])
    def post(name):
        data = {
                "age":30,
                "name":name,
                "cdate": datetime.now()
            }
        db.member.insert(data)
        return name;


    @app.route('/Member/<name>')
    def get(name):
        data = json_util.dumps( db.member.find({
            'name': name }) )
        return render_template("user.html", users=json.loads(data) )


if __name__ == '__main__':
    port=8808
    is_debug = False
    app.run(debug=is_debug, host="0.0.0.0", port=port, threaded=True)

