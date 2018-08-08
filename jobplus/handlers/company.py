from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, abort
from jobplus.forms import JobForm, CompanyProfileForm
from flask_login import current_user
from jobplus.decorators import company_required
from jobplus.models import db, Job, User, Company

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Company.query.paginate(
            page = page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False
    )
    return render_template('company/index.html', pagination=pagination, active='company')

@company.route('/profile', methods=['GET','POST'])
@company_required
def profile():
    if not current_user.is_company:
        flash('你不是企业用户', 'warning')
        return redirect(url_for('front.index'))

    form = CompanyProfileForm(obj=current_user.company)
    if form.validate_on_submit():
        form.update_company(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)


@company.route('/<int:company_id>/admin', methods=['GET','POST'])
@company_required
def admin(company_id):
    page = request.args.get('page', default=1, type=int) 
    
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('company/jobs.html', company_id=company_id, pagination=pagination)  


@company.route('/<int:company_id>/admin/publish_job', methods=['GET','POST'])
@company_required
def publish_job(company_id):
    if current_user.company.id != company_id:
        abort(404)

    form = JobForm()

    if form.validate_on_submit():
        form.create_job(current_user.company)
        flash('新增职位成功', 'success')
        return redirect(url_for('company.admin', company_id=company_id))
    return render_template('company/publish_job.html', company_id=company_id, form=form)  


@company.route('/<int:company_id>/admin/edit_job/<int:job_id>/', methods=['GET','POST'])
@company_required
def edit_job(company_id, job_id):
    if current_user.company.id != company_id:
        abort(404)

    job = Job.query.get_or_404(job_id)

    if job.company_id != current_user.company.id:
        abort(404)

    form = JobForm(obj=job)

    if form.validate_on_submit():
        form.update_job(job)
        flash('修改职位成功', 'success')
        return redirect(url_for('company.admin', company_id=company_id))
    return render_template('company/edit_job.html', company_id=company_id, form=form, job=job)  


@company.route('/<int:company_id>/admin/delete_job/<int:job_id>/', methods=['GET','POST'])
@company_required
def delete_job(company_id, job_id):
    if current_user.company.id != company_id:
        abort(404)

    job = Job.query.get_or_404(job_id)

    if job.company_id != current_user.company.id:
        abort(404)

    db.session.delete(job)
    db.session.commit()
    flash('删除职位成功', 'success')
    return redirect(url_for('company.admin', company_id=company_id))

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company, active='', panel='about')

@company.route('/<int:company_id>/job')
def company_jobs(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company/detail.html', company=company, active='', panel='job')



