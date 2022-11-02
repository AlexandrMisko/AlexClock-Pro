import requests
import datetime
import time
import yagmail
import smtplib
import re
    
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'X-CSRFToken': 'NbIabgSFrRFILZeUU2i32IjGQsXuHJG1',
    'Cookie': 'mid=YZIUAwALAAHIMaHw27iWm4uRNhXm; ig_did=267B8A84-7E4C-4AE8-8310-89537C6AE002; ig_nrcb=1; datr=ZWq4YgmzX9ZT1JWqg_JKOBhe; dpr=1.25; shbid="12194\05448282355544\0541696751940:01f75de3ff73ba83cc132c46cf7f6ad404632b04aaae15061f319cbfb1f64ca1dadc18f4"; shbts="1665215940\05448282355544\0541696751940:01f795f049050d942048e1184934f3c5267754225ecbff3b1491356e18242ffad8d14aec"; rur="NAO\05448282355544\0541697009014:01f7e715893ed1a44dfe0fcc8e7d1d0c5d0db04cc82c5566927f15bcdfa36bb8822ec567"; csrftoken=NbIabgSFrRFILZeUU2i32IjGQsXuHJG1',
}
data = {
    "enc_password": "#PWD_INSTAGRAM_BROWSER:10:1666003782:AaJQAOvwCmxrRBoLgsRmdBAhmbryCB+vi4973MVF9d575edq0vUfARENK0QiqdtfIyuhzgGzSetL1yhBUvkIDUhugrkPpsXeeAgQM9IDGVRcAxivpqpgQJI7X5UrXHC2d9CRH5uvvkTdq4VM",
    "username": "speedmilo40@gmail.com",
    "queryParams": "{\"oneTapUsers\":\"[\\\"48282355544\\\"]\"}",
    "optIntoOneTap": "false",
    "stopDeletionNonce": "",
    "trustedDeviceRecords": "{}"
}
session = requests.session()
resp = session.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers)
print(resp.text)
obj_csrf = re.compile('csrftoken=(?P<csrftoken>.*?) ', re.S)
csrftoken = obj_csrf.search(str(resp.cookies)).group('csrftoken')

yag = yagmail.SMTP(user='1586924294@qq.com', password='encbysssvjrujijb', host='smtp.qq.com')
resp = session.get('https://i.instagram.com/api/v1/users/web_profile_info/?username=alexandrmisko', headers={
    'X-IG-App-ID': '936619743392459',
})
taken_stamp = ['']*4
taken_stamp[0] = resp.json()['data']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['taken_at_timestamp']
taken_stamp[1] = resp.json()['data']['user']['edge_owner_to_timeline_media']['edges'][1]['node']['taken_at_timestamp']
taken_stamp[2] = resp.json()['data']['user']['edge_owner_to_timeline_media']['edges'][2]['node']['taken_at_timestamp']
taken_stamp[3] = resp.json()['data']['user']['edge_owner_to_timeline_media']['edges'][3]['node']['taken_at_timestamp']
rank = 0
for i in range(1,4):
    if taken_stamp[0] < taken_stamp[i]:
        taken_stamp[0] = taken_stamp[i]
        rank = i
taken_at = (datetime.datetime.fromtimestamp(taken_stamp[rank]) + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
id = resp.json()['data']['user']['edge_owner_to_timeline_media']['edges'][rank]['node']['id']
shortcode = resp.json()['data']['user']['edge_owner_to_timeline_media']['edges'][rank]['node']['shortcode']
# now_at = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
# print(now_at)
url = f'https://www.instagram.com/p/{shortcode}'
print(url)
print(taken_at)
resp = session.get('https://i.instagram.com/api/v1/accounts/edit/web_form_data/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'X-IG-App-ID': '936619743392459',
})
store_at = resp.json()['form_data']['biography']
if taken_at == store_at:
    print('无需更新')
else:
    resp = session.post('https://i.instagram.com/api/v1/web/accounts/edit/', data={
        'first_name': 'ZX+Su',
        'email': 'speedmilo40@gmail.com',
        'username': 'zx.su.77',
        'phone_number': '',
        'biography': taken_at,
        'external_url': '',
        'chaining_enabled': 'on'
    }, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'X-IG-App-ID': '936619743392459',
        'X-CSRFToken': csrftoken
    })
    print(resp.text)
    resp = session.get(f'https://i.instagram.com/api/v1/media/{id}/info/', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'X-IG-App-ID': '936619743392459'
    })
    contents = ''
    attachments = []
    media_type = resp.json()['items'][0]['media_type']
    if media_type == 2:
        contents = '<button type="button"><a href='+resp.json()['items'][0]['video_versions'][0]['url']+'>视频</a></button>'
        resp_bytes = session.get(resp.json()['items'][0]['video_versions'][0]['url'])
        with open('video.mp4', 'wb') as f:
            f.write(resp_bytes.content)
        attachments.append('video.mp4')
    elif media_type == 1:
        contents = '<button type="button"><a href='+resp.json()['items'][0]['image_versions2']['candidates'][0]['url']+'>图片</a></button>'
        resp_bytes = session.get(resp.json()['items'][0]['image_versions2']['candidates'][0]['url'])
        with open('image.jpg', 'wb') as f:
            f.write(resp_bytes.content)
        attachments.append('image.jpg')
    else:
        img_num = 1
        video_num = 1
        items = resp.json()['items'][0]['carousel_media']
        for item in items:
            if item['media_type'] == 1:
                contents += '<button type="button"><a href='+item['image_versions2']['candidates'][0]['url']+'>图片</a></button>'
                resp_bytes = session.get(item['image_versions2']['candidates'][0]['url'])
                with open(f'image_{img_num}.jpg', 'wb') as f:
                    f.write(resp_bytes.content)
                attachments.append(f'image_{img_num}.jpg')
                img_num += 1
            else:
                contents += '<button type="button"><a href='+item['video_versions'][0]['url']+'>视频</a></button>'
                resp_bytes = session.get(item['video_versions'][0]['url'])
                with open(f'video_{video_num}.mp4', 'wb') as f:
                    f.write(resp_bytes.content)
                attachments.append(f'video_{video_num}.mp4')
                video_num += 1
    try:
        yag.send(to='1586924294@qq.com', subject='AlexandrMisko更新啦！', contents='<h1>方式1（动态--复制下面链接到有Instagram登录状态的浏览器中打开）：</h1>'+url+'<h1>方式2（在线--直接打开即可）：</h1>'+contents+'<h1>方式3（下载--查看下方附件）：</h1>', attachments=attachments)
    except smtplib.SMTPSenderRefused:
        print('您所发送的邮件大小超出腾讯邮箱限制，取消发送附件')
        yag.send(to='1586924294@qq.com', subject='AlexandrMisko更新啦！', contents='<h1>方式1（动态--复制下面链接到有Instagram登录状态的浏览器中打开）：</h1>'+url+'<h1>方式2（在线--直接打开即可）：</h1>'+contents)
    except smtplib.SMTPException as e:
        print(e)
    yag.close()
    print('发送邮件成功！')
