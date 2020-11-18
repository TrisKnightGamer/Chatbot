import requests
from urllib import parse
import wikipedia
import random
wikipedia.set_lang('vi')
def search(s, is_general=True):
    try:
        s = wikipedia.search(s)[:1]
        res = wikipedia.summary(random.choice(s), sentences=2)
        return {
            "result": res
        }
    except:
        return {
            "result": False
        }
