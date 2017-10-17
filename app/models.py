# from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
#
# #
# app=Flask(__name__)
# #
# app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:123456@192.168.56.102:3377/p2pbill"
# db=SQLAlchemy(app)

#平台信息表
class P2P(db.Model):
    __tablename__="p2p"
    def __init__(self,name,url,funds_deposit,risk_deposit):
        self.name=name
        self.url=url
        self.funds_deposit=funds_deposit
        self.risk_deposit=risk_deposit
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),unique=True) #平台名称
    url=db.Column(db.String(255),unique=True) #平台URL
    funds_deposit=db.Column(db.Boolean,default=False) #资金存管
    risk_deposit=db.Column(db.Boolean,default=False)  #风险金存管
    invests=db.relationship('Invest',backref="p2p") #投资记录外键关联关系
    userp2ps=db.relationship('UserP2P',backref="p2p")#用户平台外键关联关系
    billflow=db.relationship("BillFlow",backref="p2p") #资金流水外键关联关系


#用户信息表
class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(16),unique=True) #登录用户名
    password=db.Column(db.String(100)) #密码
    nickname=db.Column(db.String(32)) #昵称
    email=db.Column(db.String(32),unique=True) #邮箱
    phone=db.Column(db.String(11),unique=True) #手机
    face=db.Column(db.String(255)) #头像
    loginlogs=db.relationship("Loginlog",backref="user")
    bankcards=db.relationship("BankCard",backref="user")
    invest = db.relationship("Invest", backref="user")
    userp2p = db.relationship("UserP2P", backref="user")
    billflow = db.relationship("BillFlow", backref="user")
    def check_pwd(self,pwd):
        return check_password_hash(self.password,pwd)


#投资记录表
class Invest(db.Model):
    __tablename__="Invest"
    id=db.Column(db.Integer,primary_key=True)
    p2p_id=db.Column(db.Integer,db.ForeignKey('p2p.id')) #外键关联p2p
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    money=db.Column(db.Integer) #投资金额
    start_time=db.Column(db.DateTime)# 投资开始时间
    end_time=db.Column(db.DateTime)# 投资到期时间
    days=db.Column(db.Integer) #投资周期天数,可以不用手动填写
    profit=db.Column(db.Integer) #年利润
    lucre=db.Column(db.Integer)  #收益
    status=db.Column(db.Integer,default=0) #0投资中,1已到期,2已完成

#用户平台关联表
class UserP2P(db.Model):
    __tablename__="userp2p"
    def __init__(self,p2p_id,user_id,account,password,card_id,phone):
        self.p2p_id=p2p_id
        self.user_id=user_id
        self.account=account
        self.password=password
        self.card_id=card_id
        self.phone=phone
    id=db.Column(db.Integer,primary_key=True)
    p2p_id=db.Column(db.Integer,db.ForeignKey("p2p.id")) #外键关联p2p
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    account=db.Column(db.String(16))  #平台帐户
    password=db.Column(db.String(100))#平台密码
    card_id=db.Column(db.Integer,db.ForeignKey('bankcard.id')) #银行卡号
    phone=db.Column(db.String(11)) #手机号


#资金流水记录表
class BillFlow(db.Model):
    __tablename__="billflow"
    id=db.Column(db.Integer,primary_key=True)
    card_id=db.Column(db.Integer,db.ForeignKey("bankcard.id"))
    p2p_id=db.Column(db.Integer,db.ForeignKey("p2p.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    money=db.Column(db.Integer) #金额
    status=db.Column(db.Integer,default=0) #0进行中,1已完成
    type=db.Column(db.Integer) #0 充值，1 提现

#银行卡管理
class BankCard(db.Model):
    __tablename__="bankcard"
    def __init__(self,name,card,user_id):
        self.name=name
        self.card=card
        self.user_id=user_id
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32)) #开户行
    card=db.Column(db.String(25),unique=True) #银行卡号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    billflows=db.relationship('BillFlow',backref='bankcard')
    userp2ps=db.relationship('UserP2P',backref='bankcard')

#登录日志
class Loginlog(db.Model):
    __tablename__="loginlog"
    def __init__(self, user_id, ip):
        self.user_id=user_id
        self.ip=ip
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    ip=db.Column(db.String(15))
    addtime=db.Column(db.DateTime,default=datetime.now)


if __name__=="__main__":
    # pass
    db.create_all()
    user=User(username="admin",password=generate_password_hash("Qwe123123"),nickname="道可道",email="962584902@qq.com",phone="15821834763")
    db.session.add(user)
    db.session.commit()