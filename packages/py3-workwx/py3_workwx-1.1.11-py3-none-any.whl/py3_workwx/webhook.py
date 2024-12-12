#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py_usefully
=================================================
"""
from typing import Union

from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response
import py3_requests

validator_json_schema = Dict()
validator_json_schema.normal = Dict({
    "type": "object",
    "properties": {
        "errcode": {
            "oneOf": [
                {"type": "integer", "const": 0},
                {"type": "string", "const": "0"},
            ]
        }
    },
    "required": ["errcode"],
})


def normal_response_handler(response: Response = None):
    if isinstance(response, Response) and response.status_code == 200:
        json_addict = Dict(response.json())
        if Draft202012Validator(validator_json_schema.normal.to_dict()).is_valid(instance=json_addict):
            return json_addict.get("media_id", True)
        return None
    raise Exception(f"response handler error {response.status_code}|{response.text}")


class Webhook:
    """

    企业微信 群机器人

    @see https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(self, base_url: str = "https://qyapi.weixin.qq.com/", key: str = "",
                 mentioned_list: Union[tuple, list] = [],
                 mentioned_mobile_list: Union[tuple, list] = []):
        """
        企业微信 群机器人

        @see https://developer.work.weixin.qq.com/document/path/91770
        :param base_url: 基础 url
        :param key: 群机器人 key
        :param mentioned_list: userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
        :param mentioned_mobile_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        """
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.key = key
        self.mentioned_list = mentioned_list
        self.mentioned_mobile_list = mentioned_mobile_list

    def send_text_formatter(self, content: str = "", mentioned_list: Union[tuple, list] = [],
                            mentioned_mobile_list: Union[tuple, list] = []):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :return:
        """
        return Dict({
            "msgtype": "text",
            "text": {
                "content": f"{content}",
                "mentioned_list": self.mentioned_list + mentioned_list,
                "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list
            }
        })

    def send_markdown_formatter(self, content: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#markdown%E7%B1%BB%E5%9E%8B
        :param content:
        :return:
        """
        return Dict({
            "msgtype": "markdown",
            "markdown": {
                "content": f"{content}"
            }
        })

    def send_image_formatter(self, image_base64: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E7%89%87%E7%B1%BB%E5%9E%8B
        :param image_base64:
        :return:
        """
        return Dict({
            "msgtype": "image",
            "image": {
                "base64": f"{image_base64}",
                "md5": "MD5"
            }
        })

    def send_news_formatter(self, articles: Union[tuple, list] = []):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E6%96%87%E7%B1%BB%E5%9E%8B
        :param articles:
        :return:
        """
        return Dict({
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        })

    def send_template_card_formatter(self, template_card: dict = {}):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%A8%A1%E7%89%88%E5%8D%A1%E7%89%87%E7%B1%BB%E5%9E%8B
        :param template_card:
        :return:
        """
        return Dict({
            "msgtype": "template_card",
            "template_card": template_card
        })

    def send_file_formatter(self, media_id: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E7%B1%BB%E5%9E%8B
        :param media_id:
        :return:
        """
        return Dict({
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        })

    def send_voice_formatter(self, media_id: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E8%AF%AD%E9%9F%B3%E7%B1%BB%E5%9E%8B
        :param media_id:
        :return:
        """
        return Dict({
            "msgtype": "voice",
            "voice": {
                "media_id": media_id
            }
        })

    def send(self, **kwargs):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770
        :param kwargs: py_usefully.requests.request kwargs
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("response_handler", normal_response_handler)
        kwargs.setdefault("url", f"/cgi-bin/webhook/send")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("params", Dict())
        kwargs.params.setdefault("key", self.key)
        return py3_requests.request(
            **kwargs.to_dict()
        )

    def upload_media(self, **kwargs):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%8E%A5%E5%8F%A3
        :param kwargs: py_usefully.requests.request kwargs
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", normal_response_handler)
        kwargs.setdefault("params", Dict({}))
        kwargs.params.setdefault("key", self.key)
        kwargs.params.setdefault("type", "file")
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", f"/cgi-bin/webhook/upload_media")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        return py3_requests.request(
            **kwargs.to_dict()
        )
