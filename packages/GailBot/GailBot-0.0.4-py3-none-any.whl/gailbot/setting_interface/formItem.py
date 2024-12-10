# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-04-24 18:59:42
# @Last Modified by:   Your name
# @Last Modified time: 2024-04-24 20:57:01
from enum import Enum
from typing import Any
from dataclasses import dataclass

class FormType(Enum):
    Text = 1
    Selection = 2
    OnOff = 3
    File = 4
    MultiSelect = 5


#
@dataclass(init=True)
class FormItem:
    type: FormType
    name: str
    selection_items: Any | None = None
    default_value: Any | None = None