Inspired to create this after hearing my sister's struggles of booking a gym slot, especially for the more popular gyms.
Also ActiveSG website is horribly hard to navigate (inconsistent nav bars, menu-dropdown presenting non-fruitful results for some reason)

OK I actually managed to deploy to Heroku - everyone saying pythonanywhere easier etc etc but man couldn't figure out where to start
Massive kudos to this [GOAT](https://www.youtube.com/watch?v=rfdNIOYGYVI)
Originally didn't know how to deploy/if can deploy non-web apps easily, so didn't want to bother, but later felt a bit sad people don't get to use it, so I tried anyway.
And I'm so glad I tried! :D :D :D :D

Learning points, and necessary changes to deploy on Heroku on my deploy_aktivesgbot repo

Update: However, reportedly by my users (just my sis actl), it's still a tad too slow compared to the app which already cached the log in. So discovered the purpose of this bot is simply to check and book spontaneously, not competitively in wee hours of the morning when slots open up. I'll figure out a different bot for that, solving captchas should be fun...

Ideas for improvement: 
```
1. use Persistence to remember user's data choices/watchlist for slots that free up when users cancel their booking, if they opt to. Hourly checking frequency?
2. Competitive Booking during slot-opening time
```
