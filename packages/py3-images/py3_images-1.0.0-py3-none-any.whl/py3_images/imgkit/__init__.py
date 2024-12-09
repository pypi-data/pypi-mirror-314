#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_images
=================================================
"""
import os

import imgkit
from addict import Dict


def from_string(**kwargs):
    """
    @see https://pypi.org/project/imgkit/
    :param kwargs:
    :return:
    """
    kwargs = Dict(kwargs)
    kwargs.setdefault("output_path", None)
    if isinstance(kwargs.get("output_path", None), str) and len(kwargs.get("output_path", "")):
        os.makedirs(os.path.dirname(kwargs.get("output_path")), exist_ok=True)
    if imgkit.from_string(**kwargs):
        return kwargs.get("output_path", None)
    return None


def from_url(**kwargs):
    """
    @see https://pypi.org/project/imgkit/
    :param kwargs:
    :return:
    """
    kwargs = Dict(kwargs)
    kwargs.setdefault("output_path", None)
    if isinstance(kwargs.get("output_path", None), str) and len(kwargs.get("output_path", "")):
        os.makedirs(os.path.dirname(kwargs.get("output_path")), exist_ok=True)
    if imgkit.from_url(**kwargs):
        return kwargs.get("output_path", None)
    return None


def from_file(**kwargs):
    """
    @see https://pypi.org/project/imgkit/
    :param kwargs:
    :return:
    """
    kwargs = Dict(kwargs)
    kwargs.setdefault("output_path", None)
    if isinstance(kwargs.get("output_path", None), str) and len(kwargs.get("output_path", "")):
        os.makedirs(os.path.dirname(kwargs.get("output_path")), exist_ok=True)
    if imgkit.from_file(**kwargs):
        return kwargs.get("output_path", None)
    return None
