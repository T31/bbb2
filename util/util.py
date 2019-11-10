import hashlib
import os.path

def get_file_len_bytes(file_path):
    file_size = None
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        msg = ("Failed to get file size."
               " SrcFilePath=\"" + str(file_path) + "\".")
        raise BackblazeB2Error(msg) from e

def calc_sha1(file_path):
    file_stream = None
    try:
        file_stream = open(file=file_path, mode='rb')
    except OSError as e:
        msg = "Failed to calc sha1 for file \"" + str(file_path) + "\"."
        raise BackblazeB2Error(msg) from e

    try:
        hasher = hashlib.sha1()
        chunk = file_stream.read(4096)
        while chunk:
            hasher.update(chunk)
            chunk = file_stream.read(4096)
        return hasher.hexdigest()
    finally:
        file_stream.close()

def get_entire_file(file_path):
    file_stream = None
    try:
        file_stream = open(file=file_path, mode='rb')
    except OSError as e:
        msg = "Failed to read file \"" + str(file_path) + "\"."
        raise BackblazeB2Error(msg) from e

    try:
        return file_stream.read()
    finally:
        file_stream.close()
