from werkzeug.security import generate_password_hash, check_password_hash

from App.ModelUtil import BaseModel
from App.ext import db


class Letter(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    letter = db.Column(db.String(1), unique=True)

    # 作为print
    # def __str__(self):
    #     return self.letter
    #
    # # 和str一样，python2中使用的
    # def __unicode__(self):
    #     return self.letter
    # 给机器看的
    def __repr__(self):
        return self.letter


class City(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    regionName = db.Column(db.String(16))

    cityCode = db.Column(db.Integer, default=0)

    pinYin = db.Column(db.String(64))

    c_letter = db.Column(db.Integer, db.ForeignKey(Letter.id))


"""
insert into movies(id, showname, shownameen, director, leadingRole, type, country, language, duration,
 screeningmodel, openday, backgroundpicture, flag, isdelete) values(228830,"梭哈人生","The Drifting Red Balloon",
 "郑来志","谭佑铭,施予斐,赵韩樱子,孟智超,李林轩","剧情,爱情,喜剧","中国大陆","汉语普通话",90,"4D",date("2018-01-30 00:00:00"),
 "i1/TB19_XCoLDH8KJjy1XcXXcpdXXa_.jpg",1,0);
"""


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    showname = db.Column(db.String(32))
    shownameen = db.Column(db.String(128))
    director = db.Column(db.String(32))
    leadingRole = db.Column(db.String(256))
    type = db.Column(db.String(64))
    country = db.Column(db.String(32))
    language = db.Column(db.String(32))
    duration = db.Column(db.Integer)
    screeningmodel = db.Column(db.String(16))
    openday = db.Column(db.DateTime)
    backgroundpicture = db.Column(db.String(256))
    flag = db.Column(db.Integer)
    isdelete = db.Column(db.Boolean)


"""
insert into cinemas(name,city,district,address,phone,score,hallnum,servicecharge,astrict,flag,isdelete)
 values("深圳戏院影城","深圳","罗湖","罗湖区新园路1号东门步行街西口","0755-82175808",9.7,9,1.2,20,1,0);
"""


class Cinemas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    city = db.Column(db.String(16))
    district = db.Column(db.String(16))
    address = db.Column(db.String(256))
    phone = db.Column(db.String(32))
    score = db.Column(db.Float)
    hallnum = db.Column(db.Integer)
    servicecharge = db.Column(db.Float)
    astrict = db.Column(db.Integer)
    flag = db.Column(db.Integer)
    isdelete = db.Column(db.Boolean, default=False)


PERMISSION_ORDERED = 1
PERMISSION_DELETE = 2
PERMISSION_MODIFICATION = 4


class User(BaseModel, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(16), unique=True)
    u_email = db.Column(db.String(64), unique=True)
    u_password = db.Column(db.String(256))
    is_activate = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)
    u_permission = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.u_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.u_password, password)


    def check_permission(self, permission):
        return self.u_permission & permission == permission
    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()