from flask import Flask, request, abort
from bs4 import BeautifulSoup
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import *
import requests, json

import random
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('unG7GBW3UQFz2GwbvbhHYOytIRQko+rnT1uzaInmpYamFKKTmgEpRt69tF0yuao1VkY+rtc8ii3Ofz6BQkq8JUqzK80LegQHD20qTEuJ5zSybytciRweDiLFgXJ/vc514gJQJhYoUVPWCfqDsWOXZwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d3aad60e85b6fe032bf3678ce3061011')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#去資料庫查詢
def get_answer(message_text):
    
    url = "https://database111.azurewebsites.net/qnamaker/knowledgebases/ef328dd8-87a0-4fa9-9c8b-f62ee24cacaf/generateAnswer"

    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Authorization': 'EndpointKey a9754114-06db-4dab-aa87-e74791c81097'
                   }
               )

    data = response.json()
 
    try: 
        #我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        #這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']

        return answer

    except Exception:

        return "Error occurs when finding answer"

def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 5:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if user_message == '貼圖':
        message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
    elif user_message == '臉怎麼那麼臭':
        message = TextSendMessage(text='因為去年被刷掉了，所以今年要霸氣的強勢回歸')
    elif user_message == '你抱著什麼娃娃阿':
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/dRwYdNr.jpg',
                        action=PostbackTemplateAction(
                            label='這個是?',
                            text='哦..這是代表?',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/WIPxmns.jpg',
                        action=PostbackTemplateAction(
                            label='那這隻又是?',
                            text='那這隻又怎麼解釋?',
                            data='action=buy&itemid=2'
                        )
                   )
                ]
            )
        )
        
    elif user_message == '哦..這是代表?':
        message = TextSendMessage(text='還沒成為Liner，我只能抱路邊找的類似熊大的娃娃')
    elif user_message == '那這隻又怎麼解釋?':
        message = TextSendMessage(text='一樣啊，等錄取之後才能去抱正版最大隻的(怒)!')

    elif user_message == '看不出來誒~我該怎麼幫你?':
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='當然是讓我進到總部實習囉!',
                actions=[
                    PostbackTemplateAction(
                        label='Sure',
                        text='那介紹一下你自己吧',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='Why not',
                        text='介紹一下機器人所用到的技術'
                    )
                ]
            )
        )
    elif user_message == '那介紹一下你自己吧':
        message = TextSendMessage(text='你好~我是吳今詠，叫我Robin就好。目前為大學生/家教老師/實習工程師。成績即使不是最好，但學習能力、抓住機會的能力絕對是最強的。這是我第一次接觸chatbot，這星期自學了超級多東西XD，(也碰上超多問題)，即使很多功能還沒完善，但絕對不會讓你們後悔錄取我的。')
    elif user_message == '介紹一下機器人所用到的技術':
        message = TextSendMessage(text='Linebot api、NLP語意分析、資料庫、基礎爬蟲、Random隨機取樣。此bot動態連結至Azure資料庫，可隨時查看log，以訓練出更符合使用者提問之答案。')
    elif user_message == '新聞':
        content = apple_news()
        message = TextSendMessage(text= content)            

    else :
        answer = get_answer(event.message.text)
        message = TextSendMessage(text= answer)    
    line_bot_api.reply_message(event.reply_token, message)

#處理貼圖
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(event.reply_token, sticker_message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
