# -*- coding: utf-8 -*-
# @Author: Jason Y. Wu
# @Date:   2023-07-31 16:21:27
# @Last Modified by:   Jason Y. Wu
# @Last Modified time: 2023-08-01 05:37:57
from dataclasses import dataclass
from datetime import date, time


@dataclass
class ProcessingStats:
    """
    Defines a class to contain stats about each processing item
    """

    date: date = date.today().strftime("%m/%d/%y")
    start_time: time | float = None
    end_time: time | float = None
    elapsed_time_sec: float = None
