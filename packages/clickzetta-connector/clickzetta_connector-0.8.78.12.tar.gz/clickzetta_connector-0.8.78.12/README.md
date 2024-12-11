# clickzetta-connector


`clickzetta-connector` 是云器 ClickZetta Lakehouse 的基础 Python SDK，提供遵循 PEP-249 规范的 Database API 调用接口以及批量数据上传（bulkload）功能。


安装
```shell
pip install clickzetta-connector
```


## 执行 SQL


一个简单示例
```python
from clickzetta import connect


# 建立连接
conn = connect(username='username',
               password='password',
               service='api.clickzetta.com',
               instance='instance',
               workspace='quickstart_ws',
               schema='public',
               vcluster='default')


# 执行 SQL
cursor = conn.cursor()
cursor.execute('select * from clickzetta_sample_data.ecommerce_events_history.ecommerce_events_multicategorystore_live limit 10;')


# 获取结果
results = cursor.fetchall()
for row in results:
    print(row)
```


## 使用 SQL hints


在 JDBC 中通过 set 命令设置的 SQL hints，使用 cursor 接口时可以通过 parameters 参数传递 hints，示例


```python
# 设置作业运行超时时间为 30 秒
my_param = dict()
my_param['hints'] = dict()
my_param['hints']['sdk.job.timeout'] = 30
cursor.execute('...', parameters=my_param)
```



