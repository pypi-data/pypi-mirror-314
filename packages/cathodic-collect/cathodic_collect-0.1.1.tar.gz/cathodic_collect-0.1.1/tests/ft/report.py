# customed report
from cathodic_report.report import Report

from . import s


class MyReport(Report):
    """用于测试图片绘制"""

    # _p alias Path
    def template_folder_fn(self) -> s.Path:
        return s.Path("./src/templates/")

    def render_device_graph(self, device_data: s.rforms.DeviceTimeSeries):
        self._render_device_graph(data=device_data)
