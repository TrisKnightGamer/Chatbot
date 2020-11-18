import requests
import random
def stt(mp3):
    url = 'https://api.fpt.ai/hmi/asr/general'
    payload = open(f'{mp3}', 'rb').read()
    api_key = ['6HBiGwH4oT84lFvhmYyaeIxwbZp4Bery', 'IdPmA1fN6dQsTRkiZ1BQ1diZqgVo5KHT', 'n5f2U3HxGOGASNeeFJukiUrmsn7nDIU1', 'mrDQ0qXmZ0ieeu9w6aliNEYwpYAI5v8l', 
        'dg6q3hjMGJ9c5CBH5wDzIgMWfpmyIYhq', 'oDLVCkmT8wfyckmEpZe2tof72kFkkg16']
    random.seed(5)
    headers = {
        'api-key': api_key[random.random()],
    }

    response = requests.post(url=url, data=payload, headers=headers)

    print(response.json())
