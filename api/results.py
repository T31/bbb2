class UploadPart:
    part_num = None
    content_len = None
    sha1 = None

    def __init__(self, part_num, content_len, sha1):
        self.part_num = part_num
        self.content_len = content_len
        self.sha1 = sha1

class ListPartsResult:
    upload_parts = None
    next_part = None

    def __init__(self, upload_parts, next_part):
        self.upload_parts = upload_parts
        self.next_part = next_part

class UnfinishedLargeFile:
    file_id = None
    file_name = None

    def __init__(self, file_id, file_name):
        self.file_id = file_id
        self.file_name = file_name

class ListUnfinishedLargeFilesResult:
    unfinished_files = None
    next_file = None

    def __init__(self, unfinished_files, next_file):
        self.unfinished_files = unfinished_files
        self.next_file = next_file

class DownloadFileByIdResult:
    file_id = None
    content_len = None
    sha1 = None
    payload = None

    def __init__(self, file_id, content_len, sha1, payload,):
        self.file_id = file_id
        self.content_len = content_len
        self.sha1 = sha1
        self.payload = payload
