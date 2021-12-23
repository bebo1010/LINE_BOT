from transitions.extensions import GraphMachine

from utils import send_text_message
from get_weather import get_weather, get_temperature, cities

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def temperature_check(self, event):
        text = event.message.text
        return text.lower() == "check temperature"

    def weather_check(self, event):
        text = event.message.text
        return text.lower() == "check weather"
    
    def on_enter_get_city_temperature(self, event):
        self.city = event.message.text #expect user to input city name here
        if self.city in cities:
            send_text_message(event.reply_token, "為您查詢中")
            self.city_exist(event)
        else:
            send_text_message(event.reply_token, "此城市不存在!")
            self.city_not_exist(event)

    def on_enter_get_temperature(self, event):
        print("Time to check temperature")

        message = self.city + "當前溫度為攝氏 " +  get_temperature(self.city) + " 度"
        reply_token = event.reply_token
        send_text_message(reply_token, message)
        self.done()

    def on_exit_get_temperature(self):
        print("Done checking")

    def on_enter_get_weather(self, event):
        print("Time to check weather")

        message = self.city + "當前天氣狀況為 " +  get_weather(self.city)
        reply_token = event.reply_token
        send_text_message(reply_token, message)
        self.done()

    def on_exit_get_weather(self):
        print("Done checking")
