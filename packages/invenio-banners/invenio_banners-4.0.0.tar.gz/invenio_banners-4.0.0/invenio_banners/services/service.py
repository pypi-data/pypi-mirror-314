# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner Service API."""

import distutils.util

import arrow
from invenio_db.uow import unit_of_work
from invenio_records_resources.services import RecordService
from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.base.utils import map_search_params
from sqlalchemy import func

from ..records.models import BannerModel


class BannerService(RecordService):
    """Banner Service."""

    def read(self, identity, id):
        """Retrieve a banner."""
        self.require_permission(identity, "read")

        banner = self.record_cls.get(id)

        return self.result_item(
            self,
            identity,
            banner,
            links_tpl=self.links_item_tpl,
        )

    def search(self, identity, params):
        """Search for banners matching the querystring."""
        self.require_permission(identity, "search")

        search_params = map_search_params(self.config.search, params)

        query_param = search_params["q"]
        filters = []

        if query_param:
            filters.extend(
                [
                    BannerModel.url_path.ilike(f"%{query_param}%"),
                    BannerModel.message.ilike(f"%{query_param}%"),
                    BannerModel.category.ilike(f"%{query_param}%"),
                ]
            )
            bool_value = self._validate_bool(query_param)
            if bool_value is not None:
                filters.extend(
                    [
                        BannerModel.active.is_(bool_value),
                    ]
                )

            datetime_value = self._validate_datetime(query_param)
            if datetime_value is not None:
                filters.extend(
                    [
                        func.date(BannerModel.start_datetime) == datetime_value,
                        func.date(BannerModel.end_datetime) == datetime_value,
                        func.date(BannerModel.created) == datetime_value,
                        func.date(BannerModel.updated) == datetime_value,
                    ]
                )

        banners = self.record_cls.search(search_params, filters)

        return self.result_list(
            self,
            identity,
            banners,
            params=search_params,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    @unit_of_work()
    def create(self, identity, data, raise_errors=True, uow=None):
        """Create a banner."""
        self.require_permission(identity, "create")

        # validate data
        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=raise_errors,
        )

        # create the banner with the specified data
        banner = self.record_cls.create(valid_data)

        return self.result_item(
            self, identity, banner, links_tpl=self.links_item_tpl, errors=errors
        )

    @unit_of_work()
    def delete(self, identity, id, uow=None):
        """Delete a banner from database."""
        self.require_permission(identity, "delete")

        banner = self.record_cls.get(id)
        self.record_cls.delete(banner)

        return self.result_item(self, identity, banner, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def update(self, identity, id, data, uow=None):
        """Update a banner."""
        self.require_permission(identity, "update")

        banner = self.record_cls.get(id)

        # validate data
        valid_data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=True,
        )

        self.record_cls.update(valid_data, id)

        return self.result_item(
            self,
            identity,
            banner,
            links_tpl=self.links_item_tpl,
        )

    @unit_of_work()
    def disable_expired(self, identity, uow=None):
        """Disable expired banners."""
        self.require_permission(identity, "disable")
        self.record_cls.disable_expired()

    def _validate_bool(self, value):
        try:
            bool_value = distutils.util.strtobool(value)
        except ValueError:
            return None
        return bool(bool_value)

    def _validate_datetime(self, value):
        try:
            date_value = arrow.get(value).date()
        except ValueError:
            return None
        return date_value
