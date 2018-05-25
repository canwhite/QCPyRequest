#Interface_AES_test.py
from Crypto.Cipher import AES
import base64
import requests
import unittest
import json


class AESTest(unittest.TestCase):

    #数据初始化
    def setUp(self):
        BS = 16
        #函数式编程的一种，通过lambda定义匿名函数对字符串进行补足，使其长度为16的，一直加乘直到没有余数
        self.pad = lambda s: s + (BS - len(s) % BS) *chr(BS - len(s) % BS)
        self.base_url = 'http://127.0.0.1:8000/sign/sec_get_guest_list/'
        self.app_key = 'W7v4D60fds2Cmk2U'


    #base64加密
    def encryptBase64(self,src):
        return base64.urlsafe_b64encode(src)


    #AES加密
    def encryptAES(self,src,key):
        '''生成AES密文'''
        iv = b'1172311105789011'
        cryptor = AES.new(key,AES.MODE_CBC,iv)
        ciphertext = cryptor.encrypt(self.pad(src))
        #最后再通过base64加密一下
        return self.encryptBase64(ciphertext)


    #测试AES方法
    def test_aes_interface(self):

        payload = {'eid':'1','phone':'13800138000'}
        #加密,app_key只需要自己知道，decode()默认utf-8解码
        #可以从这里看出来我们是把参数给加密了
        encoded = self.encryptAES(json.dump(payload),self.app_key).decode()

        r = requests.post(self.base_url,data = {"data":encoded})
        result = r.json()
        self.assertEqual(result['status'],200)
        self.assertEqual(result['message'],'success')




