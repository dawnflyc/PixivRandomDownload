import json
import os
import random
import re
import time

import requests

proxy = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890'
}


def header(url):
    return {
        'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/76.0.3809.132 Safari/537.36",
        'Referer': url,
        'Cookie': '__cfduid=df4c94d9266140fa769fb982fde1d3f301617859032; first_visit_datetime_pc=2021-04-08+14:17:12; p_ab_id=5; p_ab_id_2=1; p_ab_d_id=1046732053; yuid_b=MFISaIU; __utmz=235335808.1617859035.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1504593990.1617859035; PHPSESSID=31161881_CSTk2IFCP8o2ZSSzYWPV3rFc2kqrga6N; device_token=bae8bc7229d83f1568c721612919f25b; c_type=24; privacy_policy_agreement=0; a_type=0; b_type=1; ki_s=214760:0.0.0.0.2;214994:0.0.0.0.2; login_ever=yes; __utmv=235335808.|2=login ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=31161881=1^9=p_ab_id=5=1^10=p_ab_id_2=1=1^11=lang=zh=1; tag_view_ranking=JUhUC4yJLC~SKQUHZx-lq~BFKUzIToh2~jpIZPQ502H~zZVZ6698Si~YujG5aPAeR~--BqJSx0Ht~K5kkxWXCe_~ibTwFdmyvo~7wdsgQtcu4~RTJMXD26Ak~LJo91uBPz4~Lt-oEicbBr~Mmb81P1JFg~65aiw_5Y72; ki_t=1617859066292;1617859066292;1617861083437;1;12; __utma=235335808.1504593990.1617859035.1618117231.1618120293.3; __utmc=235335808; __cf_bm=8ed7dd1f0f687127adf080482f129014ca65da86-1618120291-1800-AS1460AWnnxjSpYyUxjI7PAggk4lLpx/LJfVDO1qqx48Ssp4eb5KXV5v1YNeDnS7gZpgc2iFsXAdCVQGNjvICnqtZTQWVpJH526XY+cZ8+tpNzFM1ivtRGcX2Axg5Yig8bSSGVjYOUUmM7IwDmMYRSXkwJ4ey9oSqc09W9zT97FtlUHn/cxPqZO1hKN8IvK13g==; __utmt=1; __utmb=235335808.2.10.1618120293; _gid=GA1.2.1749810522.1618120296; _gat_UA-1830249-3=1'
    }


def download(url, name):
    print('开始下载\t' + url)
    ir = requests.get(url, headers=header(url), proxies=proxy)
    open(name, 'wb').write(ir.content)


def find(work_id, path, filter=None):
    id_str = str(work_id)
    work_url = 'https://www.pixiv.net/artworks/' + id_str
    page = requests.get(work_url, headers=header(work_url), proxies=proxy)
    if page.status_code == 200:
        json_str = re.findall('\"bookmarkCount\":[0-9]+,\"likeCount\":[0-9]+,\"commentCount\":[0-9]+',
                              str(page.content))
        json_value = json.loads('{' + json_str[0] + '}')
        sort = json_value["bookmarkCount"] + json_value["likeCount"] + json_value["commentCount"]
        dir = str(sort) + '-' + id_str
        if sort > 99:
            if not filter is None:
                if not filter(page):
                    return False
            if not os.path.exists(path):
                os.makedirs(path)
            if not os.path.exists(path+'/' + dir):
                os.makedirs(path+'/' + dir)
            else:
                return False

            page_url = 'https://www.pixiv.net/ajax/illust/' + id_str + '/pages?lang=zh'
            json_page = requests.get(page_url, headers=header(page_url), proxies=proxy)
            json_text = json.loads(json_page.content)
            if not json_text['error']:
                print('\n开始爬取\t' + work_url)
                json_body = json_text['body']
                for u in json_body:
                    ran = random.randint(0, 99999)
                    ran_str = str(ran)
                    download(u['urls']['original'], path+'/'+ dir + '/' + ran_str+'.jpg')
                return True
            else:
                print('页面ajax异常')
        else:
            print('...')
    else:
        print('...')
    return False
