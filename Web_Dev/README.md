All web development courses and projects I have completed thus far:

![cert1](cert1.jpg)


This certificate above verifies that Andrew Yu Ming Xin successfully completed the course [The Modern Javascript Bootcamp Course (2022)](https://www.udemy.com/course/javascript-beginners-complete-tutorial/) on 07/03/2022 as taught by Colt Steele, Stephen Grider on Udemy.
The certificate indicates the entire course was completed as validated by the student.
The course duration represents the total video hours of the course at time of most recent completion.

- [Section_8_Challenge_1](Section_8_Challenge_1): functions, De Morgan's Law, .includes
- [Section_8_Challenge_2](Section_8_Challenge_2): for...of (iterable)
- [Section_8_Challenge_3](Section_8_Challenge_3): 
- [Section_8_Challenge_4](Section_8_Challenge_4): Math.floor(Math.random() * n) = [0,n-1]/[0,n)
- [Section_14_NBA_Scores_Chart](Section_14_NBA_Scores_Chart): Destructuring ftw
- [Section_20_Timer](Section_20_Timer): 
```
- Class, optional args
- "this" in arrow func refers to that class' object since underlying implemention hoists func into constructor (as evident in Babel)
- "get" and "set" keywords enable usage as if an attribute
```
- [Section_21_Movie_Fight](Section_21_Movie_Fight): 
```
- Drawing diagrams on https://app.diagrams.net/ to help planning & visualization
- Bulma framework
- emphasis on independence of .html & .js files/reusability & zero knowledge of project
- Abstraction via helper funcs (input debounce)
- Closing dropdown on click outside
// e.target reveals the element clicked on, anywhere in the document.
document.addEventListener("click", (e) => {
 // If any element in the root is clicked, dropdown will remain open. Otherwise, will close.
 if (!root.contains(e.target)) dropdown.classList.remove("is-active");
 });
};
- HTML data attributes (data-xxxx is in .dataset.xxxx)
- MochaJS Testing Framework Library + Chai, browser-specific example 
```
- [Section_22_Maze](Section_22_Maze): 
```
- MatterJS Physics <canvas> API
- const {World, Engine, Runner, Render, Bodies, Body, Mouse, MouseConstraint, Events} = Matter;
  const engine = Engine.create();
  const {world} = engine;
  const render = Render.create({
    element: ...,
    engine: engine,
    options: {...},
  });
  const runner = Runner.create();
  Render.run(render);
  Runner.run(runner, engine);
  // World.add(world, ...);
  // Bodies.[shape](...)
  // Body.setVelocity(...)
  // MouseConstraint.create(engine, {mouse: Mouse.create(render.canvas)})
- const grid = Array(cellsVertical) // Rows
    .fill(null) // Cannot just do .fill([false, false, false]), as they are the exact same arrays in memory, hence Eg. grid[0].push(true) will edit all 3 arrays
    .map(() => Array(cellsHorizontal).fill(false)); // Columns
- Bodies....(..., {label: "...", isStatic: true, render: {fillStyle: "..."}}
- Workaround for clipping issues due to current lack of CCP
- // Listening for events inside world object allows to create Win Condition
  Events.on(engine, "collisionStart", (e) => {
    // Chrome reuses the e each time, overwriting all info of prev es, hence need to loop thru e.pairs array
    e.pairs.forEach((collision) => {
      // collision array: {id: '...', bodyA: {…}, bodyB: {…}, collision: {…}, ...}
- // clearing MatterJS-related, so doesn't affect the next run thru recursion, etc
    World.clear(world);
    Engine.clear(engine);
    Render.stop(render);
    Runner.stop(runner);
    render.canvas.remove();
    render.canvas = null;
    render.context = null;
    render.textures = {};
```
- [Section_23_Secret_Msg_Sharing_App](Section_23_Secret_Msg_Sharing_App):
```
- event.preventDefault(): prevents default browser behavior to submit info in form to a backend server (appearing as if refreshing)
- b64-encoding is basically combining all bits then splitting from ASCII (8) to base64 (6) (ASCII<->base64 = btoa(...)<->atob(...))
- Deploying live via "npx now" in console with NodeJS installed
```
- [Section_24_NodeJS_CLI_nls](Section_24_NodeJS_CLI_nls):
```
- Creating a command
1. cd into most direct parent folder of index.js
2. #!/usr/bin/env node (1st line of index.js, to treat like an executable)
3. "npm init -y" (package.jsonl, containing impt "scripts", "dependencies")
4. bin (alternative command to execute binary, executable)
5. "npm link" (package-lock.json)
6. "npm i NAME/NAME@VERSION_NO" (libraries installed from npmjs.com, node_modules)
7. "npm exec CMD_NAME" / "npx CMD_NAME" to run CMD_NAME
   If some Windows Error: Invalid character 800A03F6, right-click any .js file, "Properties">"Open with">Locate Eg. C:\Program Files\nodejs\node.exe
8. Executables bin commands are in "%appdata%\npm"
- fs (.lstat(FILE_PATH) then .isFile/isDirectory() to know if file or folder, .readdir), util (.promisify), path (.join(DIR, FILE), chalk (.bold, .blue) [need to use "npm i chalk@4.1.2" (latest version built with CommonJS), to prevent "[ERR_REQUIRE_ESM]: require() not supported"]
- Callback (confusing quickly esp if adding more layers of complexity (unscalable)) vs Promise (Runs sequentially awaiting for each lstat, so quite slow) vs Promise.all (Runs parallel, seems sychronous)
- process.argv for array of CLI args, process.cwd() for cwd path
```
- [Section_25_NodeJS_CLI_watch](Section_25_NodeJS_CLI_watch):
```
- Lodash.debounce, Chokidar (.watch, .on), Caporal (.version, .argument, .action, .parse), child_process (spawn, .kill)
- Details on StdIO and child_process, in C notes.
```
- [Section_26_Future_Amazon](Section_26_Future_Amazon):
```
- require("FILE_PATH"), module.exports = ...
- fs (.access, .writeFile, .readFile
- crypto (.randomBytes(NUM).toString("hex"), .scrypt(PASSWORD, SALT, BITS)
- ExpressJS (express(), .Router(), .static("PUBLIC_DIR"), .use, .listen, .get/post(ROUTE (Eg. /:id can get id variable from URL), [ANY_VALIDATORS], ANY_MIDDLEWARE_FUNCS, (req, res)=>{}), req["session"], res.send/redirect
- Nodemon
- Cookie-session (cookieSession({keys: ["RANDOM_ENCRYPTION_KEY"]})
- Express-validator (check(...).trim/normalizeEmail/isEmail/isLength/isFloat/withMessage/custom(), errors.mapped()[property].msg to convert [errors]->{property: {msg: "..."}}
- Multer (({storage: multer.memoryStorage()}), .single("image"))
- Funcs in constructors CANNOT be async in nature. HENCE use sync versions all sync versions inside / async funcs outside & invoke separately 
- Object.assign(record, attrs): k-v pairs of later (attrs) copies (if doesn't exist) & overwrites (if exists) earlier (record) objects
```
- [Section_33_TME](Section_33_TME):
```
- jsdom ({JSDOM}.fromFile().window.document...)
- addEventListener("DOMContentLoaded", ...) to wait for all JS files to be loaded first
- global.STH (Node will first find if "STH" was defined anywhere in current file. If not, will find in global variables which are shared between ALL diff files)
```
<hr>

![cert2](cert2.jpg)

This certificate above verifies that ANDREW YU MING XIN successfully completed the course [The Complete 2023 Web Development Bootcamp](https://www.udemy.com/course/the-complete-web-development-bootcamp/) on 12/14/2023 as taught by Dr. Angela Yu on Udemy. 
The certificate indicates the entire course was completed as validated by the student. 
The course duration represents the total video hours of the course at time of most recent completion.

- [Extra: About Me](Extra_About_Me): 
- [Extra: CV](Extra_CV): 
- [Extra: TinDog](Extra_TinDog): Learnt CSS advanced concepts,ordering & Bootstrap

- [Exercise_1_Life_Left](Exercise_1_Life_Left): let, \`${}\`
- [Exercise_2_BMI_Calc](Exercise_2_BMI_Calc): let VAR; (undefined)
- [Exercise_3_FibonacciGenerator](Exercise_3_FibonacciGenerator): const for arrays, array methods
- [Exercise_4_DiceGame](Exercise_4_DiceGame): 
```
document.getElementsbyTagName(), .getElementsbyClassName(), .getElementById(), .querySelector(), .querySelectorAll()
ELE.attributes, .getAttribute, .setAttribute, .classList.add/remove/toggle, .style vs getComputedStyle()
ELE.innertext, .textcontent, .innerHTML, .insertAdjacentHTML
```
- [Exercise_5_DrumKit](Exercise_5_DrumKit): switch, Audio, addEventListener, setTimeout
- [Extra_Exercise_5_Piano](Extra_Exercise_5_Piano): Just a fun variation of Drumkit, with Piano Keys instead!
- [Exercise_6_SimonGame](Exercise_6_SimonGame): A bit more complicated logic
- [Exercise_7_BMI_Calc_Server](Exercise_7_BMI_Calc_Server): 
```
Web app version of [Exercise_2_BMI_Calc](Exercise_2_BMI_Calc)
HTML forms with Javascript
body-parser middleware integrated into native ExpressJS via express.urlencoded({extended: true})
res.write/.send/.sendFile/.render/.redirect()
In serving local ∴ static files, use __dirname, app.use(express.static("public"));
```
- [Exercise_8_ToDoList](Exercise_8_ToDoList):
```
EJS Templating: app.set("view engine", "ejs"), <%= %>, <% %>, usage of name="" + value="" to redirect to diff POST path
HTML Layout/Partials: <%- include("header/footer/AnotherHTMLfile") -%>
module.exports / exports / exports.someFunc = someFunc + require...
```
- [exercise_9_react_notes](exercise_9_react_notes):
```
// IMPT
function deleteNote(id){
        setNotes((prevNotes) => {
            return prevNotes.filter((note, index) => index !== id)
        })
    }
// Adding id to note
{notes.map((note, index) => <Note key={index} id={index} }/>)}

Material-UI Core + Icons
Pre-built using Google's Design Concept React Components (∴ > bootstrap/favicons)
```
- [exercise_10_react_emojipedia](exercise_10_react_emojipedia):
```
Babel, JSX
Inline CSS for updating on-the-fly
import React from "react"
import ReactDOM from "react-dom/client", ReactDOM.createRoot(document.querySelector("#root")).render(<App />);
export default NAME
React Custom Props
```
- [exercise_11_react_todolist](exercise_11_react_todolist):
```
import {useState} from "react"
useState Hooks
Array, Object Destructuring
Arrow funcs () => {} for delayed execution
```
<hr>

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

## Firebase (Backend/Database)
1. http://console.firebase.google.com/
2. Create Project
3. Build > Realtime Database > Create Database, Test Mode, Enable > Rules > change "now < ..." to "auth.uid != null"
4. Build > Authentication > Get Started > Enable Email/Password
5. Project Overview icon > Project Settings > Web API Key 
6. Eg. [FirebaseGuide](FirebaseGuide.py)

## Useful Websites:
1. [BS syntax, docs, examples](https://getbootstrap.com/docs/5.1/), test on [CodePly](https://www.codeply.com/)
2. [Learn UI-UX design patterns](http://ui-patterns.com/patterns) , [Inspiration](https://dribbble.com/search)
3. [Wireframe via sketching](https://sneakpeekit.com/)  / [templating](https://balsamiq.cloud/)
4. Mock-up via Photoshop, Illustrator
5. Prototype via animated replica

- [BS theme templates](https://startbootstrap.com/themes)
- [Download JS library files](https://cdnjs.com/)
- [Favicon (Tab icon)](https://favicon.io/)
- Apple, Instagram logo, etc icons: [Font Awesome (Add images to HTML class)](https://fontawesome.com/icons), [Flat icon](https://www.flaticon.com/), [Noun Project](https://thenounproject.com/), [StorySet](https://storyset.com/)
- [UIUX Designs](https://dribbble.com/)
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

