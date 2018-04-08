from flask import Flask, Response, request, send_file

import warnings
warnings.filterwarnings('ignore')


import numpy as np
import pandas as pd
import math 
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier , GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn import tree
from sklearn import svm
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor


from sklearn.preprocessing import Imputer , Normalizer , scale
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV

import keras
from keras import backend as K


import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns

mpl.style.use( 'ggplot' )
sns.set_style( 'white' )
pylab.rcParams[ 'figure.figsize' ] = 8 , 6

app = Flask(__name__)

train = pd.read_csv("total.csv")
df = train

train2 = pd.read_csv("wholesale_price.csv")
df2 = train2


def get_graphs(state ,district , market):
	gp = df.loc[(df.state == state) & (df.district == district) & (df.market == market), : ]
	fig, axes = plt.subplots(5,1)
	fig.set_size_inches(20, 30)
	sns.barplot(data=gp ,y="modal_price",x="commodity", hue = "variety" ,orient="v" ,ax=axes[0] )
	sns.kdeplot(gp.modal_price , shade=True, color="r" , ax=axes[1] )
	sns.stripplot(x="commodity", y="modal_price", data=gp , hue = "variety" , jitter=True , ax = axes[2])
	sns.distplot(gp.modal_price , ax = axes[3])
	sns.pointplot(x="commodity", y="modal_price", data=gp , ax = axes[4] ) 
	fig.savefig("2.png") 
	
	
def get_val(state , district , commodity):
    temp = df.loc[(df.state == state) & (df.district == district) & (df.commodity == commodity), : ]
    fig, axes = plt.subplots(6,1)
    fig.set_size_inches(20, 30)
    sns.barplot(data=temp ,y="min_price",x="market" ,orient="v" , ax = axes[0])
    sns.pointplot(data=temp ,y="min_price",x="market" ,orient="v" , ax = axes[1])
    sns.barplot(data=temp ,y="modal_price",x="market" ,orient="v" , ax = axes[2])
    sns.pointplot(data=temp ,y="modal_price",x="market" ,orient="v" , ax = axes[3])
    sns.barplot(data=temp ,y="max_price",x="market" ,orient="v" , ax = axes[4])
    sns.pointplot(data=temp ,y="max_price",x="market" ,orient="v" , ax = axes[5])
    fig.savefig("3.png")         	   

	
def pairplot(state , district , market):
    gp = df.loc[(df.state == state) & (df.district == district) & (df.market == market), : ]
    g = sns.PairGrid(gp , hue = "variety")
    # g = g.map_diag(plt.hist)
    g = g.map_offdiag(plt.scatter)
    g = g.add_legend()
    g = plt.figure(figsize=(15,10))
    fig.savefig("4.png") 
	

@app.route('/describe', methods=['GET'] )
def describe():
	dataframe = df.describe()
	dataframe.to_csv('abc.csv',index = False)
	return send_file('abc.csv')
	
	
@app.route('/head', methods=['GET'] )
def head():
	dataframe = df.head()
	dataframe.to_csv('head.csv',index = False)
	return send_file('head.csv')
	
@app.route('/info', methods=['GET'] )
def info():
	state=request.args.get('state')
	district=request.args.get('district')
	market=request.args.get('market')
	gp = df.loc[(df.state == state) & (df.district == district) & (df.market == market), : ]
	#a = ""
	#for i in range(0 , gp.shape[0]):
	#	a = a + gp.commodity + "    " + gp.variety + "    " + gp.arrival_date + "    " + str(gp.min_price) + "    " + str(gp.max_price) + "    " + str(gp.modal_price) + "    "
	gp.to_csv( 'price_prediction.csv' , index = False )
	return send_file('price_prediction.csv')	
	
	
@app.route('/info1', methods=['GET'] )	
def info1():
	state=request.args.get('state')
	district=request.args.get('district')
	commodity=request.args.get('commodity')
	gp = df.loc[(df.state == state) & (df.district == district) & (df.commodity == commodity), : ]
	#a = ""
	#for i in range(0 , gp.shape[0]):
	#	a = a + gp.commodity + "    " + gp.variety + "    " + gp.arrival_date + "    " + str(gp.min_price) + "    " + str(gp.max_price) + "    " + str(gp.modal_price) + "    "
	gp.to_csv( 'price_prediction_com.csv' , index = False )
	return send_file('price_prediction_com.csv')	
	
	
	
@app.route('/heat_map', methods=['GET'] )
def heat_map():
	correlation_map = df[df.columns].corr()
	obj = np.array(correlation_map)
	obj[np.tril_indices_from(obj)] = False
	fig,ax= plt.subplots()
	fig.set_size_inches(15,10)
	sns.heatmap(correlation_map, mask=obj,vmax=.7, square=True,annot=True)
	fig.savefig("1.png")
	return send_file("1.png")
	

@app.route('/predictions', methods=['GET'] )
def predictions():
	Crop=request.args.get('crop')
	X = [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7]
	y = df2.loc[ df2.crop == Crop , "_2004_05" : "_2011_12" ].as_matrix()
	X = np.array(X)
	y = y.reshape(8 , 1)
	X = X.reshape(8 , 1)
	reg = svm.SVR(C=0.5 , epsilon=0.01)
	reg.fit(X , y ) 
	X_test = [8 , 9 , 10 , 11 , 12 , 13 , 14 , 15]
	X_test = np.array(X_test)
	pred = reg.predict(X_test.reshape(8 , 1))
	pred = pred.reshape(8 , 1)
	temp = y.reshape(8 , 1)
	rohit = []
	for i in temp:
		rohit.append(i)
	for i in pred:
		rohit.append(i)
	rohit = np.array(rohit)
	rohit = rohit.reshape(16,)
	Years = ["2004-05" , "2005-06" ,"2006-07", "2007-08" , "2008-09" , "2009-10" , "2010-11" , "2011-12" , "2012-13" , "2013-14" , "2014-15" , "2015-16" , "2016-17" , "2017-18" , "2018-19" , "2019-20" ]
	Years = np.array(Years)
	d = { "Years" : Years , "Prediction" : rohit }
	final = pd.DataFrame(d)
	fig, axes = plt.subplots(1,1)
	fig.set_size_inches(10, 5)
	sns.pointplot(data=final ,x = "Years" ,y = "Prediction", orient="v" )
	fig.savefig("5.png")
	final.to_csv( 'wholesale_price_prediction.csv' , index = False )
	return send_file('wholesale_price_prediction.csv')
	
	
@app.route('/get_graphs', methods=['GET'] )
def theta():
	state=request.args.get('state')
	district=request.args.get('district')
	market=request.args.get('market')
	get_graphs(state, district, market)
	return send_file("2.png")
	
	
@app.route('/get_val', methods=['GET'] )
def alpha():
	state=request.args.get('state')
	district=request.args.get('district')
	commodity=request.args.get('commodity')
	get_val(state, district, commodity)
	return send_file("3.png")
	
	
	
@app.route('/pairplot', methods=['GET'] )
def gamma():
	state=request.args.get('state')
	district=request.args.get('district')
	market=request.args.get('market')
	pairplot(state, district, 'market')
	return send_file("4.png")	
	


