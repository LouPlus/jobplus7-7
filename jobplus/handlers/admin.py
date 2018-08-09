from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from jobplus.forms import RegisterForm, UserProfileForm, CompanyProfileForm, JobForm 
from jobplus.models import db, User, Job
from flask_login import current_user
from jobplus.decorators import admin_required

admin = Blueprint('admin', __name__, url_prefix='/admin') 


@admin.route('/', methods=['GET','POST'])
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/users', methods=['GET','POST'])
@admin_required
def users():
    page = request.args.get('page', default=1, type=int) 

    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination, active='admin') 




@admin.route('/users/adduser', methods=['GET','POST'])
@admin_required
def adduser():
    form = RegisterForm()
    
    if form.validate_on_submit():
        form.create_user()
        flash('新增用户成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_user.html', form=form)


@admin.route('/users/addcompany', methods=['GET','POST'])
@admin_required
def addcompany():
    form = RegisterForm()
    
    if form.validate_on_submit():
        form.create_company()
        flash('新增企业成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_company.html', form=form)



@admin.route('/users/<int:user_id>/edituser', methods=['GET','POST'])
@admin_required
def edituser(user_id):
    user = User.query.get_or_404(user_id)
    form = UserProfileForm(obj=user.resume)

    if form.validate_on_submit():
        form.update_resume(user)
        flash('简历更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/users/<int:user_id>/editcompany', methods=['GET','POST'])
@admin_required
def editcompany(user_id):
    user = User.query.get_or_404(user_id)
    form = CompanyProfileForm(obj=user.company)

    if form.validate_on_submit():
        form.update_company(user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_company.html', form=form, user=user)



@admin.route('/users/<int:user_id>/disable', methods=['GET','POST'])
@admin_required
def disable(user_id):
    user = User.query.get_or_404(user_id)

    if user.is_disable:
        user.is_disable = False
        flash('已经成功启用用户', 'success')
    else:
        user.is_disable = True
        flash('已经成功禁用用户', 'success')

    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users')) 
    

@admin.route('/jobs') 
@admin_required
def jobs():
    page = request.args.get('page', default=1, type=int) 

    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/jobs.html', pagination=pagination, active='admin') 


