import youtube_dl


def download(url, file_type):
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

    return {
        'downloaded_file': '/tmp/' + video_id + '.' + file_type,
        'filename': video_title + '.' + file_type,
        'mime': mime
    }
