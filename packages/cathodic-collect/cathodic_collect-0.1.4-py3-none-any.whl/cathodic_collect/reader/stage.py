import datetime

import pandas as pd
from cathodic_report.wordfile import forms as rforms

from cathodic_collect import const, tools, utils


class Stage1(tools.DFclass):
    header: list[str] = [
        const.TEST_ID_NAME,
        const.DATE_NAME,
    ]
    min_length: int = 1

    def get_start_end(self) -> tuple[datetime.datetime, datetime.datetime]:
        self.df[const.DATE_NAME] = pd.to_datetime(self.df[const.DATE_NAME])
        start, end = self.df[const.DATE_NAME].iloc[0], self.df[const.DATE_NAME].iloc[-1]
        return start, end

    def get_ts_data(self, name: str) -> rforms.TimeSeries:
        return rforms.TimeSeries(
            name=name,
            time=self.df[const.DATE_NAME].tolist(),
            value=self.df[name].tolist(),
        )

    def total_time(self) -> int:
        start, end = self.get_start_end()
        res = end - start
        assert isinstance(res, datetime.timedelta)
        hours = res.total_seconds() / 3600
        return int(hours)


class Stage2(tools.DFclass):
    header: list[str] = [
        const.TEST_ID_NAME,
        *utils.get_min_max_avg(const.POWER_ON_NAME),
        *utils.get_min_max_avg(const.POLAR_NAME),
        *utils.get_min_max_avg(const.DC_CURRENT_DENSITY_NAME),
        *utils.get_min_max_avg(const.AC_CURRENT_DENSITY_NAME),
        *utils.get_min_max_avg(const.AC_VOL_NAME),
    ]
    min_length: int = 1

    def load_static_value(self, name: str) -> rforms.graph.StaticValue:
        min_max_avg = utils.get_min_max_avg(name)
        min_ = self.df[min_max_avg[0]].iloc[0]
        max_ = self.df[min_max_avg[1]].iloc[0]
        mean_ = self.df[min_max_avg[2]].iloc[0]
        return rforms.graph.StaticValue(
            min=min_,
            max=max_,
            mean=mean_,
        )


class Stage3(tools.DFclass):
    header: list[str] = [
        const.TEST_ID_NAME,
        const.PIECE_ID_NAME,
        const.PIECE_AREA_NAME,
        const.RISK_ASSESS_NAME,
    ]
    min_length: int = 1

    def get_result(self) -> str:
        return self.df[const.RISK_ASSESS_NAME].iloc[0]


class Stage3AC(Stage3):
    header: list[str] = [
        *Stage3.header,
        const.AC_DENSITY_VALUE_0_100,
    ]


class Stage3DC(Stage3):
    header: list[str] = [
        *Stage3.header,
        *utils.get_min_max_avg(const.POWER_ON_NAME),
        *utils.get_min_max_avg(const.POWEROFF_NAME),
        *utils.get_min_max_avg(const.POLAR_NIGHT_20MV),
    ]
