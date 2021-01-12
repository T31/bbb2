import client.internal

class Internal:
    def get_key_from_file(self, key_file_path = None):
        return client.internal.AppKey("someKeyId", "someAppKey")
