import time
import random
import logging
import json
import random
import settings
from datetime import datetime
from argparse import ArgumentParser, RawTextHelpFormatter

from flask import Flask, request, json
from flask_cors import CORS, cross_origin

import psycopg2

import threading

settings.api = Flask(__name__)
api = settings.api
CORS(api)

def parse_cmdline():
    parser = ArgumentParser(description=__doc__,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "dsn",
        help="database connection string\n\n"
             "For cockroach demo, use postgresql://<username>:<password>@<hostname>:<port>/bank?sslmode=require,\n"
             "with the username and password created in the demo cluster, and the hostname and port listed in the\n"
             "(sql/tcp) connection parameters of the demo cluster welcome message."
    )

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="print debug info")

    opt = parser.parse_args()
    return opt

opt = parse_cmdline()
logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
#conn = psycopg2.connect(opt.dsn)
conn = psycopg2.connect(
    host="34.75.115.219",
    database="postgres",
    user="postgres",
    password="cockroach123")
    
settings.global_conn = conn

import hydronizer_database as db
import hydronizer_mqtt as mqtt


########################################
# GET API for last water break
@api.route('/lastwaterbreak', methods=['GET'])

def get_last_water_break():
    device_id = request.args['deviceid']
    return db.get_last_entry(device_id)
########################################

########################################
# GET API for metrics
@api.route('/metrics', methods=['GET'])
def get_metrics():
    device_id = request.args['deviceid']
    return db.get_metrics_db(device_id)
########################################

########################################
# GET API for user timer
@api.route('/userTimer', methods=['GET'])
def get_user_timer():
    device_id = request.args['deviceid']
    return db.get_user_time(device_id)
########################################

########################################
# POST API for setting new time
@api.route('/postNewTime', methods=['POST'])
def update_user_timer():
    if not request.json or not 'device_id' in request.json or not 'device_name' in request.json or not 'new_time' in request.json:
        abort(400)
    device_id = request.json['device_id']
    device_name = request.json['device_name']
    new_time = request.json['new_time']
    return db.update_time(device_id, device_name, new_time)
########################################

if __name__ == "__main__":
    api.run()
    db.create_table_if_not_exist()
    db.create_table_if_not_exist()
    db.create_user_table_if_not_exist()
    