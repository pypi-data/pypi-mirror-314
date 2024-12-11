# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from itertools import chain
import json

from ngcbase.api.pagination import pagination_helper_header_page_reference
from ngcbase.util.utils import format_org_team

PAGE_SIZE = 100


class InfiniBandPartitionAPI:  # noqa: D101
    def __init__(self, api_client):
        self.connection = api_client.connection
        self.client = api_client

    @staticmethod
    def _get_infiniband_partition_endpoint(org_name=None, team_name=None):
        org_team = format_org_team(org_name, team_name, plural_form=False)
        return "/".join(["v2", org_team, "forge", "infiniband-partition"])

    def list(self, org_name, team_name, site, target, status):  # noqa: D102
        ep = self._get_infiniband_partition_endpoint(org_name, team_name)
        params = []
        if site:
            params.append(f"siteId={site}")
        if target:
            params.append(f"query={target}")
        if status:
            params.append(f"status={status}")
        params.append("includeRelation=Tenant")
        params.append("includeRelation=Site")
        # params.append("includeRelation=VPC")
        params.append("orderBy=UPDATED_DESC")
        params.append(f"pageSize={PAGE_SIZE}")
        query = "?".join([ep, "&".join(params)])
        return chain(
            *[
                res
                for res in pagination_helper_header_page_reference(
                    self.connection,
                    query,
                    org_name=org_name,
                    team_name=team_name,
                    operation_name="list_infiniband_partition",
                )
                if res
            ]
        )

    def info(self, org_name, team_name, infiniband_partition):  # noqa: D102
        ep = self._get_infiniband_partition_endpoint(org_name, team_name)
        url = f"{ep}/{infiniband_partition}"
        params = []
        params.append("includeRelation=Tenant")
        params.append("includeRelation=Site")
        # params.append("includeRelation=VPC")
        query = "?".join([url, "&".join(params)])
        resp = self.connection.make_api_request(
            "GET", query, auth_org=org_name, auth_team=team_name, operation_name="info_infiniband_partition"
        )
        return resp

    def create(  # noqa: D102
        self,
        org_name,
        team_name,
        name,
        description,
        site,
    ):
        url = self._get_infiniband_partition_endpoint(org_name, team_name)
        create_obj = {
            "name": name,
            "description": description,
            "siteId": site,
        }
        resp = self.connection.make_api_request(
            "POST",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(create_obj),
            operation_name="create_infiniband_partition",
        )
        return resp

    def update(self, org_name, team_name, infiniband_partition, name, description):  # noqa: D102
        ep = self._get_infiniband_partition_endpoint(org_name, team_name)
        url = f"{ep}/{infiniband_partition}"
        update_obj = {
            "name": name,
            "description": description,
        }
        resp = self.connection.make_api_request(
            "PATCH",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(update_obj),
            operation_name="update_infiniband_partition",
        )
        return resp

    def remove(self, org_name, team_name, infiniband_partition):  # noqa: D102
        ep = self._get_infiniband_partition_endpoint(org_name, team_name)
        url = f"{ep}/{infiniband_partition}"
        resp = self.connection.make_api_request(
            "DELETE",
            url,
            auth_org=org_name,
            auth_team=team_name,
            operation_name="remove_infiniband_partition",
            json_response=False,
        )
        return resp


class GuestInfiniBandPartitionAPI(InfiniBandPartitionAPI):  # noqa: D101
    pass
