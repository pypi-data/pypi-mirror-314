# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-10 22:00:14
# @Description: Define the schema for data related to a single plugin suite
from typing import Dict, List, Optional
from pydantic import BaseModel


class Suite(BaseModel):
    name: str
    id: str
    description: str
    Version: str
    Author: str
    plugins: str


    # Version: str
    # Author: str
    # Email: str
    # BucketName: Optional[str] = ""
    # ObjectName: Optional[str] = ""
    # ObjectUrl: Optional[str] = ""


class Requirements(BaseModel):
    requirements: Optional[Dict[str, str]] = {}  

class Dependencies(BaseModel):
    dependencies: Optional[Dict[str, str]] = {}  

class ConfModel(BaseModel):
    # """dictionary type for plugin suite configuration dictionary"""

    suite: Suite
    requirements: Optional[Requirements] = None  
    dependencies: Optional[Dependencies] = None 

    # suite_name: str
    # plugins: List[PluginDict]
