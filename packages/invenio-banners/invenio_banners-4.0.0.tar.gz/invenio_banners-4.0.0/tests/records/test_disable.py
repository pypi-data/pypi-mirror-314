# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test disable expired."""

from datetime import datetime, timedelta

from invenio_banners.records.models import BannerModel

banners = {
    "valid": {
        "message": "valid",
        "url_path": "/valid",
        "category": "warning",
        "end_datetime": datetime.utcnow() + timedelta(days=1),
        "active": True,
    },
    "everywhere": {
        "message": "everywhere",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "sub_records_only": {
        "message": "sub_records_only",
        "url_path": "/resources/sub",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "expired": {
        "message": "expired",
        "url_path": "/expired",
        "category": "info",
        "end_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
}


def test_disable_expired(app):
    """Test clean up old announcement but still active."""
    BannerModel.create(banners["everywhere"])
    BannerModel.create(banners["expired"])
    BannerModel.create(banners["valid"])
    BannerModel.create(banners["sub_records_only"])

    assert BannerModel.query.filter(BannerModel.active.is_(True)).count() == 4

    BannerModel.disable_expired()

    _banners = BannerModel.query.filter(BannerModel.active.is_(True)).all()
    assert len(_banners) == 3
    assert _banners[0].message == "everywhere"
    assert _banners[1].message == "valid"
    assert _banners[2].message == "sub_records_only"
