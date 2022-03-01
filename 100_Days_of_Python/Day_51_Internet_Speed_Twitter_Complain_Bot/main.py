"""
Original was only InternetSpeedTwitterBot, but I didn't know my guaranteed speeds or even who my ISP was, so added a lil more spice to find out >:)
1. Check ISP: https://www.whoismyisp.org/ (StarHub-Ltd-NGNBN-Services)
2. I'm not sure about guaranteed speeds, so I check range of down/up speeds for the ISP on http://www.speedtest.com.sg/latest_result_starhub.php
3. Fairly compare current speeds on https://www.speedtest.net/ with average, based on ISP & OS
4. Singapore Signature Move - Complain! (inspiration from https://www.vice.com/en/article/yp3vzj/this-bot-will-tweet-at-comcast-whenever-your-internet-is-slower-than-advertised)
"""

from SpeedCheck import SpeedCheck
from InternetSpeedTwitterBot import InternetSpeedTwitterBot

CHROME_DRIVER_PATH = "V96_chromedriver.exe"

speedcheck = SpeedCheck(CHROME_DRIVER_PATH)
twitter_bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
twitter_bot.check_current_dlul_speeds()

if twitter_bot.current_dl_speed < speedcheck.MY_ISP_avg_dl_speed or twitter_bot.current_ul_speed < speedcheck.MY_ISP_avg_ul_speed:
    twitter_bot.tweet_at_provider(round(speedcheck.MY_ISP_avg_dl_speed, 2), round(speedcheck.MY_ISP_avg_ul_speed, 2))
