import youtube_dl
import subprocess
import click
from flask.cli import with_appcontext
from .db import (db, Job)


def download(url, file_type, start, end):
    options = {
        'outtmpl': '/tmp/%(id)s.%(ext)s',
        'postprocessors': [],
        'postprocessor_args': [],
    }

    if file_type == 'mp4':
        options['format'] = 'mp4'

    elif file_type == 'mp3':
        options['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })

    else:
        return 'Invalid file type'

    print(options)

    with youtube_dl.YoutubeDL(options) as ydl:
        result = ydl.extract_info(url, download=True)
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result

    video_id = video['id']
    video_title = video['title']
    downloaded_file = '/tmp/' + video_id + '.' + file_type

    if start is not None or end is not None:
        downloaded_file = slice_media(downloaded_file, start, end)

    return {
        'downloaded_file': downloaded_file,
        'filename': video_title + '.' + file_type,
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
    job = Job.query.filter_by(state='created').limit(1).first()

    if job is None:
        click.echo("No unhandled job found")
        return

    result = download(job.url, job.file_type, job.start, job.end)

    job.downloaded_file = result['downloaded_file']
    job.filename = result['filename']
    job.state = 'done'

    db.session.add(job)
    db.session.commit()

    click.echo('Done')
