[The Complete 2022 Web Development Bootcamp](https://www.udemy.com/course/the-complete-web-development-bootcamp)

- [Extra: About Me](Extra_About_Me): 
- [Extra: CV](Extra_CV): 
- [Extra: TinDog](Extra_TinDog): Learnt CSS advanced concepts,ordering & Bootstrap
- [Section_8_Challenge_1](Section_8_Challenge_1): functions, De Morgan's Law, .includes
- [Section_8_Challenge_2](Section_8_Challenge_2): for...of (iterable)
- [Section_8_Challenge_3](Section_8_Challenge_3): 
- [Section_8_Challenge_4](Section_8_Challenge_4): Math.floor(Math.random() * n) = [0,n-1]/[0,n)
- [Section_14_NBA_Scores_Chart](Section_14_NBA_Scores_Chart): Destructuring ftw
- [Section 20 Timer](Section_20_Timer): Class, optional args, "this" in arrow func refers to that class' object since underlying implemention hoists func into constructor (as evident in Babel)


## Hosting website on Github:
1. make repo public
2. Settings>Pages>Source (main), save>if error 404, wait ~30 mins & try again 
3. Ensure .html files can be accessed (not in folders, etc?)

## Deploying Webapp using [Heroku](https://www.heroku.com/), gunicorn
1. Create new app > input unique App name > Create app
2. Deploy > (Deployment method > GitHub > Connect + Automatic Deploys > Enable Automatic Deploys + Manual Deploy > Deploy Branch) > View (Success should see 'Application error')
3. Viewing Heroku logs: On your Webapp's dashboard page, More > View Logs (If 'No web processes running', successfully hosted on Heroku, but doesn't know how to run app (need to setup WebServerGatewayInterface server with gunicorn which standardises language and protocols b/w Python Flask application & host server since normal web servers can't run Python applications. Python->WSGI via gunicorn->Heroku))
```
Hence,
4. Files > Settings > Project:... > Python Interpretor > + > gunicorn (Note version number)
5. Create/Add to requirements.txt 'gunicorn==(version number)'
6. Create Procfile file, 'web: gunicorn main:app'  (Telling Heroku to create a web worker able to receive HTTP requests, use gunicorn to serve Webapp, which is the Flask app object in main.py)
7. Commit & Push updated to GitHub, on dashboard, Open app
```
## SQLite -> PostgreSQL in Heroku
1. Files > Settings > Project:... > Python Interpretor > + > psycopg2-binary (Note version number)
2. Create/Add to requirements.txt 'psycopg2-binary==(version number)'
3. Commit & Push updated to GitHub (delete & ensure no pipfile/pipfile.lock files in GitHub repo)
4. On dashboard, Resources > Add-ons > Heroku Postgres > Hobby Dev-Free > Submit Order Form
5. On dashboard, Settings > Reveal Config Vars (same as .env file)
6. Copy name of the database config var (Eg. DATABASE_URL), replace app.config["SQLALCHEMY_DATABASE_URI"] to = os.environ.get("DATABASE_URL", "sqlite:///___.db") so will use either depending on if run on Heroku or locally

## Useful Websites:
1. [BS syntax, docs, examples](https://getbootstrap.com/docs/5.1/), test on [CodePly](https://www.codeply.com/)
2. [Learn UI-UX design patterns](http://ui-patterns.com/patterns) , [Inspiration](https://dribbble.com/search)
3. [Wireframe via sketching](https://sneakpeekit.com/)  / [templating](https://balsamiq.cloud/)
4. Mock-up via Photoshop, Illustrator
5. Prototype via animated replica

- [BS theme templates](https://startbootstrap.com/themes)
- [Download JS library files](https://cdnjs.com/)
- [Favicon (Tab icon)](https://favicon.io/)
- Apple,Instagram logo, etc icons: [Font Awesome](https://fontawesome.com/icons), [Flat icon](https://www.flaticon.com/)
- [Gifs](https://giphy.com/)
- Colors: search <colors> MDN, [Color Hunt](colorhunt.co), [Color Theory](https://color.adobe.com/create/color-wheel)
- Fonts: [Google Fonts](https://fonts.google.com/), [Font Families](https://www.cssfontstack.com/)
- [Mobile-friendly test affecting google searching rankings](https://search.google.com/test/mobile-friendly)

## Some important notes:
```
4 pillars of Good Design - 1. Color Theory, 2. Typography, 3.UI, 4.UX
Color Theory - mood to predominant color 
  (Red:Love, Energy, Intensity|Yellow:Joy, Intellect, Attention|Green:Freshness, Safety, Growth|Blue:Stability, Trust, Serenity|Purple:Royalty, Wealth, Femininity)
   Egs. Car                         Workout                         Food                            Paypal, Coinbase                Payday Loans
               secondary color: color diff shade of predominant color to create analogous color palette (navigation bars, body, logo & background) +:eye-soothing -:doesn't stand out
                            OR  color directly opp of predominant color to create complementary/clashing color palette +: stands out, -:very jarring on eg. text & text bg
Typography - Serif subfamily: Old Style(winery), Transitional, Modern(VOGUE) (can tell the age & HENCE target audience by the diff b/w thickest and thinnest parts of the same letter. old->modern less diff->more diff Eg. O, O, O)
      VS     Sans-Serif subfamily (highly legible (PHOTOS)(for body text): Grotesque, Humanist, Geometric
UI - Perception Hierarchy via 1.colors 2.size 3.weight 4.layout (eg. 40-60 chars per line for non-tedious, non-choppy+awkward to read),
                              5.alignment (draw a line going thru beginning of each item - TICK less lines) 6.white space (minimalistic, isolate prdt & inject exclusivity, impt)                               7.target audience
UX - 1.Simplicity 2.Consistency(navbar) 3.Reading Patterns(F pattern generally, Z pattern for more sparse, more img/vid content)
     4.Responsiveness 5.X Dark Patterns (Trickery to get ppl to do sth they didn't mean/want to) Eg. Shopee, Amazon auto selecting express delivery & making it stand out to profit/Curved line as a hair on mobile to click on website & profit/Purposely confusing checkboxes for email newsletter, etc
```
