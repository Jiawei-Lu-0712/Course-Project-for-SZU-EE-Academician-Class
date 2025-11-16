import requests
import matplotlib.pyplot as plt

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
timestamps = []
prices = []
for item in data:
    # 提取时间戳和价格数据
    timestamp = item['date']
    price = item['close']
    # 添加到相应的列表中
    timestamps.append(timestamp)
    prices.append(price)

# 使用 matplotlib 绘制柱状图
plt.bar(timestamps, prices)
plt.xlabel('时间戳')
plt.ylabel('价格')
plt.title('比特币价格变化')
plt.show()
