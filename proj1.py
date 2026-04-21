#complete your tasks in this file
import sys
import unittest
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)
#complete your tasks in this file


@dataclass(frozen = True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen = True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str


@dataclass(frozen = True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float

region_conditions = [
    RegionCondition(
        region=Region(
            rect=GlobeRect(1.0, 7.0, 100.0, 105.0),
            name="Malaysia",
            terrain="forest"
        ),
        year=2003,
        pop=50000000,
        ghg_rate=3e8
    ),

    RegionCondition(
        region=Region(
            rect=GlobeRect(40.0, 41.0, -75.0, -73.0),
            name="New York",
            terrain="other"
        ),
        year=2017,
        pop=9000000,
        ghg_rate=5e7
    ),

    RegionCondition(
        region=Region(
            rect=GlobeRect(15.0, 25.0, 35.0, 45.0),
            name="Red Sea",
            terrain="ocean"
        ),
        year=1989,
        pop=0,
        ghg_rate=1e6
    ),

    RegionCondition(
        region=Region(
            rect=GlobeRect(35.0, 36.0, -121.0, -120.0),
            name="San Luis Obispo",
            terrain="other"
        ),
        year=2001,
        pop=47000,
        ghg_rate=5e5
    )
]

def emissions_per_capita(rc: RegionCondition) -> float:
    if rc.pop == 0: 
        return 0.0
    return rc.ghg_rate/rc.pop


def area(gr:GlobeRect) -> float:
    R = 6378.1
    Y1 = math.radians(gr.west_long)
    Y2 = math.radians (gr.east_long)
    O1 = math.radians (gr.lo_lat)
    O2 = math.radians(gr.hi_lat)
    
    long_diff = (Y2 - Y1)
    if long_diff < 0:
        long_diff += 2 * math.pi
    lat_diff = abs((math.sin(O2))-((math.sin(O1))))
    return R**2 * long_diff * lat_diff

def emissions_per_square_km(rc: RegionCondition) -> float:
    a = area(rc.region.rect)
    if a == 0:
        return 0.0
    return rc.ghg_rate/a

def get_density(rc: RegionCondition) -> float:
    reg_area = area(rc.region.rect)
    if reg_area == 0:
        return 0.0
    return rc.pop/ reg_area

def densest(rc_list: List[RegionCondition]) -> str:
    if not rc_list:
        raise ValueError("empty list")
    if len(rc_list) == 1:
        return rc_list[0].region.name

    def find_max_rc(rs: List[RegionCondition]) -> RegionCondition:
        if len(rs) == 1:
            return rs[0]
        first = rs[0]
        best_of_rest = find_max_rc(rs[1:])
        if get_density(first) >= get_density(best_of_rest):
            return first
        else:
            return best_of_rest

    return find_max_rc(rc_list).region.name


def growth_rate(terrain: str) -> float:
    if terrain == "ocean":
        return 0.0001
    if terrain == "mountains":
        return 0.0005
    if terrain == "forest":
        return -0.00001
    return 0.0003


def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    rate = growth_rate(rc.region.terrain)
    new_pop = int(rc.pop * ((1 + rate) ** years))

    if rc.pop == 0:
        new_ghg = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)

    return RegionCondition(
        region=rc.region,
        year=rc.year + years,
        pop=new_pop,
        ghg_rate=new_ghg
    )

# region_conditions = [Malaysia, 2003, 50000000, 3e8]
# region_conditions = [New_York, 2017, 9000000, 5e7]
# region_conditions = [Red_Sea, 1989, 6000000, 1e6]
# region_conditions = [San_Luis_Obispo, 2001, 47000, 5e5]]
