#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : middleware
# Author  : zhoubohan
# Date    : 2024/12/11
# Time    : 10:51
# Description :
"""
import os
import uuid
import time

import bcelogger
from bceiam.bce_client_configuration import BceClientConfiguration
from bceiam.middleware.auth import const
from bceserver.auth.consts import GLOBAL_AUTH_INFO_KEY
from fastapi import Request, HTTPException, status
from resourcev1.client.resource_api import Record, CreateRecordRequest
from resourcev1.client.resource_client import ResourceClient

_available_metrics = ["multimodal_count"]


def get_multimodal_count_default_record(object_id: str) -> Record:
    """Get multimodal count default record."""
    return Record(
        uuid=str(uuid.uuid4()).replace("-", ""),
        metric="multimodal_count",
        value="1",
        objectType="multimodal",
        objectID=object_id,
        timestamp=int(time.time()),
    )


def get_resource_dependency(config: BceClientConfiguration, metric: str):
    """Get resource dependency."""
    if metric not in _available_metrics:
        raise Exception(f"metric {metric} is not available")

    async def resource(request: Request):
        """Subscription dependency."""
        try:
            record = Record()
            if metric == "multimodal_count":
                record = get_multimodal_count_default_record(
                    os.environ.get("ENDPOINT_NAME", "")
                )

            auth_info_context = getattr(request.state, GLOBAL_AUTH_INFO_KEY, None)
            bcelogger.info(
                f"[ResourceMiddleware]auth_info_context: {auth_info_context}"
            )
            if auth_info_context is None:
                bcelogger.error("[ResourceMiddleware]auth info context is None")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "code": "Unauthorized",
                        "message": "[ResourceMiddleware]auth info context is None",
                    },
                )

            org_id = auth_info_context.get(const.ORG_ID, "")
            user_id = auth_info_context.get(const.USER_ID, "")
            if len(org_id) == 0 or len(user_id) == 0:
                bcelogger.error("[ResourceMiddleware]org_id or user_id is empty")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "code": "Unauthorized",
                        "message": "[ResourceMiddleware]org_id or user_id is empty",
                    },
                )

            resource_client = ResourceClient(
                endpoint=config.endpoint,
                context={const.ORG_ID: org_id, const.USER_ID: user_id},
            )

            resource_client.create_record(CreateRecordRequest(records=[record]))
            bcelogger.info(
                f"[ResourceMiddleware]create record: {record} org_id: {org_id} user_id: {user_id}"
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e

            bcelogger.error(f"[ResourceMiddleware]internal err: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "InternalServerError",
                    "message": f"[ResourceMiddleware]internal err: {str(e)}",
                },
            )

    return resource
