from app import db

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.String(10))
    warehouse_name = db.Column(db.String(120))

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(25),index=True, unique=True)
    product_name = db.Column(db.String(150))
    product_sku = db.Column(db.String(25))
    product_status = db.Column(db.String(10))
    # stok_hist = db.relationship('Stok', backref='itemdetail', lazy='dynamic')

class Credential(db.Model):
    __tablename__ = 'credential'
    id = db.Column(db.Integer, primary_key=True)
    appId = db.Column(db.String(50))
    clientId = db.Column(db.String(50))
    clientSecret= db.Column(db.String(50))
    clientBearer = db.Column(db.String(50))

class Stok(db.Model):
    __tablename__ = 'stok'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(25))
    item_qty = db.Column(db.Integer)
    stok_date = db.Column(db.Date)
    wh_id = db.Column(db.String(25))
    out_yda=db.Column(db.Integer)

class RedeemNP(db.Model):
    __tablename__ = 'redeemnp'
    id = db.Column(db.Integer, primary_key=True)
    nmuserid = db.Column(db.String(10))
    redeemitem = db.Column(db.String(50))
    reqdate = db.Column(db.Date)