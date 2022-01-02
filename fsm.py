from transitions.extensions import GraphMachine

import os
import sys
from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

from utils import send_text_message, send_carousel_message, send_button_message, send_image_message

import requests as rs
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


part=''

#import message_template

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "開始查詢" 

    def on_enter_menu(self, event):
        title = '請選擇您要執行的項目'
        text = '『查詢匯率』還是『今天吃什麼』'
        btn = [
            MessageTemplateAction(
                label = '查詢匯率',
                text ='查詢匯率'
            ),
            MessageTemplateAction(
                label = '今天吃什麼',
                text = '今天吃什麼'
            ),
        ]
        url = 'https://image.freepik.com/free-vector/business-icons-collection_1270-6.jpg'
        send_button_message(event.reply_token, title, text, btn, url)



    def is_going_to_choose(self, event):
        text = event.message.text
        if (text == '查詢匯率'):
            return True
        return False

    def on_enter_choose(self, event):
        title = '請選擇您要查詢的項目'
        text = '『亞洲』還是『歐美』'
        btn = [
            MessageTemplateAction(
                label = '亞洲',
                text ='亞洲'
            ),
            MessageTemplateAction(
                label = '歐美',
                text = '歐美'
            ),

        ]
        url = 'https://image.freepik.com/free-vector/illustration-donation-support-icons_53876-6146.jpg'
        send_button_message(event.reply_token, title, text, btn, url)


    def is_going_to_Asiaexchange(self, event):
        text = event.message.text
        if (text == '亞洲'):
            return True
        return False

    def on_enter_Asiaexchange(self, event):
        title = '請選擇您要查詢的種類'
        text = '『新加坡幣』 『人民幣』 『日圓』 『其他』，以下匯率均來自台灣銀行，需要其他地區匯率請選其他'
        btn = [
            MessageTemplateAction(
                label = '新加坡幣',
                text ='新加坡幣'
            ),
            MessageTemplateAction(
                label = '人民幣',
                text = '人民幣'
            ),
            MessageTemplateAction(
                label = '日圓',
                text = '日圓'
            ),
            MessageTemplateAction(
                label = '其他',
                text = '其他'
            ),
        ]
        url = 'https://image.freepik.com/free-vector/finance-department-employees-are-calculating-expenses-company-s-business_1150-41782.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_EAexchange(self, event):
        text = event.message.text
        if (text == '歐美'):
            return True
        return False

    def on_enter_EAexchange(self, event):
        title = '請選擇您要查詢的種類'
        text = '『美元』 『英鎊』 『加拿大幣』 『其他』，以下匯率均來自台灣銀行，需要其他地區匯率請選其他'
        btn = [
            MessageTemplateAction(
                label = '美元',
                text ='美元'
            ),
            MessageTemplateAction(
                label = '英鎊',
                text = '英鎊'
            ),
            MessageTemplateAction(
                label = '加拿大幣',
                text = '加拿大幣'
            ),
            MessageTemplateAction(
                label = '其他',
                text = '其他'
            ),
        ]
        url = 'https://image.freepik.com/free-vector/money-bag-background-design_1270-41.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_exchange_SGD(self, event):
        text = event.message.text
        if (text == '新加坡幣'):
            return True
        return False

    def on_enter_exchange_SGD(self, event):
        index=1
        value_SGD = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_SGD+'\n輸入「開始查詢」回到主選單'))
        self.go_back()

    def is_going_to_exchange_CNY(self, event):
        text = event.message.text
        if (text == '人民幣'):
            return True
        return False

    def on_enter_exchange_CNY(self, event):
        index=2
        value_CNY = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_CNY+'\n輸入「開始查詢」回到主選單'))
        self.go_back()



    def is_going_to_exchange_JPY(self, event):
        text = event.message.text
        if (text == '日圓'):
            return True
        return False

    def on_enter_exchange_JPY(self, event):
        index=3
        value_JPY = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_JPY+'\n輸入「開始查詢」回到主選單'))
        self.go_back()

    def is_going_to_exchange_USD(self, event):
        text = event.message.text
        if (text == '美元'):
            return True
        return False

    def on_enter_exchange_USD(self, event):
        index=4
        value_USD = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_USD+'\n輸入「開始查詢」回到主選單'))
        self.go_back()
    
    def is_going_to_exchange_GBP(self, event):
        text = event.message.text
        if (text == '英鎊'):
            return True
        return False

    def on_enter_exchange_GBP(self, event):
        index=5
        value_GBP = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_GBP+'\n輸入「開始查詢」回到主選單'))
        self.go_back()

    def is_going_to_exchange_CAD(self, event):
        text = event.message.text
        if (text == '加拿大幣'):
            return True
        return False

    def on_enter_exchange_CAD(self, event):
        index=6
        value_CAD = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_CAD+'\n輸入「開始查詢」回到主選單'))
        self.go_back()



    def is_going_to_exchange_else(self, event):
        text = event.message.text
        return text == "其他"

    def on_enter_exchange_else(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請至網站查詢： \n https://www.findrate.tw/exchange-quotation.php#.YdCTwVu-uO4"+'\n輸入「開始查詢」回到主選單')
        self.go_back()

    def is_going_to_exchange_back(self, event):
        text = event.message.text
        if (text == '其他'):
            return True
        return False
    def on_enter_exchange_back(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請至網站查詢： \n https://www.findrate.tw/exchange-quotation.php#.YdCTwVu-uO4"+'\n輸入「開始查詢」回到主選單')
        self.go_back()


    def is_going_to_eat(self, event):
        text = event.message.text
        if (text == '今天吃什麼'):
            return True
        return False

    def on_enter_eat(self, event):
        title='請選擇您要查詢的方式'
        text = '請選「一日三餐」或「其他種類」'
        btn = [
            MessageTemplateAction(
                label = '一日三餐',
                text ='一日三餐'
            ),
            MessageTemplateAction(
                label = '其他種類',
                text = '其他種類'
            ),
        ]
        url ='https://image.freepik.com/free-vector/plate-cuttlery-graphic-illustration_53876-9118.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_food(self, event):
        text = event.message.text
        if (text == '一日三餐'):
            return True
        return False

    def on_enter_food(self, event):
        title = '請選擇您要查詢的種類'
        text = '『早餐』 『午餐』『晚餐』'
        btn = [
            MessageTemplateAction(
                label = '早餐',
                text ='早餐'
            ),
            MessageTemplateAction(
                label = '午餐',
                text = '午餐'
            ),
            MessageTemplateAction(
                label = '晚餐',
                text = '晚餐'
            ),
        ]
        url = 'https://image.freepik.com/free-vector/fast-food-isometric-set_1284-21631.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_breakfast(self, event):
        text = event.message.text
        if (text == '早餐'):
            return True
        return False

    def on_enter_breakfast(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "台南早餐懶人包: \n https://dingeat.com/tainanbreakfast/"+'\n輸入「開始查詢」回到主選單')
        self.go_back()
    

    def is_going_to_lunch(self, event):
        text = event.message.text
        if (text == '午餐'):
            return True
        return False

    def on_enter_lunch(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請看這裡: \n https://13shaniu.tw/tag/%E5%8F%B0%E5%8D%97%E5%8D%88%E9%A4%90/"+'\n輸入「開始查詢」回到主選單')
        self.go_back()

    def is_going_to_dinner(self, event):
        text = event.message.text
        if (text == '晚餐'):
            return True
        return False

    def on_enter_lunch(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請看這裡: \n https://13shaniu.tw/tag/%E5%8F%B0%E5%8D%97%E6%99%9A%E9%A4%90/"+'\n輸入「開始查詢」回到主選單')
        self.go_back()

   
    def is_going_to_healthyfood(self, event):
        text = event.message.text
        if (text == '健康食品'):
            return True
        return False

    def on_enter_healthyfood(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請看這裡: \n https://kellylife.tw/happy-meal/"+'\n輸入「開始查詢」回到主選單')
        self.go_back()


    def is_going_to_dessert(self, event):
        text = event.message.text
        if (text == '甜品及其他'):
            return True
        return False

    def on_enter_dessert(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請看這裡: \n https://margaret.tw/tainan-coffee-shops/"+'\n輸入「開始查詢」回到主選單')
        self.go_back()



    def is_going_to_restaurant(self, event):
        text = event.message.text
        if (text == '其他種類'):
            return True
        return False

    def on_enter_restaurant(self, event):
        title = '請選擇您要查詢的種類'
        text = '『健康食品』 『甜品及其他』'
        btn = [
            MessageTemplateAction(
                label = '健康食品',
                text ='健康食品'
            ),
            MessageTemplateAction(
                label = '甜品及其他',
                text = '甜品及其他'
            ),
    
        ]
        url = 'https://img.freepik.com/free-vector/hand-drawn-dessert-collection_53876-100973.jpg?size=338&ext=jpg'
        send_button_message(event.reply_token, title, text, btn, url)






def get_exchange_value(index):
    if index==1:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/SGD')
    elif index==2:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/CNY')
    elif index==3:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/JPY')
    elif index==4:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/USD')
    elif index==5:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/GBP')
    elif index==6:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/CAD')
    # get html
    res.encoding = 'utf-8'
    # get data table
    soup = BeautifulSoup(res.text, 'lxml')
    table = soup.find('table', {'class': 'table table-striped table-bordered table-condensed table-hover'})
    table = table.find_all('tr')
    # remove table title
    table = table[2:]
    # add to dataframe
    col = ['牌告時間', '您查詢的種類', '台灣銀行現金買入', '台灣銀行現金賣出', '台灣銀行匯率買入', '台灣銀行匯率賣出']
    data = []
    for row in table:
        row_data = []
        date = row.find('td',{'class':'text-center'}).text
        currency = row.find('td',{'class':'text-center tablet_hide'}).text
        cash = row.find_all('td',{'class':'rate-content-cash text-right print_table-cell'})
        sight = row.find_all('td',{'class':'rate-content-sight text-right print_table-cell'})
        row_data.append(date)
        row_data.append(currency)
        row_data.append(cash[0].text)
        row_data.append(cash[1].text)
        row_data.append(sight[0].text)
        row_data.append(sight[1].text)
        data.append(row_data)
    df = pd.DataFrame(data)
    df.columns = col
    df['牌告時間'] = pd.to_datetime(df['牌告時間'])
    df.set_index('牌告時間', inplace=True)
    # value query
    pre_output=df.iloc[0]
    pre_output=str(pre_output)[:-24]
    output = pre_output.replace('Name: ','牌告時間：')
    return output
