import boto3

s3 = boto3.client('s3')


def download_file(remote_file, local_file):
    return s3.download_file('youtube-dl-storage', remote_file, local_file)


def upload_file(local_file, remote_filename):
    return s3.upload_file(local_file, 'youtube-dl-storage', remote_filename);
