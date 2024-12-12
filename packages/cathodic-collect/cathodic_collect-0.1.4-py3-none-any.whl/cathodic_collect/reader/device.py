import abc
import typing as t
from multiprocessing import Value
from pathlib import Path

import pandas as pd
from cathodic_report.wordfile import forms as rforms

from cathodic_collect import const
from cathodic_collect.forms import Meta

from . import stage
from .dfreader import DFReader


class StageFileReader(abc.ABC):
    workdir: str  # 必须设置默认的 workdir

    @abc.abstractmethod
    def get_workdir(self) -> Path:
        pass

    @abc.abstractmethod
    def read_stage(
        self, stage: int, file_id: int, ctype: t.Literal["ac", "dc"]
    ) -> Path:
        """从根据不同阶段，获得不同 file-id 的文件名"""
        pass


class DeviceReader(StageFileReader):
    def __init__(self, meta: Meta):
        self.meta = meta
        self.df_reader = DFReader()

    def read_device(self, file_id: int) -> rforms.DeviceInfo:
        self.check_file_id(file_id)
        return rforms.DeviceInfo(
            device_form=self.get_device_form(file_id),
            table_forms=self.get_table_forms(file_id),
            graph_data=self.get_graph_data(file_id),
        )

    def get_device_form(self, file_id: int) -> rforms.DeviceForm:
        """从 meta 中读取数据，并且返回"""
        summary_form = self.meta.summary_table[file_id - 1]
        return rforms.DeviceForm(
            id=file_id,
            device_id=summary_form.device_id,
            distance=summary_form.distance,
            piece_area=summary_form.piece_area,
            resistivity=summary_form.resistivity,
            judge_metric=-0.85,  # make it default.
            protect_status="有" if summary_form.is_protect else "无",
        )

    def get_device_id(self, file_id: int) -> str:
        """从 meta 中读取数据，并且返回"""
        device_id = self.meta.summary_table[file_id - 1].device_id
        assert file_id == self.meta.summary_table[file_id - 1].id
        return device_id

    def read_df(
        self, stage: int, file_id: int, ctype: t.Literal["ac", "dc"]
    ) -> pd.DataFrame:
        return self.df_reader.read_csv(
            self.read_stage(stage=stage, file_id=file_id, ctype=ctype),
        )

    def filter_device(self, sfile, file_id):
        df = sfile.df[sfile.df[const.TEST_ID_NAME] == self.get_device_id(file_id)]
        if df.empty:
            df = sfile.df[
                sfile.df[const.TEST_ID_NAME] == int(self.get_device_id(file_id))
            ]
        return df

    def get_table_forms(self, file_id: int) -> list[rforms.TableForm]:
        """从不同阶段的文件中读取并且返回 table 数据"""
        res = []

        if self.meta.has_ac:
            s1 = stage.Stage1(self.read_df(stage=1, file_id=file_id, ctype="ac"))
            s2 = stage.Stage2(self.read_df(stage=2, file_id=file_id, ctype="ac"))

            s2df = self.filter_device(s2, file_id)
            s2 = stage.Stage2(s2df)
            s3 = stage.Stage3(self.read_df(stage=3, file_id=file_id, ctype="ac"))
            s3df = self.filter_device(s3, file_id)
            s3 = stage.Stage3(s3df)

            res.append(
                rforms.TableForm(
                    id=file_id,
                    table_data=rforms.graph.DeviceTable(
                        table_name="交流干扰分析结果",
                        c_type="交流",
                        start_time=s1.get_start_end()[0].strftime("%Y-%m-%d %H:%M"),
                        end_time=s1.get_start_end()[1].strftime("%Y-%m-%d %H:%M"),
                        total_time=s1.total_time(),
                        po=s2.load_static_value(const.POWER_ON_NAME),
                        pf=s2.load_static_value(const.POLAR_NAME),
                        dc_density=s2.load_static_value(const.DC_DENSITY_NAME),
                        ac_density=s2.load_static_value(const.AC_DENSITY_NAME),
                        ac_voltage=s2.load_static_value(const.AC_VOL_NAME),
                        judge_result=s3.get_result(),
                    ),
                ),
            )
        if self.meta.has_dc:
            s1 = stage.Stage1(self.read_df(1, file_id, ctype="dc"))
            s2 = stage.Stage2(self.read_df(2, file_id, ctype="dc"))
            s2df = self.filter_device(s2, file_id)
            s2 = stage.Stage2(s2df)
            s3 = stage.Stage3(self.read_df(3, file_id, ctype="dc"))
            s3df = self.filter_device(s3, file_id)
            s3 = stage.Stage3(s3df)

            res.append(
                rforms.TableForm(
                    id=file_id,
                    table_data=rforms.graph.DeviceTable(
                        table_name="直流干扰分析结果",
                        c_type="直流",
                        start_time=s1.get_start_end()[0].strftime("%Y-%m-%d %H:%M"),
                        end_time=s1.get_start_end()[1].strftime("%Y-%m-%d %H:%M"),
                        total_time=s1.total_time(),
                        po=s2.load_static_value(const.POWER_ON_NAME),
                        pf=s2.load_static_value(const.POLAR_NAME),
                        dc_density=s2.load_static_value(const.DC_DENSITY_NAME),
                        ac_density=s2.load_static_value(const.AC_DENSITY_NAME),
                        ac_voltage=s2.load_static_value(const.AC_VOL_NAME),
                        judge_result=s3.get_result(),
                    ),
                ),
            )
        return res

    def check_file_id(self, file_id: int):
        assert file_id >= 1 and file_id <= self.meta.header.file_num

    def get_graph_data(self, file_id: int) -> rforms.DeviceTimeSeries:
        # dc ac 是一样的
        ctype: t.Literal["ac", "dc"] = "ac" if self.meta.has_ac else "dc"
        s1 = stage.Stage1(self.read_df(stage=1, file_id=file_id, ctype=ctype))

        return rforms.DeviceTimeSeries(
            id=file_id,
            poweron=s1.get_ts_data(const.POWER_ON_NAME),
            poweroff=s1.get_ts_data(const.POWEROFF_NAME),
            ac_density=s1.get_ts_data(const.AC_DENSITY_NAME),
            dc_density=s1.get_ts_data(const.DC_DENSITY_NAME),
            ac_voltage=s1.get_ts_data(const.AC_VOL_NAME),
        )
