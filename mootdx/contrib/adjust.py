import json
import re

import numpy as np
import pandas as pd
import httpx

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Referer': 'http://stockpage.10jqka.com.cn/',
    'DNT': '1',
}

# 00 不复权 01前复权 02后复权
# factor = before after
# http://d.10jqka.com.cn/v2/line/hs_600036/01/2018.js
# http://d.10jqka.com.cn/v6/line/hs_600000/00/all.js


def get_adjust_year(symbol=None, year='2021', factor='00'):
    if factor == 'before':
        factor = '01'
    elif factor == 'after':
        factor = '02'
    else:
        factor = '00'

    url = f'http://d.10jqka.com.cn/v2/line/hs_{symbol}/{factor}/{year}.js'

    res = httpx.get(url, headers=headers)

    if res.status_code != 200:
        return None

    text = re.findall(r'\((.*)\)', res.text)[0]
    text = json.loads(text)

    data = text['data'].split(';')
    data = [item.split(',')[:8] for item in data]

    columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'factor']
    return pd.DataFrame(data, index=list(np.asarray(data).T[0]), columns=columns)
