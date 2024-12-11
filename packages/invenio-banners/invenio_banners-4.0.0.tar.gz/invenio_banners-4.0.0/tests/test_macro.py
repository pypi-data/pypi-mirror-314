# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test views."""

from datetime import datetime

import pytest
from flask import url_for

from invenio_banners.records.models import BannerModel
from invenio_banners.utils import style_category


def _create_banner(message, category, url_path=None):
    """Util to create a banner."""
    banner = BannerModel.create(
        {
            "message": message,
            "category": category,
            "url_path": url_path,
            "start_datetime": datetime.utcnow(),
            "active": True,
        }
    )

    return banner


def test_jinja_macro(app, db):
    """Test the rendering of the banner in a template via macro."""

    tpl = """
    <html>
        <body>
            {%- from "semantic-ui/invenio_banners/banner.html" import banner -%}
            {{ banner() }}
        </body>
    </html>
    """
    template = app.jinja_env.from_string(tpl)
    # should be empty, no banners
    html = template.render()
    one_line = html.replace("\n", "").replace(" ", "")
    assert one_line == "<html><body></body></html>"

    # add one banner
    EXPECTED_MSG = "Test banner info message"
    EXPECTED_CATEGORY = "info"
    EXPECTED_STYLE = "ui info flashed top attached manage m-0 message"
    banner = _create_banner(EXPECTED_MSG, EXPECTED_CATEGORY)
    style = style_category(banner.category)

    html = template.render()
    assert EXPECTED_MSG in html
    assert style.endswith(EXPECTED_STYLE)
    assert style in html

    # change message and category
    EXPECTED_MSG = "Test banner warning message"
    EXPECTED_CATEGORY = "warning"
    EXPECTED_STYLE = "ui warning flashed top attached manage m-0 message"

    banner.message = EXPECTED_MSG
    banner.category = EXPECTED_CATEGORY
    db.session.commit()

    style = style_category(banner.category)

    html = template.render()
    assert EXPECTED_MSG in html
    assert style.endswith(EXPECTED_STYLE)
    assert style in html
