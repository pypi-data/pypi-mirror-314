from pydantic import BaseModel


class SinglePoint(BaseModel):
    """single point data in graph-data"""

    distance: float
    device_id: str
    # 土壤电阻率
    resistivity: float

    poweron_elec_avg: float
    poweron_elec_min: float
    poweron_elec_max: float

    v_off_avg: float
    v_off_min: float
    v_off_max: float

    dc_density_min: float
    dc_density_max: float
    dc_density_avg: float

    ac_density_min: float
    ac_density_max: float
    ac_density_avg: float

    ac_vol_min: float
    ac_vol_max: float
    ac_vol_avg: float
