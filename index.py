# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from flask_cors import *
from flask import Flask, render_template, jsonify, request, send_from_directory, request
from update import setScreenXls,readFile,getXlsList,setScreenXlsAsin,setScreenXlsa
import re,sys,os ,time
from flask import make_response


sys.path.append('bin/')
sys.path.append('db/')

from AsinTable import Add_Asin_dao ,find_Asin_dao ,findAll_Asin_dao,count_Asin_dao ,Remove_Asin_dao

app = Flask(__name__)





@app.route("/competitor", methods=['GET'])
def competitor_asin():
	asin=request.args.get("asin")
	return str([ asinItem for asinItem  in    getXlsList("File/st.xls")[0] if asinItem[0]==asin])


@app.route("/FindAll", methods=['GET'])
def FindAll():
	asin_type=request.args.get("asin_type")
	print (asin_type	)
	return  "".join([asin[0] for asin in findAll_Asin_dao(asin_type)])

@app.route("/FindAsin", methods=['GET'])
def FindAsin():
	asin=request.args.get("asin")
	rst = make_response( find_Asin_dao(asin))
	rst.headers['Access-Control-Allow-Origin'] = '*'
	return   rst, 201

@app.route("/g", methods=['GET', 'POST'])
def Game_console_asin():
	# asin=request.args.get("asin")
	nBB=str( [  asinItem for asinItem  in    getXlsList("File/asin.xls")[0]  ])
	fo =str([  asinItem for asinItem  in    getXlsList("File/asin.xls")[1]  ])
	l  =str([  asinItem for asinItem  in    getXlsList("File/asin.xls")[2] ])
	doge_Asin =str([  asinItem for asinItem  in    getXlsList("File/asin.xls")[3]  ])
	Normal_Asin=str([  asinItem for asinItem  in    getXlsList("File/asin.xls")[4]  ])
	return time.ctime(os.path.getmtime("File/asin.xls"))+" <br> Nobubox <br >"+nBB+ "<br ><br ><br ><br >  被跟卖<br >"+fo+"<br ><br ><br ><br ><br >  地评分asin<br >" +l+"<br ><br ><br ><br ><br >  变狗<br >" +doge_Asin+"<br ><br ><br ><br ><br >  正常asin<br >" +Normal_Asin+"<br ><br ><br ><br ><br >  未下库存<br >"+str([  asinItem for asinItem  in    getXlsList("File/asin.xls")[5]  ])
@app.route("/ADD_ASIN", methods=['GET', 'POST'])
def ADD_asin():
	if request.method == 'GET':
		return  render_template('index.html')
	ASINstr=request.form['asin_list']
	asin_type=request.form['asin_type']
	# print (asin_type)
	insertAsin= re.findall("B0.{8}",ASINstr)
	af=(count_Asin_dao())[0][0]
	# print (len(insertAsin))
	ret=(Add_Asin_dao(insertAsin,asin_type))[0][0]
	return "加入前"+str(af)+"  加入后 "+str(ret)


@app.route("/Del_Asin", methods=['POST'])
def Del_Asin():
	# if request.method == 'GET':
		# return  render_template('index.html')
	ASINstr=request.form['asin_list']
	# asin_type=request.form['asin_type']
	# print (asin_type)
	DeleteAsin= re.findall("B0.{8}",ASINstr)
	af=(count_Asin_dao())[0][0]
	# print (len(insertAsin))
	ret=(Remove_Asin_dao(DeleteAsin))[0][0]
	return "删除前"+str(af)+"  删除后 "+str(ret)



@app.route("/", methods=['GET', 'POST'])
def remove_asin():
	if request.method == 'GET':
		return  render_template('index.html')
	else:
		return getXlsList("File/asin.xls")

def run():

	app.run(host='0.0.0.0',port=5000, threaded=True)
	CORS(app, supports_credentials=True)


if __name__ == '__main__':
	run()