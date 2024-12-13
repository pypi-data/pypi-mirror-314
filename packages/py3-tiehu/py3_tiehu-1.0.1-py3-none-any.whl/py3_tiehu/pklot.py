#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_tiehu
=================================================
"""
import hashlib
import json
from datetime import datetime

import py3_requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response

request_urls = Dict()
request_urls.cxzn_interface_queryPklot = "/cxzn/interface/queryPklot"
request_urls.cxzn_interface_getParkCarType = "/cxzn/interface/getParkCarType"
request_urls.cxzn_interface_getParkCarModel = "/cxzn/interface/getParkCarModel"
request_urls.cxzn_interface_payMonthly = "/cxzn/interface/payMonthly"
request_urls.cxzn_interface_addVisit = "/cxzn/interface/addVisit"
request_urls.cxzn_interface_lockCar = "/cxzn/interface/lockCar"
request_urls.cxzn_interface_getParkinfo = "/cxzn/interface/getParkinfo"
request_urls.cxzn_interface_addParkBlack = "/cxzn/interface/addParkBlack"
request_urls.cxzn_interface_delParkBlacklist = "/cxzn/interface/delParkBlacklist"
request_urls.cxzn_interface_getParkGate = "/cxzn/interface/getParkGate"
request_urls.cxzn_interface_openGate = "/cxzn/interface/openGate"
request_urls.cxzn_interface_saveMonthlyRent = "/cxzn/interface/saveMonthlyRent"
request_urls.cxzn_interface_delMonthlyRent = "/cxzn/interface/delMonthlyRent"
request_urls.cxzn_interface_getMonthlyRent = "/cxzn/interface/getMonthlyRent"
request_urls.cxzn_interface_getMonthlyRentList = "/cxzn/interface/getMonthlyRentList"
request_urls.cxzn_interface_delMonthlyRentList = "/cxzn/interface/delMonthlyRentList"
request_urls.cxzn_interface_getParkDeviceState = "/cxzn/interface/getParkDeviceState"
request_urls.cxzn_interface_upatePlateInfo = "/cxzn/interface/upatePlateInfo"
request_urls.cxzn_interface_getParkBlackList = "/cxzn/interface/getParkBlackList"
request_urls.cxzn_interface_deleteVisit = "/cxzn/interface/deleteVisit"

validator_json_schemas = Dict()
validator_json_schemas.normal = Dict({
    "type": "object",
    "properties": {
        "status": {
            "oneOf": [
                {"type": "integer", "const": 1},
                {"type": "string", "const": "1"},
            ]
        },
    },
    "required": ["status", "Data"]
})


def normal_response_handler(response: Response = None):
    if isinstance(response, Response) and response.status_code == 200:
        json_addict = Dict(response.json())
        if Draft202012Validator(validator_json_schemas.normal).is_valid(instance=json_addict):
            return Dict(json.loads(json_addict.get("Data", "")))
        return None
    raise Exception(f"Response Handler Error {response.status_code}|{response.text}")


class Pklot(object):
    """
    @see https://www.showdoc.com.cn/1735808258920310/9467753400037587
    """

    def __init__(
            self,
            base_url: str = "",
            parking_id: str = "",
            app_key: str = ""
    ):
        """
        @see https://www.showdoc.com.cn/1735808258920310/9467753400037587
        :param base_url:
        :param parking_id:
        :param app_key:
        """

        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.parking_id = parking_id
        self.app_key = app_key

    def signature(self,data: dict = {}):
        """
        @see https://www.showdoc.com.cn/1735808258920310/8113601111753119
        :param data:
        :return:
        """
        temp_string = ""
        data = Dict(data)
        if data.keys():
            data_sorted = sorted(data.keys())
            if isinstance(data_sorted, list):
                temp_string = "&".join([
                    f"{i}={data[i]}"
                    for i in
                    data_sorted if
                    i != "appKey"
                ]) + f"{hashlib.md5(self.app_key.encode('utf-8')).hexdigest().upper()}"
        return hashlib.md5(temp_string.encode('utf-8')).hexdigest().upper()

    def request_with_signature(self,**kwargs):
        """
        request with signature
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("response_handler", normal_response_handler)
        kwargs.setdefault("url", "")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("json", Dict())
        timestamp = int(datetime.now().timestamp())
        kwargs["json"] = {
            **{
                "parkingId": self.parking_id,
                "timestamp": timestamp,
                "sign": self.signature({
                    "parkingId": self.parking_id,
                    "timestamp": timestamp,
                })
            },
            **kwargs["json"],
        }
        return py3_requests.request(
            **kwargs.to_dict()
        )
