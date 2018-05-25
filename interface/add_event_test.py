#引入单元测试模块
import unittest
#引入请求模块
import requests
#引入os和sys
import os, sys
#获取当前文件的地址的前两级，到/Users/ericzhang/Desktop/pyrequest-master'
#最里层嵌套 返回规范化的绝对路径/Users/ericzhang/Desktop/pyrequest-master／interface/add_event_test.py
#第二层嵌套返回/Users/ericzhang/Desktop/pyrequest-master／interface
#so第三层嵌套返回/Users/ericzhang/Desktop/pyrequest-master
#感觉和前边的方法差不多
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#在path的开始位置插入上边的目录
sys.path.insert(0, parentdir)
#'/Users/ericzhang/Desktop/pyrequest-master'


#之前的那个是为了拼接地址，这个可能是为了全局倒入
from db_fixture import test_data


class AddEventTest(unittest.TestCase):
    ''' 添加发布会 '''

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_add_event/'
        #app_key
        self.api_key = '&Guest-Bugmaster'
        #当前时间
        now_time = time()
        #当前时间得到点前的内容
        self.client_time = str(now_time).split('.')[0]
        #sign
        md5 = hashlib.md5()
        #拼接sign验证字符串
        sign_str = self.client_time + self.api_key
        #转化成utf8编码
        sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
        #添加到md5
        md5.update(sign_bytes_utf8)
        #加密
        self.sign_md5 = md5.hexdigest()

    def tearDown(self):
        print(self.result)

    '''如何签名参数为空'''
    def test_add_event_sign_null(self):
        '''签名参数为空'''
        payload = {'eid':1,":",'limit':'','address':'','start_time':'','time':'','sign':''}
        '''发送请求通知'''
        r = requests.post(self.base_url,data = payload)
        '''得到请求结果'''
        result = r.json()
        #写断言
        self.assertEqual(result['status'],10011)
        self.assertEqual(result['message'],'user sign null')

  '''请求超时'''
    def test_add_event_time_out(self):
        '''弄一个超时的时间'''
        now_time = str(int[self.client_time] - 61)
        payload = {'eid':1,":",'limit':'','address':'','start_time':'','time':now_time,'sign':'abc'}
        r = requests.post(self.base_url,data = payload)
        result = r.json()
        self.assertEqual(result['status'],10012)
        self.assertEqual(result['message'],'user sign timeout')


  '''签名错误'''
    def test_add_event_sign_error(self):
        '''签名错误'''
        payload= {'eid':1,":",'limit':'','address':'','start_time':'','time':self.client_time,'sign':'abc'}
        r = requests.post(self.base_url,data = payload)
        result = r.json()
        self.assertEqual(result['status'],10013)
        self.assertEqual(result['message'],'user sign error')

    def test_add_event_all_null(self):
        ''' 所有参数为空 '''
        payload = {'eid':'','':'','limit':'','address':"",'start_time':''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertEqual(self.result['message'], 'parameter error')

    def test_add_event_eid_exist(self):
        ''' id已经存在 '''
        payload = {'eid':1,'name':'一加4发布会','limit':2000,'address':"深圳宝体",'start_time':'2017'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertEqual(self.result['message'], 'event id already exists')

    def test_add_event_name_exist(self):
        ''' 名称已经存在 '''
        payload = {'eid':11,'name':'红米Pro发布会','limit':2000,'address':"深圳宝体",'start_time':'2017'}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertEqual(self.result['message'], 'event name already exists')

    def test_add_event_data_type_error(self):
        ''' 日期格式错误 '''
        payload = {'eid':11,'name':'一加4手机发布会','limit':2000,'address':"深圳宝体",'start_time':'2017'}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('start_time format error.', self.result['message'])

    def test_add_event_success(self):
        ''' 添加成功 '''
        payload = {'eid':11,'name':'一加4手机发布会','limit':2000,'address':"深圳宝体",'start_time':'2017-05-10 12:00:00'}
        r = requests.post(self.base_url,data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')





if __name__ == '__main__':
    test_data.init_data() # 初始化接口测试数据
    #通过unittest调用main函数
    unittest.main()
