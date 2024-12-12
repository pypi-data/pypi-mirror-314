#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/19
# @Author  : yanxiaodong
# @File    : types.py
"""
from typing import List, Optional
from pydantic import BaseModel, Field

from .graph_api_variable import Variable
from .graph_api_operator import Operator


class EdgeTarget(BaseModel):
    """
    EdgeTarget
    """
    operator: str = None
    property: str = None
    input: str = None
    output: str = None
    state: str = None


class Edge(BaseModel):
    """
    Edge
    """
    from_: EdgeTarget = Field(None, alias="from")
    to: EdgeTarget = None


class GraphContent(BaseModel):
    """
    Graph Content
    """
    name: Optional[str] = None
    local_name: Optional[str] = Field(None, alias="localName")
    environment: Optional[str] = None
    properties: Optional[List[Variable]] = None
    inputs: Optional[List[Variable]] = None
    outputs: Optional[List[Variable]] = None
    nodes: Optional[List[Operator]] = None
    edges: Optional[List[Edge]] = None
    visuals: Optional[str] = None