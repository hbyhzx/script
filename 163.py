"""
批量爬取音乐数据 - js逆向
"""
import requests
import re
import random
from Crypto.Cipher import AES
import base64
from binascii import hexlify
 
 
def RSA1(text):
    '''
    RSA加密
    :param text: 需要加密的密文
    :return:
    '''
    f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    e = "010001"
    text = text[::-1]  # 倒序
    # 返回二进制数据的16进制表示
    #  pow(x, y) x的y次方  int(e, 进制)
    #  创建RSA对象  => 加密结果  压缩
    #  位运算 (排序算法)
    result = pow(int(hexlify(text.encode()), 16), int(e, 16), int(f, 16))
    # 131的压缩
    return format(result, 'x').zfill(131)
 
 
 
def RandomString(a):
    '''
    随机返回16位字符串 JS代码里面的a(16) i
    :param a:
    :return:
    '''
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    randomStr = random.sample(string, a)
    # 返回i值
    return "".join(randomStr)
 
 
def AESEncrypt(text, key):
    '''
    AES加密
    :param text: 需要加密的密文
    :param key: 秘钥
    :return:
    '''
    # 初识向量 ->字节
    iv = b'0102030405060708'
    # 填充  AES 秘钥 16位  目的: 保障秘钥的长度符合 填充 删除
    #  16位数据  转变bytes
    pad = 16 - len(text) % 16
    text = text + chr(2) * pad
    # 创建 AES对象
    encryptor = AES.new(key.encode(), AES.MODE_CBC, iv)
    # AES 进行加密
    encryptor_str = encryptor.encrypt(text.encode())
 
    result = base64.b64encode(encryptor_str).decode()
    return result
 
 
def AES2(text, random_str):
    '''
    第二次AES加密
    :param text: 加密的密文
    :param random_str: 随机16位字符串
    :return:
    '''
    # 第一次加密 (d, g)
    first_aes = AESEncrypt(text, key='0CoJUm6Qyw8W8jud')
    # 第二次加密 把第一次加密内容 + 秘钥为i(随机16个字符串)
    second_aes = AESEncrypt(first_aes, random_str)
    return second_aes  # params
 
 
url = 'https://music.163.com/discover/toplist'
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'NMTID=00OnNx-ny-kGbRsNEcep3LZ4lp8rpQAAAGJHyiZjA; _iuqxldmzr_=32; _ntes_nnid=905353327d062d6526bf30b7313fc5fa,1688444903810; _ntes_nuid=905353327d062d6526bf30b7313fc5fa; WEVNSM=1.0.0; WNMCID=zrwecq.1688444905061.01.0; WM_TID=PeeAqr7XWZFARBQRBReE10P7HdXIZJwJ; ntes_utid=tid._.bhRazRNlzqJER1EFQUOFx0bqDcCdMvmK._.0; sDeviceId=YD-XKNffsyyp2pBR1VBEAbEhe8QaJRr0Cbf; __snaker__id=aezpEfQ4aSswGdU3; gdxidpyhxdE=SEKQwGBos3%5C%2B2UtNl14glU02Dqnb%2FupjfqqAehCtobxgdJCD6fs%2FzKhCBn0wv1ywjn%2FLE%2F2aJHljc9v1p5VRgzCM%5C5k1%2B6d2xRVWy3WNQvGRPxx6%5CZalKnZpxcblgpp7d6IR97dbijA37gRQn%2FaOPfWpVOjhbu6Mr3EGl2jVE4q%5C6mnb%3A1704278718014; WM_NI=w22ZFzjDTX%2FJZtIOltqVT1QGG1YaYihbD034dlfiAFJ4AJ1UgJ9p42ZEWBFkYXzBytP88iaMWTxXYCqQZz7drUYEzv%2BPW5hi4LFmiPIZ%2BlzT9iKZcesO7KrdITR26fdUdkU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee88f079b6ef9ed1ee6f9b968fb7d15f869e8badc479b096f7a8dc7b829f8986b62af0fea7c3b92ab5eefebbc572aa9c9cb9ae429aac87b0ef80b38a9cd2d44d85ef9782dc63acbe8cd1b240a8b4aa8ac44e8aec8fabb45fa596f791b73a9a9b99a3c5619b88b6a3fc8094e8f88ae447958cb8b9dc49b38f969bb670b28b97a6f97ee99099d6eb63f8948a8eec5c8b86e58df960fbb785bbe26fb191f9acf1708b8c9ed3b56ea88bac8cd837e2a3; JSESSIONID-WYYY=71x89Yv74dCK8UKsi7Gs1e444CRF0R3hipD8nGvNel2e8qNT09wHV6fIAcb9mkY%2F6ayOFNW7t3cgb6NVWhoD9Yu9XiuXoQ7W%2Fl8kEyZynFOKzY8Vv5QrlBx4s%2B9ZWXFKrtdzjo%2BKWAyeE%5ClN9Cu%2FM9WCPq1J5KaDwyE5XZUaSdpciVjK%3A1705501419446; playerid=56188857'
}
 
res = requests.get(url, headers=headers)
 
ids = re.findall(r'"/song\?id=(\d+)"', res.text)    # 所有音乐的id
names = re.findall(r'<a href="/song\?id=\d+">(.*?)</a>', res.text)   # 所有音乐的名字
# print(names)
for i, n in zip(ids, names):
    # print(i, n)
    # d值
    text = '{"ids":"[%s]","level":"standard","encodeType":"aac","csrf_token":""}' % i
    # 生成随机16位字符串
    random_str = RandomString(16)
    # 第一次AES加密的结果返回
    # text2 = AESEncrypt(text, key)
    # AES加密
    params = AES2(text, random_str)
    encSecKey = RSA1(random_str)
 
 
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
 
    data = {
        'params': params,
        'encSecKey': encSecKey,
    }
    try:
        response = requests.post(url, headers=headers, data=data).json()
        mp3_url = response.get('data')[0].get('url')
        # print(mp3_url)
        if mp3_url != None:
            res_mp3 = requests.get(mp3_url)
            open('%s.mp3' % n, 'wb').write(res_mp3.content)
            print('%s歌曲下载成功' % n)
    except Exception:
        pass
