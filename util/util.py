import hashlib
import os.path

from BackblazeB2Error import BackblazeB2Error

def get_file_len_bytes(file_path):
    file_size = None
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        msg = ("Failed to get file size."
               " SrcFilePath=\"" + str(file_path) + "\".")
        raise BackblazeB2Error(msg) from e

def calc_sha1(data):
    hasher = hashlib.sha1()
    hasher.update(data)
    return hasher.hexdigest()

def calc_sha1_file(file_path):
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

def open_binary_read_file(file_path):
    try:
        return open(file=file_path, mode='rb')
    except OSError as e:
        msg = "Unable to open file \"" + src_file_path + "\"."
        raise BackblazeB2Error(msg) from e

def read_file_chunk(read_file, read_len):
    if 0 == read_len:
        return bytearray()

    ret_val = bytearray()
    parts = []
    bytes_left = read_len

    while bytes_left > 0:
        part = read_file.read(bytes_left)
        if len(part) == 0:
            return ret_val.join(parts)
        elif None == part:
            continue

        bytes_left -= len(part)
        parts.append(part)

    return ret_val.join(parts)
