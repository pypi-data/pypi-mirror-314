# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Errors."""


class BannerNotExistsError(Exception):
    """Banner not found exception."""

    def __init__(self, banner_id):
        """Constructor."""
        self.banner_id = banner_id

    @property
    def description(self):
        """Exception's description."""
        return f"Banner with id {self.banner_id} is not found."
