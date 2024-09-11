import requests
import random
import json
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
random_integer = random.randint(13204394220997, 93204394220997)
requests.packages.urllib3.disable_warnings()
cookies='p_h5_u=DADEB53C-83B4-413D-B5C5-B52F0572FACD; selectedStreamLevel=LD; r117lf=35830f5f427f260c42e65025961b303e; Hm_lvt_af91e610eea7757cf9376392476fa295=1726042274; JSESSIONID=abc5slHUDHTRd-eMNyGhz; sangfor8822=22558280; timeStamp=1726046445313; requestToken=bc34e9c284f8b7cca2cd85fd335c1ceb; requestToken2=98ac1185d3cf37568aaa952f683bda4d; ssoLoginName=__27e6Vu7Ej7Nm8Jn9Vp8Yn9Cm9Yp9EsBXbBHuBSwCFoCSyDCcCQcEDf6Jf6Ub8Xv8Iv9KdABu93vA6rAMfCAhAIcDAoC4tCTjENkCTdDXw6Ph6Zx; s=aba1de16-0c26-483f-8541-fbdab541570d; cr=student; mid=m-aba1de16-0c26-483f-8541-fbdab541570d'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36','cookie': cookies }

def startlearn(headers,itemId,attachId):
    start_record_url='https://www.jste.net.cn/lfv5/learnContentLib/startRecord.action?lcMaterialInfo.materialId=m-aba1de16-0c26-483f-8541-fbdab541570d&lcMaterialItem.itemId='+itemId+'&lcMaterialItem.attachId='+attachId+'&rnd=0.'+ str(random_integer)
    record_response = requests.get(start_record_url, headers=headers)
    #print(start_record_url,record_response.text)
    global record_id
    record_id=json.loads(record_response.text)
    record_id = record_id["data"]["recordId"]
    print("获取学习记录码recordId:",record_id)


def learn(headers,itemId,attachId):
    record_url = 'https://www.jste.net.cn/lfv5/learnContentLib/updateRecord.action?recordId='+record_id+'&groupId=aba1de16-0c26-483f-8541-fbdab541570d&rnd=0.'+ str(random_integer)
    record_response = requests.get(record_url, headers=headers)
    print('当前学习提交状态：',record_response.text)

def print_message(interval,value,itemId,attachId):
    startlearn(headers,itemId,attachId)
    timelearn=interval*60
    while timelearn > 0:
        now = datetime.now()
        # 格式化时间为字符串
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("正在学习:",itemId,'，共',interval,"分钟，还剩余",(timelearn/60-value),'分钟学习完成，当前时间：',current_time)
        time.sleep(30)
        timelearn -= 30
        learn(headers,itemId,attachId)

    print("学习时间已足够，开始学习下一个")

learntime_url='https://www.jste.net.cn/lfv5/learnContentLib/studentMain.action'
learntime_response = requests.get(learntime_url, headers=headers, verify=False)
#print(learntime_response.text)

# 解析 HTML
soup = BeautifulSoup(learntime_response.text, 'html.parser')
# 找到包含 learnTime 变量的 <script> 标签
script_tag = soup.find('script', string=re.compile(r'var learnTime'))
# 提取 learnTime 变量的内容
learn_time_text = re.search(r'var learnTime\s*=\s*(\{.*?\});', script_tag.string, re.DOTALL).group(1)
# 将提取的内容解析为 Python 字典
learn_time_data = json.loads(learn_time_text)
#print(learn_time_data)
json_str = str(learn_time_data).replace("'", '"')
# 解析为JSON对象
data = json.loads(json_str)
# 分别输出JSON中的信息
print("已学课程信息：")
for key, value in data.items():
    print(f"itemId: {key}, time: {value}")


learn_tag = soup.find('script', string=re.compile(r'var mjson'))
# 提取 learnTime 变量的内容
learn_tag_time_text = re.search(r'var mjson\s*=\s*(\{.*?\});', learn_tag.string, re.DOTALL).group(1)
#learn_tag_time_text = str(learn_tag_time_text).replace("'", '"')
learn_tag_time_text  = json.loads(learn_tag_time_text )
#print(learn_tag_time_text)
print("未学课程信息：")
for item in learn_tag_time_text["itemList"]:
    if item["maxLearnTime"] > 0:
        for key, value in data.items():
            #print('已学：',key,'未学：',item["itemId"],'已学视频itemId:',value,'未学时长：',item["maxLearnTime"])
            if key == item["itemId"]:
                print("当前视频已有学习记录。已学视频itemId:",key,'当前视频itemId:',item["itemId"])
                if value >= item["maxLearnTime"]:
                    print('当前视频学习时长已满足，跳过。已学时长：',value,'最大记录时长：',item["maxLearnTime"])
                    break
                else:
                    print("开始学习：")
                    print(f"itemTitle: {item['itemTitle']}")
                    print(f"maxLearnTime: {item['maxLearnTime']}")
                    print(f"itemId: {item['itemId']}")
                    print(f"attachId: {item['attachId']}")
                    print_message(int(item['maxLearnTime']),value,item['itemId'],item['attachId'])

