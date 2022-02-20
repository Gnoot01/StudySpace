This is a simple working prototype of booking 'competitively' at 9am each day 3 days in advance for the gym slot on ActiveSG, which gets snatched up in minutes 
(esp so for the more popular timings like 9am, 11am, 5pm, 7pm, etc).

ActiveSG utilizes Google recaptchav2, which enables users to pass the captcha just by clicking on it. Looks at how you behaved prior to clicking eg. 
how your cursor moved on its way to the check (organic path/acceleration), which part of the checkbox was clicked (random places, or dead on center every time using 
click location history tied to your acc), browser fingerprint, Google cookies & contents

Bypass Method 1: Often most reliable and because ActiveSG doesn't really protect against this, allow some time.sleep() to do it yourself

Bypass Method 2: [Captcha services](https://2captcha.com/) $3/1000 recaptchas, can use their API or library. Not recommended since this version of recaptcha2 is quite simple and would not be sound time-wise (requests are submitted and need to be solved by human workers at the receiving end/some delay if requests get rejected/long queue times) or financially, since ActiveSG doesn't really protect against this

Bypass Method 3: [Open-sourced captcha bypass](https://github.com/ecthros/uncaptcha2) but this is for the audio-images version of uncaptcha2, unlike the click-and-go version on ActiveSG.
