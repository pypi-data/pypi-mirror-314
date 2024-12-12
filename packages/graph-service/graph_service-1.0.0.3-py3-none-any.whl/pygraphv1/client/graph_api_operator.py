#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/25
# @Author  : yanxiaodong
# @File    : graph_api_operator.py
"""
from pydantic import BaseModel, Field
from typing import List, Optional

from .graph_api_variable import Variable


class CategoryVisual(BaseModel):
    """
    CategoryVisual
    """
    name: str = None
    display_name: str = Field(None, alias="displayName")


class Operator(BaseModel):
    """
    Operator
    """
    name: str = None
    local_name: str = Field(None, alias="localName")
    display_name: str = Field(None, alias="displayName")
    kind: str = None
    kind_display_name: str = Field(None, alias="kindDisplayName")
    parent_kind: str = Field(None, alias="parentKind")
    description: str = None
    category: List[str] = None
    category_visual: Optional[CategoryVisual] = Field(None, alias="categoryVisual")
    inputs: Optional[List[Variable]] = None
    outputs: Optional[List[Variable]] = None
    properties: Optional[List[Variable]] = None
    states: Optional[List[Variable]] = None
    visuals: Optional[str] = None
    runtime: str = None
    version: str = None


class CreateOperatorRequest(BaseModel):
    """
    CreateOperatorRequest  create a new op
    """
    operator: Operator = Field(None, alias="operator"),
    file_name: str = Field(..., alias="fileName", description="算子文件名", example="MongoDatasource.yaml")
    need_upload: bool = Field(None, description="是否需要上传算子文件", alias="needUpload", example=True)
