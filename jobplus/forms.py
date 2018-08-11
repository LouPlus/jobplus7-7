from flask_wtf import FlaskForm
from flask_login import login_required, current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, SelectField
from wtforms.validators import Length, Email, EqualTo, Required
from jobplus.models import db, User, Resume, Company, Job

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住')
    submit = SubmitField('登录')
    
    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('请输入正确的密码')


class RegisterForm(FlaskForm):
    name = StringField('用户名', validators=[Required(), Length(2, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    confirm_password = PasswordField('确认密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')


    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')
    def create_user(self):
        user = User()
        user.username = self.name.data
        user.email = self.email.data
        user.password = self.password.data

        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

        u = User.query.filter_by(email=user.email).first()
        self.create_resume(u)
        return user

    def create_company(self):
        user = User()
        user.username = self.name.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = User.ROLE_COMPANY 

        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

        u = User.query.filter_by(email=user.email).first()
        self.create_table_company(u)

        return user

    def create_resume(self, user):
        resume = Resume()
        resume.user_id = user.id
        db.session.add(resume)
        db.session.commit()

    def create_table_company(self, user):
        print(user)
        company = Company()
        company.user_id = user.id
        company.name = user.username
        db.session.add(company)
        db.session.commit()


class UserProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(2, 24)])
    phone = StringField('电话')
    work_year = StringField('工作年限') 
    degree = StringField('学历') 
    resume_url = StringField('简历') 
    submit = SubmitField('提交')

    def validate_phone(self, field):
        if field.data:
            phone = field.data
            if phone[:2] not in ['13', '15', '18'] or len(phone) != 11:
                raise ValidationError('请输入有效的手机号码')

    def update_resume(self, user):
        if user.resume:
            resume = user.resume
        else:
            resume = Resume()
            resume.user_id = user.id

        self.populate_obj(resume)
        db.session.add(resume)
        db.session.commit()
        return resume


class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称', validators=[Length(2, 24)])
    phone = StringField('电话')
    description = StringField('一句话描述') 
    logo = StringField('Logo') 
    website = StringField('网站') 
    city = StringField('城市') 
    staff_num = StringField('公司规模') 
    industry = StringField('行业 (多个用/ 隔开)') 
    welfare = StringField('公司福利 (多个用, 隔开)')
    address = StringField('公司地址') 
    submit = SubmitField('提交')


    def validate_phone(self, field):
        if field.data:
            phone = field.data
            if phone[:2] not in ['13', '15', '18'] or len(phone) != 11:
                raise ValidationError('请输入有效的手机号码')

    def validate_name(self, f):
        c = Company.query.filter_by(name=f.data).first()
        if current_user.company: 
            if c and c != current_user.company:
                raise ValidationError('该公司名已经存在')


    def update_company(self, user):
        if user.company:
            company = user.company
        else:
            company = Company()
            company.user_id = user.id 

        self.populate_obj(company)

        db.session.add(company)
        db.session.commit()
        return company


class JobForm(FlaskForm):
    name = StringField('职位名称', validators=[Required(), Length(2, 24)])
    description = StringField('职位详情') 
    tags = StringField('职位标签 (多个用, 隔开)')
    salary = StringField('薪水')

#    work_year = SelectField(
#        '经验要求',
#        choices = [
#            ('不限', '不限'),    
#            ('1', '1'),    
#            ('2', '2'),    
#            ('3', '3'),    
#            ('1-3', '1-3'),    
    #        ('3-5', '3-5'),    
    #        ('5+' '5+')    
    #     ]
    # )

    # degree = SelectField(
    #     '学历要求',
    #     choices = [
    #        ('不限', '不限'),   
    #        ('专科', '专科'),   
    #        ('本科', '本科'),   
    #        ('硕士', '硕士'),   
    #        ('博士', '博士')   
    #     ]
    # )

    work_year = StringField('工作年限')
    degree = StringField('学历')
    submit = SubmitField('发布')

    def update_job(self, job):
        self.populate_obj(job)

        db.session.add(job)
        db.session.commit()
        return job

    def create_job(self, company):
        job = Job()
        self.populate_obj(job)

        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job
