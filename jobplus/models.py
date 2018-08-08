from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()

class Base(db.Model):
    # 不把这个类当作Model类
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY= 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    is_disable = db.Column(db.Boolean, default=False)

    company = db.relationship('Company', uselist=False)
    resume = db.relationship('Resume', uselist=False)


    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    phone = db.Column(db.String(11), index=True)
    degree = db.Column(db.String(32), index=True) 
    job = db.Column(db.String(64), index=True) 
    work_year = db.Column(db.SmallInteger, index=True) 
    resume_url = db.Column(db.String(256)) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', uselist=False)

    def __repr__(self):
        return '<Resume:{}>'.format(self.name)
        

class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    phone = db.Column(db.String(11), index=True)
    description = db.Column(db.String(128))
    logo = db.Column(db.String(128))
    website = db.Column(db.String(128))
    city = db.Column(db.String(64)) 
    staff_num = db.Column(db.String(64)) 
    industry = db.Column(db.String(64)) 
    address = db.Column(db.String(128))
    welfare = db.Column(db.String(128)) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', uselist=False)
    job = db.relationship('Job', uselist=True)

    def __repr__(self):
        return '<Company:{}>'.format(self.id)


class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    description = db.Column(db.String(128))
    degree = db.Column(db.String(32), index=True) 
    work_year = db.Column(db.String(32), index=True)
    tags = db.Column(db.String(128))
    salary = db.Column(db.String(20))
    is_disable = db.Column(db.Boolean, default=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)
