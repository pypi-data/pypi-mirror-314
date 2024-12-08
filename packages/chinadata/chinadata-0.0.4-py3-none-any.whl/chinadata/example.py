#
"""
1、安装对应库
pip install chinadata

"""
#2、
import  chinadata.ca_data as ts
pro = ts.pro_api('9e84ed87f29cf43f0a84c98cef6a69cc00')

#查询当前所有正常上市交易的股票列表
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
print(data)
#查询基金列表，
ts.set_token('9e84ed87f29cf43f0a84c98cef6a69cc00')
data = (pro.fund_basic( fields='ts_code,symbol,name,area,industry,list_date'))
print(data)

