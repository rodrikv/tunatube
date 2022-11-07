import platform
import re
import subprocess
from sys import float_repr_style
import tempfile
import os
import mimetypes

from hachoir.metadata.video import MP4Metadata
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hachoir.core import config as hachoir_config
from telethon.tl.types import DocumentAttributeVideo

hachoir_config.quiet = True


def video_metadata(file):
    return extractMetadata(createParser(file))


def call_ffmpeg(args):
    try:
        return subprocess.Popen([get_ffmpeg_command()] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise Exception(
            'ffmpeg command is not available. Thumbnails for videos are not available!')


def get_ffmpeg_command():
    return os.environ.get('FFMPEG_COMMAND',
                          'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg')


def get_video_size(file):
    p = call_ffmpeg([
        '-i', file,
    ])
    stdout, stderr = p.communicate()
    video_lines = re.findall(
        ': Video: ([^\n]+)', stderr.decode('utf-8', errors='ignore'))
    if not video_lines:
        return
    matchs = re.findall("(\d{2,6})x(\d{2,6})", video_lines[0])
    if matchs:
        return [int(x) for x in matchs[0]]

def get_video_rotation(file):
    p = call_ffmpeg([
        '-i', file,
    ])
    stdout, stderr = p.communicate()
    video_lines = re.findall(
        'displaymatrix: rotation of -(.+) degrees', stderr.decode('utf-8', errors='ignore'))
    if not video_lines:
        return False
    return abs(float(video_lines[0])) == float(90)


def get_video_thumb(file, output=None, size=200):
    output = output or tempfile.NamedTemporaryFile(suffix='.jpg').name
    metadata = video_metadata(file)
    if metadata is None:
        return
    duration = metadata.get(
        'duration').seconds if metadata.has('duration') else 0
    ratio = get_video_size(file)
    if ratio is None:
        raise Exception('Video ratio is not available.')
    if ratio[0] / ratio[1] > 1:
        width, height = size, -1
    else:
        width, height = -1, size
    p = call_ffmpeg([
        '-ss', str(int(duration / 2)),
        '-i', file,
        '-filter:v',
        'scale={}:{}'.format(width, height),
        '-vframes:v', '1',
        output,
    ])
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        return output


def get_file_mime(file):
    return (mimetypes.guess_type(file)[0] or ('')).split('/')[0]


def get_file_attributes(file):
    attrs = []
    mime = get_file_mime(file)
    if mime == 'video':
        metadata = video_metadata(file)
        rotate = get_video_rotation(file)
        video_meta = metadata
        meta_groups = None
        if hasattr(metadata, '_MultipleMetadata__groups'):
            # Is mkv
            meta_groups = metadata._MultipleMetadata__groups
        if metadata is not None and not metadata.has('width') and meta_groups:
            video_meta = meta_groups[next(
                filter(lambda x: x.startswith('video'), meta_groups._key_list))]
        if metadata is not None:
            supports_streaming = isinstance(video_meta, MP4Metadata)
            attrs.append(DocumentAttributeVideo(
                (0, metadata.get('duration').seconds)[
                    metadata.has('duration')],
                (0, video_meta.get('width' if not rotate else 'height'))[video_meta.has('width')],
                (0, video_meta.get('height' if not rotate else 'width'))[video_meta.has('height')],
                False,
                True,
            ))
    return attrs


def get_file_thumb(file):
    if get_file_mime(file) == 'video':
        return get_video_thumb(file)
