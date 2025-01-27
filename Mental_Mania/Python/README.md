<p align="center">
<h1 align="center"> Mental Mania in Python 🐍 </h1>
</p>

Some of the project ideas noted down in my Mental Mania notes, brought to life.

Each of them has some notion for enhancement in future.

## Projects
- [Telegram_Chat_Analyzer](Telegram_Chat_Analyzer):
```
chromedriver-autoinstaller for up-to-date selenium chromedriver
Natural Language Toolkit (NLTK) for stop words (common meaningless words)
os.walk (files) vs os.listdir (files & folders) vs fnmatch (filtering files by extension)
need .copy() to iterate & change-on-the-fly (.pop) if not RuntimeError: dictionary changed size during iteration

sorted ALW returns a list. OrderedDict returns a dict with preserved order after sorting.
.items() returns tuple of (k, v). Within this tuple, key[1] returns v to sort by, X word_count[user][key]!
Eg. word_count[user] = OrderedDict(sorted(word_count[user].items(), key=lambda key: key[1], reverse=True))

NEED BOTH encoding="utf-8" & ensure_ascii=False to force UNICODE-representation (i'm instead of i\u2019m)
```
- [SP_YT_Playlist_Converter](SP_YT_Playlist_Converter):
```
emoji to manipulate emoji unicodes
undetected_chromedriver as one of bypasses to using Selenium to sign in to Google account
OAuth 2.0 flow and pickles
Handling pagination of results to get full results
```
- [SUTD_GPACalculator](SUTD_GPACalculator):
```
Exemplar modularity and programming practices
Accessing files works as a pointer, so reading once through leaves pointer at last char
Hence f.read() again will read nth. Need to reset pointer or store file contents
file.tell() to give position, .seek() to a position, .truncate(_) to _ bytes, .flush() to write cache
```
- [Physics_Practices_Scrapper](Physics_Practices_Scrapper):
```
with open(..., "wb")... to save images as .jpg
docx Document(), .add_heading(), .add_picture(), .save()
docx2pdf.convert() to convert .docx to .pdf
os.remove() to delete specified files
```

## Tools and technologies
- YT Data v3 API
- Spotipy API
- Authentication via OAuth 2.0 flow

@Gnoot01 🐍 2022
