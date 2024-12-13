#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : videos
# @Time         : 2024/12/12 08:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.schemas.siliconflow_types import BASE_URL, VideoRequest
from meutils.config_utils.lark_utils import get_next_token_for_polling

from openai import OpenAI, AsyncOpenAI


async def create_task(request: VideoRequest, token: Optional[str] = None):
    token = token or await get_next_token_for_polling(FEISHU_URL_FREE)

    payload = request.model_dump(exclude_none=True)

    client = OpenAI(
        base_url=BASE_URL,
        api_key=token
    )

    resp = client.post("/video/submit", cast_to=object, body=payload)
    return resp  # {'requestId': 'e6fdd5d6-288f-45b4-a760-ead691c43ca9'}


if __name__ == '__main__':
    token = "sk-raapiguffsnsxgkfiwfusjmbpcyqoxhcohhxaybflrnvpqjw"
    arun(create_task(VideoRequest(model="tencent/HunyuanVideo", prompt="a dog in the forest"), token=token))
