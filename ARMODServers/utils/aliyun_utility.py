import oss2
from django.conf import settings
from django.core.files.storage import Storage


class AliyunObjectStorage(Storage):
    def __init__(self):
        self.access_key_id = settings.OSS_ACCESS_KEY_ID
        self.access_key_secret = settings.OSS_ACCESS_KEY_SECRET
        self.bucket_name = settings.OSS_BUCKET_NAME
        self.endpoint = settings.OSS_ENDPOINT
        self.access_url = settings.OSS_BASE_URL

    @property
    def bucket(self):
        return oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret), self.endpoint, self.bucket_name)

    def _open(self, name):
        return self.bucket.get_object(name)

    def _save(self, name, content):
        self.bucket.put_object(name, content)
        return name

    def _save(self, name, content, progress_callback):
        return self.bucket.put_object(name, content, progress_callback=progress_callback)

    def delete(self, name):
        return self.bucket.delete_object(name)

    def batch_delete_objects(self,files):
        return self.bucket.batch_delete_objects(files)

    def exists(self, name):
        return self.bucket.object_exists(name)

    def listdir(self, path):
        dirs, files = [], []
        objects = self.bucket.list_objects(path).object_list
        for object in objects:
            files.append(object.key.split(path)[-1])
        return dirs, files

    def size(self, name):
        return self.bucket.get_object_meta(name).content_length

    def url(self, name):
        return '{}/{}'.format(self.access_url, name)
