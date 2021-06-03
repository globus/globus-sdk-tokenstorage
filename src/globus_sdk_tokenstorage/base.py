import abc
import contextlib
import os


class StorageAdapter(abc.ABC):
    @abc.abstractmethod
    def store(self, token_response):
        raise NotImplementedError

    def on_refresh(self, token_response):
        """
        By default, the on_refresh handler for a token storage adapter simply
        stores the token response.
        """
        return self.store(token_response)


class FileAdapter(StorageAdapter):
    """
    File adapters are for single-user cases, where we can assume that there's a
    simple file-per-user and users are only ever attempting to read their own
    files.
    """

    def file_exists(self):
        """
        Check if the file used by this file storage adapter exists.
        """
        return os.path.exists(self.filename)

    def read_as_dict(self):
        raise NotImplementedError

    @contextlib.contextmanager
    def user_only_umask(self):
        """
        a context manager to deny rwx to Group and World, x to User
        this does not create a file, but ensures that if a file is created while in the
        context manager, its permissions will be correct on unix systems
        """
        old_umask = os.umask(0o177)
        try:
            yield
        finally:
            os.umask(old_umask)
