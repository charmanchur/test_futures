# coding=UTF-8

import os
import time
import sys
import requests 
from concurrent import futures

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()  # <2>
BASE_URL = 'http://flupy.org/data/flags'  # <3>
DEST_DIR = 'images/'  # <4>

# 设定ThreadPoolExecutor 类最多使用几个线程
MAX_WORKERS = 20

# 保存图片
def save_flag(img, filename):  # <5>
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

# 下载图片
def get_flag(cc):  # <6>
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    # 这里我们使用 requests 包，需要先通过pypi安装
    resp = requests.get(url)
    return resp.content

# 显示一个字符串，然后刷新sys.stdout,目的是在一行消息中看到进度
def show(text):  # <7>
    print(text, end=' ')
    sys.stdout.flush()

# 下载一个图片
def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

# 多线程下载多个图片
def download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        to_do = []
        # 用于创建并排定 future
        for cc in sorted(cc_list):
            # submit 方法排定可调用对象的执行时间然后返回一个future，表示这个待执行的操作
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))
        results = []
        # 用于获取future 结果
        # as_completed 接收一个future 列表，返回值是一个迭代器，在运行结束后产出future
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)
    return len(results)

def main(download_many):  # <10>
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))

if __name__ == '__main__':
    main(download_many)
