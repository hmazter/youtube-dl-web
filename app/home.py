from flask import (
    Blueprint, render_template, request, send_file
)
from . import download as dl

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')


@bp.route('/', methods=['POST'])
def download():
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

    result = dl.download(url, file_type, start, end)

    return send_file(result['downloaded_file'],
                     mimetype=result['mime'],
                     as_attachment=True,
                     attachment_filename=result['filename'])
