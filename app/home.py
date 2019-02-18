from flask import (
    Blueprint, render_template, request, send_file, redirect, url_for
)
from .db import (db, Job)
from .s3 import (download_file)

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')


@bp.route('/', methods=['POST'])
def create():
    url = request.form['url']
    file_type = request.form['type']

    if request.form['start'] == '':
        start = None
    else:
        start = request.form['start']

    if request.form['end'] == '':
        end = None
    else:
        end = request.form['end']

    job = Job(url=url, file_type=file_type, start=start, end=end, state='created')
    db.session.add(job)
    db.session.commit()

    return redirect(url_for('home.view', id=job.id))


@bp.route('/<int:id>', methods=['GET'])
def view(id):
    job = Job.query.get(id)
    return render_template('home/view.html',
                           job=job,
                           download_url=url_for('home.download', id=job.id))


@bp.route('/<int:id>/download', methods=['GET'])
def download(id):
    job = Job.query.get(id)

    local_file = '/tmp/' + str(job.id)
    download_file(job.downloaded_file, local_file)

    return send_file(local_file,
                     mimetype=job.mime(),
                     as_attachment=True,
                     attachment_filename=job.filename)
