# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner services conftest."""

import pytest


@pytest.fixture()
def superuser_identity(admin):
    """Superuser identity fixture."""
    identity = admin.identity
    return identity


@pytest.fixture()
def simple_user_identity(user):
    """Simple identity fixture."""
    identity = user.identity
    return identity
