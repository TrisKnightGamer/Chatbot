from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_sockets import Sockets
import requests
import pymongo
import json
import ast
import os
import time
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from api.wolframalpha import search_and_solve as search_wolfram
from api.wiki import search as search_wiki
from api.google_search import search_google
from api.weather import weather

from gensim.models.word2vec import Word2Vec
import NLP.main.text_classifier
from NLP.main.text_classifier import TextClassifier
from NLP.main.text_classifier import classifier
import time, random

app = Flask(__name__)
CORS(app)
#app.run(host='0.0.0.0',port=5000, debug=True)
sockets = Sockets(app)

server = pymongo.MongoClient('mongodb://0.0.0.0:27017/')
database = server['ChatApp']

messageCollection = database['messages']

start = 0
end = 0

api_key = "4e10bd9c2a268325e6ed167bd2ac57be"
base_url = "https://api.openweathermap.org/data/2.5/onecall?"

def seed_data():
    if messageCollection.count() > 0:
        print("Collection is not null")
        return
    else:
        content = """Tôi là Chatbot, hi vọng có thể giúp được bạn. Gõ 'Help' để biết thêm những gì mình có thể giúp được bạn hihi ^^."""

        record = {
            "isBot": True,
            "content": content,
            "time": time.time()
        }
        messageCollection.insert_one(record)
        time.sleep(2)
        print("Seeded successfully")
seed_data()

response = {
    "hello": [
        "Xin chào bạn.",
        "Chào bạn, tôi có thể giúp gì cho bạn",
        "Chào bạn, ngày mới tốt lành.",
        "Xin chào.",
      ],
    "goodbye":[
        "Tạm biêt.",
        "Hẹn gặp lại",
        "Chào tạm biệt",
        "Hẹn gặp lại bạn lần sau",
        "Tạm biệt, hẹn gặp lại"
      ],
    "thanks": [
        "Hân hạnh",
        "Luôn sẵn lòng :)",
        "Cảm ơn bạn, giúp được bạn là vinh dự của tôi",
        "Cảm ơn bạn, Rất vui khi được giúp đỡ bạn"
      ],
    "introduction": [
        "Tôi là chat bot có khả năng giúp bạn giải những vấn đề cơ bản trong cuộc sống",
        "Tôi là chat bot, hi vọng có thể giúp bạn một ít",
        "Là một chatbot tôi có thể giúp bạn trong vài lĩnh vực như toán, hóa, lịch sử ...",
        "Tôi có thể giúp bạn vài bài tập đơn giản như cân bằng hóa học, giải phương trình, ...",
        "Tôi là chatbot, rất hân hạnh làm quen với bạn"
      ],
    "cant":[
        "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Tôi nghĩ vấn đề này ngoài khả năng của tôi. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Xin lỗi bạn, tôi chưa được học về vấn đề này. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Tôi chưa thể giúp bạn ngay bây giờ, tôi sẽ cải thiện sau. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Xin lỗi, hiện tại tôi chưa thể giúp bạn. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Xin lỗi, hiện tại tôi chưa thể giúp bạn. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
        "Vấn đề này khá mới với tôi, tôi có thể học sau, xin lỗi bạn. Bạn có thể gõ 'Help' để biết thêm chi tiết.",
      ],
    "general_asking": [
        "Đây là kết quả của tôi, bạn có thể tham khảo:\n",
        "Tôi đã có kết quả:\n"
      ],
    "calculator": [
        "Đây là kết quả của tôi, bạn có thể tham khảo:\n",
        "Đây là kết quả: \n",
        "Kết quả nè:\n",
        "Kết quả:\n"
      ],
      "help":[
          "Bạn có thể tra cứu các thông tin về lịch sử, địa lý, văn học, toán,... và lý thuyết về những lĩnh vực khác nhau. \nĐể tra cứu thời tiết bạn vui lòng viết hoa tỉnh thành phố và quận(không cần viết tên phường, xã). Ví dụ : thời tiết tại Quận 8, Hồ Chí Minh.\nĐối với các vấn đề khác, bạn chỉ cần nhập câu hỏi bạn muốn hỏi, mình sẽ trả lời cho bạn.\n"
      ],
    "weather": [
        "Đây là thông tin thời tiết tôi có được : \n",
        "Thông tin thời tiết theo bạn yêu cầu : \n"
      ]
}

@app.route('/api/v1/messages', methods=['GET'])
def get_messages():
    print("ok")
    res = messageCollection.find({}, {'_id': False}).sort("time", 1)
    return json.dumps({'results': list(res)})

@app.route('/api/v1/messages', methods=['POST'])
def save_message():
    try:
        # Create new users
        try:
            body = request.get_json()
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = messageCollection.insert(body)
        #
        # Prepare the response
        if isinstance(record_created, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_created]), 200
        else:
            # Return Id of the newly created item
            return jsonify({"id":str(record_created),
                            "content" : body["content"]
                            }), 200
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500

@app.route('/api/v1/messages/reply', methods=['POST'])
def reply_message():
    # try:
         # Create new users
        try:
            body = request.get_json()
            #print("1")
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400
        body = request.get_json()
        content = body["content"]
        print(content)

        classified_content = classifier(content, is_general=True)
        print('label : ',classified_content)

        bot_reply = "Hi, I'm bot"
        if classified_content == "hello":
            bot_reply = random.choice(response["hello"])
        elif classified_content == "help":
            bot_reply = random.choice(response["help"])
        elif classified_content == "goodbye":
            bot_reply = random.choice(response["goodbye"])
        elif classified_content == "thanks":
            bot_reply = random.choice(response["thanks"])
        elif classified_content == "introduction":
            bot_reply = random.choice(response["introduction"])
        elif classified_content == "ask_weather_loc":
            bot_reply = weather(content, is_general=True)["result"]
            if bot_reply == False:
                bot_reply = random.choice(response["cant"])
            else :
                bot_reply = random.choice(response["weather"]) + bot_reply
        elif classified_content == "ask_weather":
            bot_reply = "Xin lỗi, hiện tại tôi chỉ hỗ trợ thông tin thời tiết hiện tại. Nếu muốn biết thông tin thời tiết hiện tại hãy cho tôi biết bạn đang ở quận nào của thành phố nào ?"
        elif classified_content == "location":
            bot_reply = weather(content, is_general=True)["result"]
            if bot_reply == False:
                bot_reply = random.choice(response["cant"])
            else:
                bot_reply = random.choice(response["weather"]) + bot_reply
        elif classified_content == "general_asking":
            bot_reply = solve_question_on_Wolfram(content, is_general=True)["result"]
            bot_reply1 = solve_question_on_Wiki(content, is_general=True)["result"]
            if bot_reply == False:
                bot_reply = random.choice(response["general_asking"]) + bot_reply1
            else:
                bot_reply = random.choice(response["general_asking"]) + bot_reply
        elif classified_content == "math":
            bot_reply = solve_question_on_Wolfram(content, is_general=True)["result"]
            if bot_reply == False:
                bot_reply = random.choice(response["cant"])
            else:
                bot_reply = random.choice(response["calculator"]) + bot_reply
        else:
            bot_reply = solve_question_on_Wolfram(content, is_general=True)["result"]
            #bot_reply1 = solve_question_on_Google(content, is_general=True)["result"]
            if bot_reply == False:
                bot_reply = random.choice(response["cant"]),
            else:
                bot_reply = random.choice(response["calculator"]) + bot_reply
        
        record_reply = messageCollection.insert({
            "content": bot_reply,
            "isBot": True,
            "time": time.time()
        })
        #
        # Prepare the response
        if isinstance(record_reply, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_reply]), 200
        else:
            # Return Id of the newly created item
            return jsonify(str(record_reply)), 200
    # except:
    #     record_reply = messageCollection.insert({
    #         "content": random.choice(response["cant"]),
    #         "isBot": True,
    #         "time": time.time()
    #     })
    #     # Error while trying to create the resource
    #     # Add message for debugging purpose
    #     return "", 500


def solve_question_on_Wolfram(question, is_general=True):
    res = search_wolfram(question, is_general=is_general)
    return {
        "result": res["result"]
    }

def solve_question_on_Wiki(question, is_general=True):
    res = search_wiki(question, is_general=is_general)
    return {
        "result": res["result"]
    } 
def solve_question_on_Google(question, is_general=True):
    res = search_google(question, is_general=is_general)
    return {
        "result": res["result"]
    } 

@app.route('/api/v1/test', methods=['GET'])
def test():
    res = search_wolfram("Cân bằng phản ứng: H2+O2=H2O", is_general=False)
    return {
        "result": res["result"]
    }

if __name__ == '__main__':
    app.run(debug=True)
