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
            results = client.list_buckets()

            for bucket in results:
                print("[BucketName=" + bucket[0]
                      + ", BucketId=" + bucket[1] + "]")
    except BackblazeB2Error as e:
        traceback.print_exc()
