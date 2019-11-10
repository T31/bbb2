import sys
import traceback

from BackblazeB2Client import BackblazeB2Client
from BackblazeB2Error import BackblazeB2Error

if "__main__" == __name__:
    try:
        if len(sys.argv) <= 1:
            print("Please provide command line argument(s).")
            sys.exit(1)

        if sys.argv[1] == "--list-buckets":
            client = BackblazeB2Client()
            client.authorize()

            specific_bucket = None
            if len(sys.argv) > 2:
                specific_bucket = sys.argv[2]

            for bucket in client.list_buckets(specific_bucket):
                print("[BucketName=" + bucket[0]
                      + ", BucketId=" + bucket[1] + "]")

        if sys.argv[1] == "--upload-file":
            if len(sys.argv) < 5:
                print("Please provide a bucket name, destination file name"
                      + ", and a source file path.")
                sys.exit(1)

            bucket_name = sys.argv[2]
            dst_file_name = sys.argv[3]
            src_file_path = sys.argv[4]

            print("Attempting to upload file \"" + src_file_path + "\""
                  + " to bucket \"" + bucket_name + "\""
                  + " with name \"" + dst_file_name + "\".")

            client = BackblazeB2Client()
            client.authorize()
            results = client.upload_file(bucket_name, dst_file_name,
                                         src_file_path)
    except BackblazeB2Error as e:
        traceback.print_exc()
