from transitions.extensions import GraphMachine

from utils import send_text_message
from get_weather import get_weather, get_temperature, temperature_keywords, weather_keywords, cities, other_interpretations

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def temperature_check(self, event):
        text = event.message.text
        self.status = 0 #status = 0 => check temperature
        return text in temperature_keywords

    def weather_check(self, event):
        text = event.message.text
        self.status = 1 #status = 1 => check weather
        return text in weather_keywords
    
    def on_enter_ask_city(self, event):
        send_text_message(event.reply_token, "請輸入要查詢的城市名稱")

    def on_enter_check_city(self, event):
        self.city = event.message.text #expect user to input city name here
        if self.city in cities:
            if self.city in list(other_interpretations):
                send_text_message(event.reply_token, "為您查詢中")
                self.city_exist(event)
        else:
            send_text_message(event.reply_token, "此城市不存在!")
            self.city_not_exist(event)

    def checking_temperature(self, event):
        return self.status == 0
    
    def checking_weather(self, event):
        return self.status == 1

    def on_enter_get_temperature(self, event):
        print("Time to check temperature")

        message = self.city + "當前溫度為攝氏 " +  get_temperature(self.city) + " 度"
        reply_token = event.reply_token
        send_text_message(reply_token, message)
        self.done()

    def on_exit_get_temperature(self):
        print("Done checking temperature")

    def on_enter_get_weather(self, event):
        print("Time to check weather")

        message = self.city + "當前天氣狀況為 " +  get_weather(self.city)
        reply_token = event.reply_token
        send_text_message(reply_token, message)
        self.done()

    def on_exit_get_weather(self):
        print("Done checking weather")
