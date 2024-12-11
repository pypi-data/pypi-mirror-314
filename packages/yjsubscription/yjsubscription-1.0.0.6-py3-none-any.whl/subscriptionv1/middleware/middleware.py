#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time    : 2024/12/11 下午14:45
# @Author  : zhoubohan
# @File    : middleware/middleware.py
# @Software: PyCharm
"""
import bcelogger
from fastapi import Request, HTTPException, status
from bceserver.conf.conf import Config, GLOBAL_CONFIG_KEY
from bceserver.auth.consts import GLOBAL_AUTH_INFO_KEY
from bceserver.context.singleton_context import SingletonContext
from bceidaas.middleware.auth import const
from subscriptionv1.client.subscription_client import SubscriptionClient
from subscriptionv1.client.subscription_api import CheckEquityRequest


def get_subscription_dependency(
    config: Config,
    equity_id: str,
):
    """Get subscription dependency."""
    context = SingletonContext.instance()
    context.set_var_value(GLOBAL_CONFIG_KEY, config)

    async def subscription(request: Request):
        """Subscription dependency."""
        try:
            auth_info_context = getattr(request.state, GLOBAL_AUTH_INFO_KEY, None)
            bcelogger.info(
                f"[SubscriptionMiddleware]auth_info_context: {auth_info_context}"
            )
            if auth_info_context is None:
                bcelogger.error("[SubscriptionMiddleware]auth info context is None")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "code": "Unauthorized",
                        "message": "[SubscriptionMiddleware]auth info context is None",
                    },
                )

            org_id = auth_info_context.get(const.ORG_ID, "")
            user_id = auth_info_context.get(const.USER_ID, "")
            if len(org_id) == 0 or len(user_id) == 0:
                bcelogger.error("[SubscriptionMiddleware]org_id or user_id is empty")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "code": "Unauthorized",
                        "message": "[SubscriptionMiddleware]org_id or user_id is empty",
                    },
                )

            sub_client = SubscriptionClient(
                endpoint=config.subscription.endpoint,
                context={const.ORG_ID: org_id, const.USER_ID: user_id},
            )

            resp = sub_client.check_equity(CheckEquityRequest(equityId=equity_id))
            bcelogger.info(
                f"[SubscriptionMiddleware]check equity response: {resp} org_id: {org_id} user_id: {user_id}"
            )
            if resp is None or resp.checkResult not in ["Valid", "ValidUsedUp"]:
                bcelogger.warning(
                    f"[SubscriptionMiddleware]check equity failed: {resp.checkResult} org_id: {org_id}"
                    + " user_id: {user_id}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "code": "Forbidden",
                        "message": f"[SubscriptionMiddleware]check equity failed: {resp.checkResult} org_id: {org_id}"
                        + " user_id: {user_id}",
                    },
                )
        except Exception as e:
            bcelogger.error(f"[SubscriptionMiddleware]internal err: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "InternalServerError",
                    "message": f"[SubscriptionMiddleware]internal err: {str(e)}",
                },
            )

    return subscription
