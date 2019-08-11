import re
import base64
import aiohttp
import asyncio
import requests

apikey = 'f65e2f517a8ef3d4d95e2bd20a600c47ff811efb63e431100def56421e607aff'


async def search(param):
    headers = {'x-apikey':apikey}
    params = {'query': param, 'limit': 300, 'descriptors_only': 'true'}
    hashes = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.virustotal.com/api/v3/intelligence/search', params=params, headers=headers) as resp:
            js = await resp.json()
            if 'error' in js.keys():
                return 'err', '{}\n{}'.format(js['error']['code'], js['error']['message'])
            for i in js['data']:
                hashes.append(i['id'])
        params = {'apikey': apikey, 'query': param}
        async with session.get('https://www.virustotal.com/vtapi/v2/file/search', params=params) as resp:
            if 'No samples matching the search criteria' in await resp.text():
                pass
            else:
                js = await resp.json()
                hashes += js['hashes']
    hashes = list(set(hashes))
    if hashes == []:
        return  'Sorry! Not found '+param
    else:
        for i in range(len(hashes)):
            hashes[i] = 'https://www.virustotal.com/gui/file/{}/detection'.format(hashes[i])
        return hashes
        
        



async def download(hashurl):
    if 'virustotal' in hashurl:
        try:
            hashurl = re.search('file\/(\w+)', hashurl).group(1)
        except:
            try:
                hashurl = base64.b64decode(re.search('file-analysis\/(.+==)', hashurl).group(1)).decode().split(':')[0]
            except:
                return -1
    params = {'query': hashurl}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://www.virustotal.com/ui/search', params=params) as resp:
                js = await resp.json()
                f_name = js['data'][0]['attributes']['meaningful_name']
                tags = js['data'][0]['attributes']['tags']
        except:
            return -1
        downloaded_file = None
        params = {'apikey': apikey, 'hash': hashurl}
        async with session.get('https://www.virustotal.com/vtapi/v2/file/download', params=params) as resp:
            downloaded_file = await resp.read()
            if downloaded_file == b'':
                return -1
            else:
                return downloaded_file, f_name, resp.url, tags




def download1(hashurl):
    if 'virustotal' in hashurl:
        try:
            hashurl = re.search('file\/(\w+)', hashurl).group(1)
        except:
            try:
                hashurl = base64.b64decode(re.search('file-analysis\/(.+==)', hashurl).group(1)).decode().split(':')[0]
            except:
                return -1
    params = {'query': hashurl}
    r = requests.get('https://www.virustotal.com/ui/search', params=params)
    try:
        f_name = r.json()['data'][0]['attributes']['meaningful_name']
    except: return -1
    downloaded_file = None
    try:
        params = {'apikey': apikey, 'hash': hashurl}
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/download', params=params)
        downloaded_file = response.content
    except:
        pass
    finally:
        if downloaded_file == b'':
            return -1
        else:
            return downloaded_file, f_name, response.url
