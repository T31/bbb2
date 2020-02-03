import sys
import traceback

from BackblazeB2Client import BackblazeB2Client
from BackblazeB2Error import BackblazeB2ConnectError
from BackblazeB2Error import BackblazeB2Error
import log

def get_help_msg():
    return ("Usage : bbb2 --list-buckets [bucketName]\n"
            + "        bbb2 --upload-file dstBucketName dstName srcPath\n"
            + "        bbb2 --cancel-all-large-file-uploads\n"
            + "        bbb2 --copy-file srcFileId dstBucketName dstFileName\n"
            + "        bbb2 --download srcBucketName srcFileName dstFilePath")

if "__main__" == __name__:
    try:
        if len(sys.argv) <= 1:
            print("Please provide command line argument(s).")
            sys.exit(1)

        if (sys.argv[1] == "-h") or (sys.argv[1] == "--help"):
            print(get_help_msg())
        elif sys.argv[1] == "--list-buckets":
            client = BackblazeB2Client()
            client.authorize()

            specific_bucket = None
            if len(sys.argv) > 2:
                specific_bucket = sys.argv[2]

            buckets = client.list_buckets(specific_bucket)
            for name in buckets:
                print("[BucketName=" + name
                      + ", BucketId=" + buckets[name] + "]")
        elif sys.argv[1] == "--upload-file":
            if len(sys.argv) < 5:
                print("Please provide a bucket name, destination file name"
                      + ", and a source file path.")
                sys.exit(1)

            bucket_name = sys.argv[2]
            dst_file_name = sys.argv[3]
            src_file_path = sys.argv[4]

            log.log_info("Attempting to upload file \"" + src_file_path + "\""
                         + " to bucket \"" + bucket_name + "\""
                         + " with name \"" + dst_file_name + "\".")

            client = BackblazeB2Client()
            client.authorize()
            client.upload_file(bucket_name, dst_file_name, src_file_path)
        elif sys.argv[1] == "--cancel-all-large-file-uploads":
            client = BackblazeB2Client()
            client.authorize()
            client.cancel_all_large_files()
        elif sys.argv[1] == "--copy-file":
            src_file_id = sys.argv[2]
            dst_bucket_name = sys.argv[3]
            dst_file_name = sys.argv[4]

            client = BackblazeB2Client()
            client.authorize()
            client.copy_file(src_file_id, dst_bucket_name, dst_file_name)
        elif sys.argv[1] == "--download":
            src_bucket_name = sys.argv[2]
            src_file_name = sys.argv[3]
            dst_file_path = sys.argv[4]
            client = BackblazeB2Client()
            while True:
                try:
                    client.authorize()
                    client.download_file(src_bucket_name, src_file_name,
                                         dst_file_path)
                    break
                except BackblazeB2ConnectError as e:
                    log.log_warning("Connect error during download."
                                    + " Reauthorizing.")
        else:
            print("Unrecognized args.")
            print(get_help_msg())
    except BackblazeB2Error as e:
        traceback.print_exc()
