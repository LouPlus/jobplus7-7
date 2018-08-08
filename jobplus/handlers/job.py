from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, abort
from jobplus.forms import JobForm
from flask_login import login_required, current_user
from jobplus.models import db, Job

job = Blueprint('job', __name__, url_prefix='/job')

@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('job/index.html', pagination=pagination, active='job')


@job.route('/<int:job_id>/enable', methods=['GET','POST'])
@login_required
def enable(job_id):
    job = Job.query.get_or_404(job_id)

    if not current_user.is_admin and current_user.id != job.company.user_id:
        abort(404)

    if not job.is_disable:
        flash('职位上线成功', 'success')
    else:
        job.is_disable = False
        db.session.add(job)
        db.session.commit()
        flash('职位上线成功', 'success')

    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin', company_id=job.company_id))


@job.route('/<int:job_id>/disable', methods=['GET','POST'])
@login_required
def disable(job_id):
    job = Job.query.get_or_404(job_id)

    if not current_user.is_admin and current_user.id != job.company.user_id:
        abort(404)

    if job.is_disable:
        flash('职位下线成功', 'success')
    else:
        job.is_disable = True
        db.session.add(job)
        db.session.commit()
        flash('职位下线成功', 'success')

    if current_user.is_admin:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('company.admin', company_id=job.company_id))

@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job)

