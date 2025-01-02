from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import pymongo
import os
import urllib.parse
import configparser



app = Flask(__name__)
title = "SMZDM sample application with Flask and MongoDB"
heading = "SMZDM  with Flask and MongoDB"
# mongodb
cf = configparser.ConfigParser()
cf.read('config.ini')
user = cf.get('db', 'user')
passwd = cf.get('db', 'passwd')
ip = cf.get('db','ip')
mydb = cf.get('db','db')
uri = 'mongodb://' + user + ':' + urllib.parse.quote_plus(passwd) + '@' + ip + '/' + mydb

client = MongoClient(uri)
# client = MongoClient("mongodb://neotest:M%40t0id!%40#$@124.156.148.21:27017/test") #host uri
# client = MongoClient("mongodb://neolee:matoid123@cluster0-shard-00-00-amlxb.gcp.mongodb.net:27017,cluster0-shard-00-01-amlxb.gcp.mongodb.net:27017,cluster0-shard-00-02-amlxb.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority") #host uri
db = client.test    #Select the database
smzdms = db.smzdm #Select the collection name
smzdms_item = db.smzdm_item 

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

# @app.route("/list")
# def lists ():
# 	#Display the all Tasks
# 	todos_l = todos.find()
# 	a1="active"
# 	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
# @app.route("/uncompleted")
def lists ():
	#Display the Uncompleted Tasks
	smzdms_l = smzdms_item.find(sort=[("name",pymongo.DESCENDING)])
	# a2="active"
	return render_template('index2.html',smzdms=smzdms_l,t=title,h=heading)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	keyword=request.values.get("keyword")
	desc=request.values.get("desc")
	desire_price=request.values.get("desire_price")
	# smzdms_item.insert_one({ "name":name, "keyword":keyword, "desc":desc, "desire_price":desire_price})
	smzdms_item.update_one({"keyword":keyword}, {'$set':{ "name":name, "desc":desc, "desire_price":desire_price}}, upsert=True)
	return redirect("/")

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	keyword=request.values.get("keyword")
	desc=request.values.get("desc")
	desire_price=request.values.get("desire_price")
	id=request.values.get("_id")
	smzdms_item.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "keyword":keyword, "desire_price":desire_price}}, upsert=True)
	return redirect("/")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	smzdms_item.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	smzdms_l=smzdms_item.find({"_id":ObjectId(id)})
	return render_template('update.html',smzdms=smzdms_l,t=title,h=heading)

@app.route("/<ITEM>")
# @app.route("/uncompleted")
def lists_1 (ITEM):
	#Display the Uncompleted Tasks
	smzdms_l = smzdms.find({'Item':ITEM}, sort=[("url",pymongo.DESCENDING)])
	# a2="active"
	return render_template('item.html',smzdms=smzdms_l,t=title,h=heading)

# @app.route("/completed")
# def completed ():
# 	#Display the Completed Tasks
# 	todos_l = todos.find({"done":"yes"})
# 	a3="active"
# 	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

# @app.route("/done")
# def done ():
# 	#Done-or-not ICON
# 	id=request.values.get("_id")
# 	task=todos.find({"_id":ObjectId(id)})
# 	if(task[0]["done"]=="yes"):
# 		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
# 	else:
# 		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
# 	redir=redirect_url()	

# 	return redirect(redir)

# @app.route("/action", methods=['POST'])
# def action ():
# 	#Adding a Task
# 	name=request.values.get("name")
# 	desc=request.values.get("desc")
# 	date=request.values.get("date")
# 	pr=request.values.get("pr")
# 	todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
# 	return redirect("/list")





# @app.route("/search", methods=['GET'])
# def search():
# 	#Searching a Task with various references

# 	key=request.values.get("key")
# 	refer=request.values.get("refer")
# 	if(key=="_id"):
# 		todos_l = todos.find({refer:ObjectId(key)})
# 	else:
# 		todos_l = todos.find({refer:key})
# 	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()
