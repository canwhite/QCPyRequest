import time, sys
#先将三方modlue路径导入
sys.path.append('./interface')
sys.path.append('./db_fixture')
#然后就可以导入具体的内容了
from db_fixture import test_data
#这个是个html输出框架
from HTMLTestRunner import HTMLTestRunner
#导入单元测试库
import unittest




# 指定测试用例为当前文件夹下的 interface 目录
test_dir = './interface'
#单元测试文件，发现加载
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')





if __name__ == "__main__":
    
    # 初始化接口测试数据
    test_data.init_data()
    # 得到一个当前时间，用于后边拼接report文件
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    
    #./指的是当前目录，整体意思就是,当前目录下的report目录里新建文件
    
    filename = './report/' + now + '_result.html'
    #文件操作用内建函数：open()
    #格式：F＝open(filename,访问方式[r,w,a,b]) ## r:读操作；w：写操作；a:添加操作；b:二进制存取操作
    #open可以访问任何形式的文件，在访问非文本格式文件（二进制文件）的时候，访问模式通常加上‘b’（即二进制模式：‘rb’或‘wb’），但并不必须，依情况而定
    #路径是填写在前面的filename参数处的
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='Guest Manage System Interface Test Report',
                            description='Implementation Example with: ')
    runner.run(discover)
    fp.close()
