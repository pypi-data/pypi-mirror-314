# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utils."""

from flask import request

from invenio_banners.services.config import BannerModel


def get_active_banners_for_request():
    """Get active banner for the current URL path request."""
    url_path = request.path
    return BannerModel.get_active(url_path)


def style_category(category):
    """Return predefined Semantic-UI classes for each banner category."""
    style_class = "ui {} flashed top attached manage m-0 message"
    if category == "warning":
        style_class = style_class.format("warning")
    elif category == "other":
        style_class = style_class.format("grey")
    else:
        style_class = style_class.format("info")
    return style_class
