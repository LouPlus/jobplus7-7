import os
import json
import re
from faker import Faker
from random import randint
from jobplus.models import db, User, Job, Resume, Company, Deliver


fake = Faker()

path = os.path.join(os.path.dirname(__file__), '..', 'datas', 'job.json')
faker_data = json.load(open(path))


LENGTH = len(faker_data)

def fake_user():
    u = User(
        username = 'test',
        email = 'test@qq.com',
        password = '123123'
    )

    try:
        db.session.add(u)
        db.session.commit()
    except:
        db.session.rollback()

    user = User.query.filter_by(email=u.email).first_or_404()

    r = Resume(
        name = '薛' + u.username,
        degree = '本科',
        work_year = 5,
        phone = 19966668888,
        resume_url = 'https://github.com/louplus/jobplus7-7',
        user_id = user.id
    )

    db.session.add(r)
    db.session.commit()


def fake_companies():
    for i in range(0, LENGTH):
        company = faker_data[i]

        db_company = User.query.filter_by(username=company['name']).first()

        if db_company:
            continue

        c = User(
            username = company['name'],        
            email = 'shiyanlou_' + str(i + 1) + '@qq.com',
            role = 20
        )

        c.password = '123123'

        try:
            db.session.add(c)
        except:
            db.session.rollback()
            continue

        user = User.query.filter_by(email=c.email).first_or_404()

        welfare = ",".join(company['welfare'])

        d = Company(
            name = company['name'],
            logo = company['logo'],
            phone = '16699998888',
            website = 'shiyanlou.com',
            address = company['address'].split('：')[1],
            city = company['city'],
            staff_num = company['size'].split('：')[1],
            welfare = welfare, 
            industry = company['industry'],
            user_id = user.id
        )

        db.session.add(d)
        db.session.commit()


def fake_admin():
    admin = User(
        username = 'admin',
        email = 'admin@qq.com',
        password = '123123',
        role = 30
    )

    db.session.add(admin)
    db.session.commit()


def fake_jobs():
    companies = Company.query.all()

    for i in range(len(companies)):


        job = Job(
            name = faker_data[i]['job'], 
            salary = faker_data[i]['salary'], 
            work_year = faker_data[i]['work_year'], 
            degree = faker_data[i]['degree'], 
            company_id = companies[i].id 
        )

        db.session.add(job)
        db.session.commit()


def fake_deliver():
    user = User.query.filter_by(role=10).first_or_404()
    company = User.query.filter_by(role=20).first_or_404()
    job = Job.query.filter_by(company_id=company.id).first_or_404()

    d = Deliver(
        company_id = company.id,
        user_id = user.id,
        job_id = job.id
    )

    db.session.add(d)
    db.session.commit()

def run():
    fake_companies()
    fake_user()
    fake_admin()
    fake_jobs()
    fake_deliver()
