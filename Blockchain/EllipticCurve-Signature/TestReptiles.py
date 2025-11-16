import requests

url = 'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start=1546300800&end=1546646400&period=14400'

# 设置超时时间和最大重试次数
timeout = 5
max_retries = 3

# 使用 Session 对象进行请求
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
session.mount('https://', adapter)

# 发送 GET 请求获取 API 数据，设置超时时间
response = session.get(url, timeout=timeout)

# 解析 API 数据
data = response.json()

# 提取比特币价格变化数据
for item in data:
    timestamp = item['date']
    open_price = item['open']
    high_price = item['high']
    low_price = item['low']
    close_price = item['close']
    volume = item['volume']
    quote_volume = item['quoteVolume']
    weighted_average = item['weightedAverage']

    # 打印比特币价格变化数据
    print('时间戳：', timestamp)
    print('开盘价：', open_price)
    print('最高价：', high_price)
    print('最低价：', low_price)
    print('收盘价：', close_price)
    print('交易量：', volume)
    print('报价交易量：', quote_volume)
    print('加权平均价：', weighted_average)
    print('---' * 10)
