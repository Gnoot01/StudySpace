"""
Takes a PDF file, identifies the text and converts the text to speech.
https://aws.amazon.com/polly/, Free Tier: 1 million characters with Neural Voice / 5 million characters with Normal Voice
Full SSML tags functionality with Normal Voice too.
SSML:
,/-/...: <break>
b/w sentences: <s>
b/w paragraphs: <p>
bold/italicised: <emphasis>
french/spanish words (Eg. entre): <lang>
acronym/1234/1234th/(3/20)/(09242003)/1'21"/address/:<say-as interpret-as="spell-out/number/ordinal/digits/fraction/date/time/address/telephone">
whisper synonyms: <amazon: effect name="whispered">
shout synonyms: <prosody volume="loud">
excited/happy synonyms: <prosody rate="fast" pitch="high">
tired/lazy synonyms: <prosody pitch="low">
<amazon:auto-breaths>
However, needs credit card details to even register so opted for https://www.ispeech.org/
Update: Never mind, requires credit card details too. I'll come back to this.

Some insightful research and libraries (pyttsx3, pdfplumber, PyPDF2): https://thecleverprogrammer.com/2020/11/15/convert-pdf-to-audiobook-using-python/
"""
