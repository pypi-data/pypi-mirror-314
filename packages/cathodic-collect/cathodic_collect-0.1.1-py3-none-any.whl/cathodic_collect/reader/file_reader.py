import abc
import pathlib


class FileReader(abc.ABC):
    @abc.abstractmethod
    def get_filename(self) -> pathlib.Path:
        """获取文件名称"""
        pass
