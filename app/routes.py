from flask import render_template,redirect, url_for,request
from app import app,db,api
from app.models import Warehouse,Product,Credential,Stok
from datetime import date
from flask_restful import Resource
from sqlalchemy import create_engine
import pandas as pd
import json
import requests

class apiv1(Resource):
    def post(self):
        if request.args.get('data')=="token":
            if request.args.get('secretkey')==app.config['SECRET_KEY']:
                cred=Credential.query.get(1)
                cred.clientBearer=request.args.get('newtoken')
                db.session.add(cred)
                db.session.commit()
                return {'status':'token updated'}
            else:
                return {'status':'wrong secret key'}
        elif request.args.get('data')=="prod":
            print(request.args.get('id'))
            prod=Product.query.filter_by(product_id=request.args.get('id')).first()
            print(prod.id)
            prod.product_name=request.args.get('prodname')
            db.session.add(prod)
            db.session.commit()
            return {'status':'prod name added'}
        else:
            id=request.args.get('id')
            qty=request.args.get('qty')
            wh=request.args.get('wh')
            print(id)
            print(qty)
            newdata=Stok(item_id=id,item_qty=qty,stok_date=date.today(),wh_id=wh)
            db.session.add(newdata)
            db.session.commit()
            return {'status':'added stok'}
    def get(self):
        if request.args.get('data')=="product":
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            df = pd.read_sql_query("SELECT * FROM product", con=engine)
            engine.dispose()
            df=df.to_json(orient='records')
            df=json.loads(df)
            return (df)
        elif (request.args.get('data')=="credentials"):
            if request.args.get('secretkey')==app.config['SECRET_KEY']:
                engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
                df = pd.read_sql_query("SELECT * FROM credential", con=engine)
                engine.dispose()
                df=df.to_json(orient='records')
                df=json.loads(df)
                return (df)
            else:
                return {'status':'wrong secret key'}
        else:
            print(request.args.get('id'))
            if request.args.get('id'):
                engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
                df = pd.read_sql_query("SELECT * FROM warehouse WHERE warehouse_id = {}".format(request.args.get('id')), con=engine)
                engine.dispose()
                df=df.to_json(orient='records')
                df=json.loads(df)
                return (df[0]['warehouse_name'])
            else:
                engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
                df = pd.read_sql_query("SELECT * FROM warehouse", con=engine)
                engine.dispose()
                df=df.to_json(orient='records')
                df=json.loads(df)
                return (df)
        
api.add_resource(apiv1,'/apiv1')

@app.route('/')
def index():
    return redirect(url_for('stokhist'))

@app.route('/<id>')
def dash(id):
    df=Stok.query.filter_by(item_id=id).all()
    wh=[x.wh_id for x in df]
    whnew=list(set(wh))
    x=[x.stok_date.strftime('%Y/%m/%d') for x in df]
    xnew=list(set(x))
    xnew.sort()
    # print(whnew)
    # print([{'label':requests.get("{0}/apiv1?id={1}".format(app.config['ENV_URL'],wh)).json(),'data':[x.item_qty for x in df if x.wh_id==wh]} for wh in whnew])
    # y=[{'label':wh,'data':[x.item_qty for x in df if x.wh_id==wh]} for wh in whnew]
    y=[{'label':requests.get("{0}/apiv1?id={1}".format(app.config['ENV_URL'],wh)).json(),'data':[x.item_qty for x in df if x.wh_id==wh]} for wh in whnew]
    return render_template('dash.html',x=xnew,y=y)

@app.route('/stokhist')
def stokhist():
    df=Stok.query.all()
    return render_template('stokhist.html',df=df)

@app.route('/delstokhist/<id>')
def delstokhist(id):
    itemdel=Stok.query.get(id)
    db.session.delete(itemdel)
    db.session.commit()
    return redirect(url_for('stokhist'))

@app.route('/wh', methods=['GET', 'POST'])
def wh():
    df=Warehouse.query.all()
    if request.method=='POST':
        NewWh=Warehouse(warehouse_id=request.form['InpWhId'],warehouse_name=request.form['InpWhName'])
        db.session.add(NewWh)
        db.session.commit()
        return redirect(url_for('wh'))
    else:        
        return render_template('wh.html',df=df)
    
@app.route('/delwh/<id>', methods=['GET', 'POST'])
def delwh(id):
    itemdel=Warehouse.query.get(id)
    db.session.delete(itemdel)
    db.session.commit()
    return redirect(url_for('wh'))
    
@app.route('/product', methods=['GET', 'POST'])
def prod():
    df=Product.query.all()
    if request.method=='POST':
        NewProd=Product(product_id=request.form['InpProdId'],product_status="Active")
        db.session.add(NewProd)
        db.session.commit()
        return redirect(url_for('prod'))
    else:        
        return render_template('product.html',df=df)
    
@app.route('/cred', methods=['GET', 'POST'])
def cred():
    df=Credential.query.get(1)
    if request.method=='POST':
        if request.form['action']=="Add Credential":
            NewCred=Credential(appId=request.form['InpAppId'],
                               clientId=request.form['InpClientId'],
                               clientSecret=request.form['InpClientSecret'],
                               clientBearer=request.form['InpClientBearer'])
            db.session.add(NewCred)
            db.session.commit()
            return redirect(url_for('cred'))
        else:
            df.appId=request.form['InpAppId']
            df.clientId=request.form['InpClientId']
            df.clientSecret=request.form['InpClientSecret']
            df.clientBearer=request.form['InpClientBearer']
            db.session.add(df)
            db.session.commit()
            # credential.query.all()
            return redirect(url_for('cred'))
    else:        
        return render_template('credential.html',df=df)