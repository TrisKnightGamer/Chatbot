from googlesearch import search

def search_google(s, is_general=True):
    try:
        for res in  search(s, tld='com', lang='vn', num = 1, pause=2.0):
            return {
                "result": res
            }
    except:
        return {
            "result": False
        }