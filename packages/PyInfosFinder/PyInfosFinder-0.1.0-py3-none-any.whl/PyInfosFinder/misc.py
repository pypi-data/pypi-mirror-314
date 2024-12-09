import requests

def getip() -> str:
    ip = 'None'
    try:
        ip = requests.get('https://api.ipify.org').text.strip()
    except:
        pass
    return ip

def getgeo(ip) -> dict:
    geo = {}
    try:
        geo = requests.get(f'http://ip-api.com/json/{ip}').json()
    except:
        pass
    return geo

def getallinfo() -> dict:
    ip = getip()
    geo_info = getgeo(ip)
    
    system_info = {
        "ip": ip,
        "geo": geo_info
    }
    return system_info