import abc
from pathlib import Path

import pandas as pd
from cathodic_report.wordfile import forms as rforms

from .. import const, forms, utils
from . import DistanceReader, FileReader
from .dfreader import DFReader
from .resis import ResistivityReader
from .stage import Stage2


class GraphReader(DistanceReader, ResistivityReader, FileReader):
    """从二阶段读取数据, 来绘制图表。"""

    def __init__(self, file_num: int):
        self.file_num = file_num
        self.df_reader = DFReader()

    def get_distances(self) -> list[float]:
        return [self.get_distance(i) for i in range(1, self.file_num + 1)]

    def read_df(self) -> pd.DataFrame:
        return self.df_reader.read_csv(self.get_filename())

    def get_resistivities(self) -> list[float]:
        return [self.get_resistivity(i) for i in range(1, self.file_num + 1)]

    def apply_str(self, data_list: list) -> list[str]:
        """调整那些不太标准的数据"""
        return [str(data) for data in data_list]

    def read_graph_data(
        self, circle_graphs: list[rforms.graph.CircleGraph]
    ) -> rforms.graph.GraphData:
        """read data from stage-2"""
        s2 = Stage2(self.read_df())
        distances = self.get_distances()

        poweron_min_max_avg = utils.get_min_max_avg(const.POWER_ON_NAME)
        poweroff_min_max_avg = utils.get_min_max_avg(const.POLAR_NAME)
        dc_density_min_max_avg = utils.get_min_max_avg(const.DC_DENSITY_NAME)
        ac_density_min_max_avg = utils.get_min_max_avg(const.AC_DENSITY_NAME)
        ac_voltage_min_max_avg = utils.get_min_max_avg(const.AC_VOL_NAME)

        return rforms.graph.GraphData(
            circle_graph=circle_graphs,
            potential=rforms.graph.ElecData(
                device_id=self.apply_str(s2.get_col(const.TEST_ID_NAME)),
                distance=distances,
                elec_potential_min=s2.get_col(poweron_min_max_avg[0]),
                elec_potential_max=s2.get_col(poweron_min_max_avg[1]),
                elec_potential_avg=s2.get_col(poweron_min_max_avg[2]),
                v_off_min=s2.get_col(poweroff_min_max_avg[0]),
                v_off_max=s2.get_col(poweroff_min_max_avg[1]),
                v_off_avg=s2.get_col(poweroff_min_max_avg[2]),
            ),
            dc_density=rforms.graph.LineGraph2(
                device_id=self.apply_str(s2.get_col(const.TEST_ID_NAME)),
                distance=distances,
                avg_value=s2.get_col(dc_density_min_max_avg[2]),
                min_value=s2.get_col(dc_density_min_max_avg[0]),
                max_value=s2.get_col(dc_density_min_max_avg[1]),
            ),
            ac_density=rforms.graph.LineGraph2(
                device_id=self.apply_str(s2.get_col(const.TEST_ID_NAME)),
                distance=distances,
                avg_value=s2.get_col(ac_density_min_max_avg[2]),
                min_value=s2.get_col(ac_density_min_max_avg[0]),
                max_value=s2.get_col(ac_density_min_max_avg[1]),
            ),
            ac_voltage=rforms.graph.LineGraph2(
                device_id=self.apply_str(s2.get_col(const.TEST_ID_NAME)),
                distance=distances,
                avg_value=s2.get_col(ac_voltage_min_max_avg[2]),
                min_value=s2.get_col(ac_voltage_min_max_avg[0]),
                max_value=s2.get_col(ac_voltage_min_max_avg[1]),
            ),
            resistivity=rforms.graph.ResisData(
                device_id=self.apply_str(s2.get_col(const.TEST_ID_NAME)),
                distance=distances,
                resistivity=self.get_resistivities(),
            ),
        )
