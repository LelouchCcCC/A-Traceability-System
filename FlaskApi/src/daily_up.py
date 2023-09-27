import requests
import json
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34102848205531413024_1584924641755&_=1584924641756'
headers ={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
}
res = requests.get(url,headers=headers)
# print(res.text)
response_data = json.loads(res.text.replace('jQuery34102848205531413024_1584924641755(','')[:-1])
areaTree_data = json.loads(response_data['data'])['areaTree']
# for province_data in areaTree_data[0]['children']:
#     print(province_data)
for pro_infos in areaTree_data[0]['children']:
    province_name = pro_infos['name']  # 省名
    for city_infos in pro_infos['children']:
        city_name = city_infos['name']  # 市名
        confirm = city_infos['total']['confirm']#历史总数
        confirm_add = city_infos['today']['confirm']#今日增加数
        heal = city_infos['total']['heal']#治愈
        dead = city_infos['total']['dead']#死亡
        print(province_name,city_name,confirm,confirm_add,heal,dead)

