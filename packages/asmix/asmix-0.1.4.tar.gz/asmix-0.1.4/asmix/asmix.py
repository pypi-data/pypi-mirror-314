import requests
from random import randrange
import time
from user_agent import generate_user_agent
import random

class Email:
    @staticmethod
    def cookies():
        while True:
            try:
                res = requests.get('https://signup.live.com/signup')
                amsc = res.cookies.get_dict().get('amsc')
                canary = res.text.split('"apiCanary":"')[1].split('"')[0].encode().decode('unicode_escape')
                return amsc, canary
            except:
                pass

    @staticmethod
    def hotmail(email):
        amsc, canary = Email.cookies()  
        cookies = {'amsc': amsc}
        headers = {
            'canary': canary,
            'origin': 'https://signup.live.com',
            'referer': 'https://signup.live.com/signup?lic=1&uaid=3daaf5bf6b70499d8a5035844d5bbfd8',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        json_data = {'signInName': email}

        response = requests.post(
            'https://signup.live.com/API/CheckAvailableSigninNames',
            cookies=cookies,
            headers=headers,
            json=json_data
        ).text

        return True if '"isAvailable":true' in response else False

class Instagram:
    @staticmethod
    def users(year):
        if year == 2011:
            id_range = 17699999
        elif year == 2012:
            id_range = 263014407
        elif year == 2013:
            id_range = 361365133
        elif year in range(2014, 2024):
            id_range = 61331927186
        else:
            return None

        def gg():
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
                'x-ig-app-id': '936619743392459',
                'x-csrftoken': 'QOeFYsOi8enKuW80uC0WezhvEgiydc2Y',
                'x-ig-www-claim': 'hmac.AR3iNxyHufbREf9pIUL6m2ciMIIxA3vQTyCHW_yWjgu5dmsq',
            }

            data = {
                'av': '17841408545457742',
                '__user': '0',
                '__a': '1',
                '__req': '53',
                'dpr': '1',
                '__csr': 'iMkMF5NsIh2I4Aggpik9SLfZgxAZOsJh6DcNcUFXH-GHqnlaoSiypHBiVaFkhtdFmO',
                '__spin_r': '1014910249',
                'variables': '{"id":"' + str(randrange(10000, id_range)) + '","render_surface":"PROFILE"}',
                'server_timestamps': 'true',
                'doc_id': '7663723823674585',
            }

            try:
                response = requests.post(
                    'https://www.instagram.com/graphql/query',
                    headers=headers,
                    data=data
                )
                username = response.json()['data']['user']['username']
                return username
            except:
                return None

        return gg()

    @staticmethod
    def check(email):

        headers = {
	    'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
	    'X-Pigeon-Rawclienttime': '1700251574.982',
	    'X-IG-Connection-Speed': '-1kbps',
	    'X-IG-Bandwidth-Speed-KBPS': '-1.000',
	    'X-IG-Bandwidth-TotalBytes-B': '0',
	    'X-IG-Bandwidth-TotalTime-MS': '0',
	    'X-Bloks-Version-Id': 'c80c5fb30dfae9e273e4009f03b18280bb343b0862d663f31a3c63f13a9f31c0',
	    'X-IG-Connection-Type': 'WIFI',
	    'X-IG-Capabilities': '3brTvw==',
	    'X-IG-App-ID': '567067343352427',
	    'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
	    'Accept-Language': 'en-GB, en-US',
	     'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'Accept-Encoding': 'gzip, deflate',
	    'Host': 'i.instagram.com',
	    'X-FB-HTTP-Engine': 'Liger',
	    'Connection': 'keep-alive',
	    'Content-Length': '356',
}

        data = {
		    'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"'+email+'"}',
		    'ig_sig_key_version': '4',
  }

        response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data).text
        
        if email in response:
            return True
        else:
            return False

    @staticmethod
    def rest(user):
        try:
            headers = {
                'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
                'X-Pigeon-Rawclienttime': '1700251574.982',
                'X-IG-Connection-Speed': '-1kbps',
                'X-IG-Bandwidth-Speed-KBPS': '-1.000',
                'X-IG-Bandwidth-TotalBytes-B': '0',
                'X-IG-Bandwidth-TotalTime-MS': '0',
                'X-Bloks-Version-Id': 'c80c5fb30dfae9e273e4009f03b18280bb343b0862d663f31a3c63f13a9f31c0',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw==',
                'X-IG-App-ID': '567067343352427',
                'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
                'Accept-Language': 'en-GB, en-US',
                'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'X-FB-HTTP-Engine': 'Liger',
                'Connection': 'keep-alive',
                'Content-Length': '356',
            }
            data = {
                'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"' + user + '"}',
                'ig_sig_key_version': '4',
            }
            response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data).json()
            r = response['email']
        except:
            r = ' Bad '
        return r

    @staticmethod
    def info(username):
        try:
            headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'x-ig-app-id': '1217981644879628',
             }
            params = {'username': username,}
            info = requests.get('https://www.instagram.com/api/v1/users/web_profile_info/',params=params,headers=headers,).json()
        except:
            info = False
        try:
            Id = info['data']['user']['id']
        except:
            Id = None

        try:
            followers = info['data']['user']['edge_followed_by']['count']
        except:
            followers = None
        try:
            following = info['data']['user']['edge_follow']['count']
        except:
            following = None
        try:
           post =  info['data']['user']['edge_owner_to_timeline_media']['count']
        except:
            post = None
        try:
            name = info['data']['user']['full_name']
        except:
            name = None
        try:
            is_verified = info['data']['user']["is_verified"]
        except:
            is_verified = None
        try:
            is_private = info['data']['user']['is_private']
        except:
            is_private = None
        try:
            biography = info['data']['user']['biography']
        except:
            biography = None
        
        try:
            Id = int(Id)
            if 1 < Id <= 1278889:
                date = 2010
            elif 1279000 <= Id <= 17750000:
                date = 2011
            elif 17750001 <= Id <= 279760000:
                date = 2012
            elif 279760001 <= Id <= 900990000:
                date = 2013
            elif 900990001 <= Id <= 1629010000:
                date = 2014
            elif 1629010001 <= Id <= 2369359761:
                date = 2015
            elif 2369359762 <= Id <= 4239516754:
                date = 2016
            elif 4239516755 <= Id <= 6345108209:
                date = 2017
            elif 6345108210 <= Id <= 10016232395:
                date = 2018
            elif 10016232396 <= Id <= 27238602159:
                date = 2019
            elif 27238602160 <= Id <= 43464475395:
                date = 2020
            elif 43464475396 <= Id <= 50289297647:
                date = 2021
            elif 50289297648 <= Id <= 57464707082:
                date = 2022
            elif 57464707083 <= Id <= 63313426938:
                date = 2023
            else:
                date = 2024
        except:
            return None

        return {
            "name": name,
            "username": username,
            "followers": followers,
            "following": following,
            "date": date,
            "id": Id,
            "post": post,
            "bio": biography,
            "is_verified": is_verified,
            'is_private': is_private,
        }
    @staticmethod
    def date(Id):
        try:
            Id = int(Id)
            if 1 < Id <= 1278889:
                date = 2010
            elif 1279000 <= Id <= 17750000:
                date = 2011
            elif 17750001 <= Id <= 279760000:
                date = 2012
            elif 279760001 <= Id <= 900990000:
                date = 2013
            elif 900990001 <= Id <= 1629010000:
                date = 2014
            elif 1629010001 <= Id <= 2369359761:
                date = 2015
            elif 2369359762 <= Id <= 4239516754:
                date = 2016
            elif 4239516755 <= Id <= 6345108209:
                date = 2017
            elif 6345108210 <= Id <= 10016232395:
                date = 2018
            elif 10016232396 <= Id <= 27238602159:
                date = 2019
            elif 27238602160 <= Id <= 43464475395:
                date = 2020
            elif 43464475396 <= Id <= 50289297647:
                date = 2021
            elif 50289297648 <= Id <= 57464707082:
                date = 2022
            elif 57464707083 <= Id <= 63313426938:
                date = 2023
            else:
                date = 2024
            return date
        except:
            return None
            

class List:
    @staticmethod
    def user(username, password, target_username, type):
        
        def sessionID():
            session = requests.Session()
            data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1589682409:{password}',
            }
            login_url = 'https://www.instagram.com/accounts/login/ajax/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'x-csrftoken': 'missing',
            }
            response = session.post(login_url, data=data, headers=headers)
            print(response.text)
            if response.status_code == 200 and response.json().get('authenticated'):
                return session.cookies.get_dict().get('sessionid')
            return None

        session_id = sessionID()
        if session_id is None:
             print('Bad Login')

        headers = {
            'user-agent': generate_user_agent(),
        }
        user_info_url = f'https://api-ig.storiesig.info/api/userInfoByUsername/{target_username}'
        response = requests.get(user_info_url, headers=headers).json()

        if response.get('result', {}).get('user', {}).get('is_private', True):
            print( 'Account Private')

        yy = type
        iq = response['result']['user']['pk']

        cookies = {
            'sessionid': f'{session_id}'
        }
        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'user-agent': generate_user_agent(),
            'x-csrftoken': '94GyQTVKUbrgdsa1RuyYZdhG45EBF2jV',
            'x-ig-app-id': '1217981644879628'
        }

        max_id = ''
        usernames = []
        batch_size = 50 if type == 'followers' else 150

        while True:
            params = {'count': '150', 'max_id': max_id}
            url = f'https://www.instagram.com/api/v1/friendships/{iq}/{yy}/'
            response = requests.get(url, params=params, cookies=cookies, headers=headers).json()
            
            users = response.get('users', [])
            if not users:
                break

            for user in users:
                usernames.append(user['username'])

                if len(usernames) % batch_size == 0:
                    for username in usernames[-batch_size:]:
                        print(username)
                        time.sleep(0.01)  

            max_id = response.get('next_max_id')
            if not max_id:
                break

        remaining_users = usernames[len(usernames) - (len(usernames) % batch_size):]
        if remaining_users:
            for username in remaining_users:
                print(username)
                time.sleep(0.01)

        return usernames