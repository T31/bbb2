import enum
import sys
import traceback

import client.client
import Bbb2Error
import log

class ExitCode(enum.Enum):
    NORMAL = 0
    USER_ERROR = 1
    INTERNAL_ERROR = 2

def usage_msg():
    return "Usage : bbb2 --list-buckets [bucketName]\n" \
           "        bbb2 --upload dstBucketName dstName srcPath\n" \
           "        bbb2 --cancel-all-large-file-uploads\n" \
           "        bbb2 --download srcBucketName srcFileName dstFilePath\n" \
           "        bbb2 {-h|--help}"

if "__main__" == __name__:
    try:
        if len(sys.argv) <= 1:
            print("Please provide command line argument(s).")
            sys.exit(ExitCode.USER_ERROR)

        if (sys.argv[1] == "-h") or (sys.argv[1] == "--help"):
            print(usage_msg())
        elif sys.argv[1] == "--list-buckets":
            client = client.client.Client()
            client.authorize()

            specific_bucket = None
            if len(sys.argv) > 2:
                specific_bucket = sys.argv[2]

            buckets = client.list_buckets(specific_bucket)
            for name in buckets:
                print("[BucketName=" + name
                      + ", BucketId=" + buckets[name] + "]")
        elif sys.argv[1] == "--upload":
            if len(sys.argv) < 5:
                print("Please provide a bucket name, destination file name"
                      + ", and a source file path.")
                sys.exit(ExitCode.USER_ERROR)

            bucket_name = sys.argv[2]
            dst_file_name = sys.argv[3]
            src_file_path = sys.argv[4]

            log.log_info("Attempting to upload file \"" + src_file_path + "\""
                         + " to bucket \"" + bucket_name + "\""
                         + " with name \"" + dst_file_name + "\".")

            client = client.client.Client()
            client.authorize()
            client.upload_file(bucket_name, dst_file_name, src_file_path)
        elif sys.argv[1] == "--cancel-all-large-file-uploads":
            client = client.client.Client()
            client.authorize()
            client.cancel_all_large_files()
        elif sys.argv[1] == "--download":
            src_bucket_name = sys.argv[2]
            src_file_name = sys.argv[3]
            dst_file_path = sys.argv[4]
            client = client.client.Client()
            while True:
                try:
                    client.authorize()
                    client.download_file(src_bucket_name, src_file_name,
                                         dst_file_path)
                    break
                except Bbb2Error.ConnectError as e:
                    log.log_warning("Connect error during download."
                                    + " Reauthorizing.")
        else:
            print("Unrecognized args.\n"
                  + usage_msg())
            sys.exit(ExitCode.USER_ERROR)
    except Bbb2Error.Bbb2Error as e:
        log.log_error("Aborting due to error.")
        traceback.print_exc()
        sys.exit(ExitCode.INTERNAL_ERROR)