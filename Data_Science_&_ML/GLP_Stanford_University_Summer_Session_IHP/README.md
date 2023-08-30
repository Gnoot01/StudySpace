I went to Stanford University, California, United States as part of my Global Leadership Programme, where I undertook 2 credit-transfer mods. They were extremely enriching, covering numerous Data Science concepts and methods.

I attained __ for [DATASCI 154](https://summer.stanford.edu/courses/datasci-154-solving-social-problems-data) (5 units) and __ for [SOC 128D](https://summer.stanford.edu/courses/soc-128d-mining-culture-through-text-data-introduction-social-data-science) (3 units)

![transcript](transcript.pdf)

# DATASCI 154
Explored the more theoretical side of Data Science
- Frame - Connect - Design Framework
- Causal Inference (Difference-in-Differences(DiD), Regression Discontinuity Design (RDD), Randomized Control Trial (RCT))
- Confounders (Eg. Common Shock)
- Optimization
- Politics & Ethics of Data
- Information to Action
- Political Polarization
- School Choice & Segregation
- Climate Mitigation
- Final Project: “How should Twitter balance Machine Learning with Human Input in their hate speech detection framework to minimize racial discrimination against minority users on their platform?”
- [ESR_Examples](DATASCI_154/ESR_Examples/Ethics_and_Society_Review.docx): Ethics and Society Review (ESR) vs Institutional Review Boards (IRB) Statement
- [PS3](DATASCI_154/PS3/PS3_AndrewYu.ipynb): importing custom module on Google Colab, np.linspace()
- [PS4](DATASCI_154/PS4/PS4_AndrewYu.ipynb): Open source “reduced complexity” climate model FaIR, General circulation models (GCMs)

# SOC 128D
Explored methods in relation to Climate Change issues like Hurricane Katrina, Cape Town Day Zero, Colorado River

Fully taught in R, but I challenged myself to research and complete all assignments in Python instead
- APIs: 
```
Google Search Interest: Pytrends
- Interest Over Time: .build_payload(...), .interest_over_time()
- Multirange Interest Over Time: .multirange_interest_over_time()
- Historical Hourly Interest: .get_historical_interest(kw_list, year_start=2005, month_start=1, day_start=1, hour_start=0, year_end=2023, month_end=7, day_end=1, hour_end=0, ...)
- Alphabetical Interest By Region: .interest_by_region(resolution='CITY/DMA/COUNTRY/REGION', inc_low_vol=True, inc_geo_code=False)
- Related Topics: .related_topics()["kw_list QUERY TERM"]["top/rising"]
- Related Queries: .related_queries()["kw_list QUERY TERM"]["top/rising"]
- Trending Searches: .trending_searches/realtime_trending_searches(pn='US')
- Yearly Top Charts: .top_charts(date, geo='GLOBAL')
- Suggestions: .suggestions(keyword)
```
- Text Mining: [ProQuest DTM](https://tdmstudio.proquest.com/home) (Geographic, Topic Modelling, Sentiment Visualization), nltk, PyPDF2
- Sentiment Analysis: plotnine (R ggplot), NRCLex, Afinn
- Topic Modelling: CountVectorizer, WordNetLemmatizer, LatentDirichletAllocation (LDA), GridSearchCV
- Maps and Spatial Data: geopandas, shapely, pygris
- Networks and Inequality: measures of centrality, igraph
- Final Project: "What can we learn about climate change through sentiment analysis across different social media platforms?"
