import youtube_dl
import subprocess


def download(url, file_type, start, end):
    options = {
        'outtmpl': '/tmp/%(id)s.%(ext)s',
        'postprocessors': [],
        'postprocessor_args': [],
    }

    if file_type == 'mp4':
        options['format'] = 'mp4'
        mime = 'video/mp4'

    elif file_type == 'mp3':
        options['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })
        mime = 'audio/mp3'

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
        'mime': mime
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
