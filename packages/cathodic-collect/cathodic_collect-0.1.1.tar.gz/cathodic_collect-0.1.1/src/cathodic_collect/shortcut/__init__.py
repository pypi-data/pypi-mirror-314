"""
这是为了方便快速导入编写的文件，里面的函数基本上都是图简单，图快来编写的。日后可能不会很好的维护。
"""

from .device import get_device_form
from .graph import get_tsdata_from_file

__all__ = ["get_device_form", "get_tsdata_from_file"]
