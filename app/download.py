import youtube_dl
import subprocess
import click
import time
from flask.cli import with_appcontext
from .db import (db, Job)
from .s3 import (upload_file)


def download(job):
    options = {
        'outtmpl': '/tmp/%(id)s.%(ext)s',
        'postprocessors': [],
        'postprocessor_args': [],
    }

    if job.file_type == 'mp4':
        options['format'] = 'mp4'

    elif job.file_type == 'mp3':
        options['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })

    else:
        return 'Invalid file type'

    print(options)

    with youtube_dl.YoutubeDL(options) as ydl:
        result = ydl.extract_info(job.url, download=True)
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

    video_id = video['id']
    video_title = video['title']
    downloaded_file = '/tmp/' + video_id + '.' + job.file_type

    if job.start is not None or job.end is not None:
        downloaded_file = slice_media(downloaded_file, job.start, job.end)

    remote_filename = str(job.id) + '.' + job.file_type
    upload_file(downloaded_file, remote_filename)

    return {
        'downloaded_file': remote_filename,
        'filename': video_title + '.' + job.file_type,
    }


def slice_media(downloaded_file, start=None, end=None):
    outfile = downloaded_file.replace('.mp', '-cut.mp')
    command = ['ffmpeg', '-y', '-i', downloaded_file]

    if start is not None:
        command.append('-ss')
        command.append(start)

    if end is not None:
        command.append('-to')
        command.append(end)

    command.append(outfile)

    if subprocess.call(command) != 0:
        raise RuntimeError('Slice command failed')

    return outfile


@click.command('run-job')
@with_appcontext
def download_command():
    """Run the next download job"""
    while True:
        job = Job.query.filter_by(state='created').limit(1).first()

        if job is None:
            click.echo("No unhandled job found, sleeping")
            time.sleep(3)

        else:
            result = download(job)

            job.downloaded_file = result['downloaded_file']
            job.filename = result['filename']
            job.state = 'done'

            db.session.add(job)
            db.session.commit()

            click.echo('Done')
