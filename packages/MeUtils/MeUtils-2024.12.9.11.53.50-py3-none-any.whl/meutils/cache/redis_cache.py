#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : redis_cache
# @Time         : 2024/12/6 10:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :  https://hermescache.readthedocs.io/en/latest/
# https://mp.weixin.qq.com/s/-T2UmkinmtQoNQo4DVpnfw

from meutils.pipe import *

import hermes.backend.redis

cache = hermes.Hermes(
    hermes.backend.redis.Backend,
    ttl=600,
    host='localhost',
    db=1,
)

if __name__ == '__main__':
    pass


    # ttl: Optional[int] = None,
    # tags: Sequence[str] = (),
    # key: Optional[Callable] = None,
    @cache(ttl=100, key=lambda fn, a, b: (a, b))
    def func(x, y):
        logger.debug('xxxxxxx')
        return x
