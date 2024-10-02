import requests
import time
import random
import re

session = requests.Session()
#url模板，需要访问留言板替换url
url_template = "https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1111111111&hostUin=1111111111&num=10&start={start}&hostword=0&essence=1&r={r_value}&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=123456789&g_tk=123456789"

start = 0
#访问qq留言板 复制cookie
cookies = {
    'eas_sid': '',
    'pgv_pvid': '',
    'RK': '',
    'ptcz': '',
    'ptui_loginuin': '1111111111',
    'uin': 'o1111111111',
    'skey': '@',
    'p_uin': 'o1111111111',
    'Loading': 'Yes',
    'qz_screen': '2560x1440',
    '__Q_w_s_hat_seed': '1',
    'pgv_info': 'ssid=s000000000',
    'QZ_FE_WEBP_SUPPORT': '1',
    'cpu_performance_v8': '0',
    'scstat': '2',
    '__layoutStat': '2',
    'pt4_token': '',
    'p_skey': ''
}


def generate_random_r_value():
    return random.random()

for i in range(40):  # 抓取10次，每次10条  一般是十条一页 几页就填几
    r_value = generate_random_r_value()  
    url = url_template.format(start=start, r_value=r_value)  
    try:
        response = session.get(url, cookies=cookies)
        response.raise_for_status() 
        content = response.text
        
        print(url)
        print(content.encode('utf-8', errors='ignore').decode('utf-8'))

        for line in content.split('\n'):
            if "pubtime" in line or 'nickname' in line or "ubbContent" in line:
                with open('content.txt', 'a', encoding='utf-8') as f:
                    f.write(line + '\n')
        start += 10

        time.sleep(random.uniform(1, 3))

    except requests.RequestException as e:
        print(f"请求失败：{e}")
        time.sleep(5)  


def process_file():
    with open('content.txt', 'r', encoding='utf-8') as infile, open('MessageBoard.txt', 'w', encoding='utf-8') as outfile:
        content = infile.read()

        pubtime_matches = re.findall(r'"pubtime":"(.*?)"', content)
        nickname_matches = re.findall(r'"nickname":"(.*?)"', content)
        ubbcontent_matches = re.findall(r'"ubbContent":"(.*?)"', content, re.S)  

        if len(pubtime_matches) == len(nickname_matches) == len(ubbcontent_matches):
            for i in range(len(pubtime_matches)):
                pubtime = pubtime_matches[i]
                nickname = nickname_matches[i]
                ubbcontent = ubbcontent_matches[i].replace('\\n', ' ').replace('\n', ' ')  
                
                outfile.write(f"{pubtime}\n")
                outfile.write(f"{nickname}: {ubbcontent}\n\n")

process_file()
