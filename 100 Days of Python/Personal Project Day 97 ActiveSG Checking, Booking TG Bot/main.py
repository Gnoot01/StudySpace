"""
I learnt alot doing this, TG Bot is a super-extremely awesome way to automate stuff since I can call commands in it from the mobile app,
to execute commands on my computer at home.
Most important learning point is ConversationHandler -
1. What I call a healthy function is when each function in the conversation does sth (passive) then ask for sth (user's input, active)
to proceed in the conversation.
2. A lazy function is when it only does something resulting in user needing to input the same answer x2 to proceed to the next step.
3. Likewise, A hyper function is when it does too many things and can probably be broken down into 2 healthy functions.
In the specified STATE, that STATE should accept the conditions needed to pass THAT STATE, and not for the previous one.
(which if the case, there's probably a lazy function. (Eg. VENUE: venue only does sth (passive), but doesn't ask for user
 input/asks for wrong user input (DATE: date) instead of VERIFY: verify_venue.) Therefore, docstrings are very critical to establish
 the purpose of that function, especially in ConversationHandler to ensure a healthy one.

Try as I might, cannot seem to find a way to use beautifulsoup+requests instead of selenium to login to ActiveSG.
Other projects involving ActiveSG are at least 5 years old, and I tried their methods but unsuccessful:
https://github.com/davidheryanto/activesg/blob/master/activesg.py, https://github.com/zhangyongsong/badminton_court_booking/blob/master/book_court.py
From what I take away, is that the form has 4 fields: login, ecpassword (encrypted by what method?? using what??), rsapublickey, _csrf
"""
import os
import logging
import datetime
import random
from generator import Generator
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, ConversationHandler, Filters
 
# Enable logging
# Eg. 14/02/2022 08:00:00 | start() in main.py | LogLvl=INFO, Line 5: ..., level: only severity level >= specified will be shown (DEBUG<INFO<WARNING<ERROR<CRITICAL)
# can add filename='logs.log', filemode='a' to append logs into logs.log file instead of displaying in terminal
logging.basicConfig(format='%(asctime)s | %(funcName)s() in %(filename)s | LogLvl=%(levelname)s, Line %(levelno)s: %(message)s', 
                    level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

# API TOKEN from @BotFather
TOKEN = os.environ.get("TOKEN")
CHOSEN_ACTIVITY = None
CHOSEN_VENUE = None
ALL_ACTIVITIES = Generator().all_activities
ACTIVITY, VENUE, VERIFY, DATE, BOOK = range(5)


def start(update: Update, context: CallbackContext) -> None:
    """Starts the bot and gives guidance"""
    update.message.reply_text("Ready to get Aktive at AktiveSG anot? Talk to me or /help to see what to do")


def help(update: Update, context: CallbackContext) -> None:
    """Describes bot, and gives tips"""
    update.message.reply_text("I am AktiveSGBot, designed to help you make informed decisions on scheduling your workouts.\n"
                              "You can use me to check the *availability* of *any activity's* timeslots at *any venue* and *book slots* right at your finger tips!\n"
                              "Use me as much as possible and report any bugs to my hooman 🤡\n"
                              "/check to *start*\n"
                              "At any point, you can /quit to *quit* the bot",
                              parse_mode=ParseMode.MARKDOWN)


def check(update: Update, context: CallbackContext) -> int:
    """Starts the checking functionality then asks for desired activity."""
    reply_keyboard = [["badminton"], ["basketball"], ["floorball"], ["flying disc"], ["futsal"], ["gateball"], ["gym"], ["hockey"],
                      ["hockey (night)"], ["lawn bowl"], ["netball"], ["open air fitness corner 2021"], ["organised programme"],
                      ["outdoor"], ["petanque"], ["pickleball"], ["sepak takraw"], ["soccer"], ["soccer (night)"], ["squash"],
                      ["street soccer"], ["swim"], ["table tennis"], ["tennis"], ["tennis wall"], ["volleyball"]]
    update.message.reply_text(f'So {update.effective_user.first_name}, choose the *activity*:', parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='or type, in lower case please!'))
    return ACTIVITY

# Basically, when press button on Inline Keyboard, there's callback_query in the msg sent. Can then retrieve query_data by callback_query.data 
# from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import CallbackQueryHandler
# def check(...): ...
#     # Inline keyboard
#     reply_keyboard = InlineKeyboardMarkup([
#                        [InlineKeyboardButton("Badminton", callback_data='badminton')],
#                        [InlineKeyboardButton("Basketball", callback_data='basketball')],
#                        [...]...
#                      ])
#     ...

# def button(update: Update, context: CallbackContext) -> None:
#     query_data = update.callback_query.data
#     # Remove buttons, same as ReplyKeyboardMarkup's one_time_keyboard=True
#     update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
#     ...

# updater.dispatcher.add_handler(CommandHandler('check', check))
# updater.dispatcher.add_handler(CallbackQueryHandler(button))


def activity(update: Update, context: CallbackContext) -> int:
    """Stores the selected activity then asks for desired venue."""
    global CHOSEN_ACTIVITY
    user = update.message.from_user
    msg = update.message.text
    CHOSEN_ACTIVITY = msg.title()
    logger.info(f"Activity chosen by {user.first_name}: {msg}")
    update.message.reply_text("Great choice!\n"
                              "And which *venue* would you like to check for this activity?\n",
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardRemove())
    return VENUE


def venue(update: Update, context: CallbackContext) -> int:
    """Checks the chosen venue and asks to verify the venue"""
    global CHOSEN_ACTIVITY
    user = update.message.from_user
    msg = update.message.text
    logger.info(f"Venue chosen by {user.first_name}: {msg}")
    update.message.reply_text("Checking if venue exists in our database...")

    generator = Generator(activity=CHOSEN_ACTIVITY)
    if generator.first_avail_venue_id is None:
        update.message.reply_text("ActiveSG doesn't seem to have any venues for this activity presently, try another activity?")
        return check(update, context)

    venues = generator.gen_all_avail_venue_ids()
    found_partial_match = False
    msg_split = msg.title().split(" ")[0]
    matches_keyboard = [[venue] for venue in venues.keys() if msg_split in venue.split(" ")]
    for venue in venues.keys():
        # Can further split(" "), check len(list), then check for word in list: if word in venue_split:...
        venue_split = venue.split(" ")
        # Exact match
        if msg.title() == venue:
            update.message.reply_text(f"Exact match found: {venue}\n"
                                      "Is this it?",
                                      reply_markup=ReplyKeyboardMarkup([[venue]], one_time_keyboard=True))
            return VERIFY
        # Partial match, give choices that match as buttons
        # This found_partial_match, without break is necessary as msg_split takes only first word of msg. Hence,
        # Eg. User input: Jurong West Sports Hall, and there's Jurong East Sports Hall then Jurong West Sports Hall.
        # msg_split = Jurong. On loop to Jurong East Sports Hall, found_partial_match = True. BUT doesn't break/Partial match->return VERIFY, so that
        # next loops can find Exact match -> directly return VERIFY.
        elif msg_split in venue_split:
            found_partial_match = True
    if found_partial_match:
        update.message.reply_text("Partial match found, did you mean any of these?\n"
                                  "/disappointed if you don't see your venue",
                                  reply_markup=ReplyKeyboardMarkup(matches_keyboard, one_time_keyboard=True))
        return VERIFY
    # No match
    update.message.reply_text("I'm sorry I couldn't find your venue 😔\n"
                              "Click /disappointed")
    return VERIFY


def verify_venue(update: Update, context: CallbackContext) -> int:
    """Verifies the venue and asks for desired date+days"""
    global CHOSEN_VENUE
    user = update.message.from_user
    msg = update.message.text

    generator = Generator(activity=CHOSEN_ACTIVITY)
    venues = generator.gen_all_avail_venue_ids()
    venue_matched = False
    for venue in venues:
        if msg == venue:
            venue_matched = True
            break

    if venue_matched:
        CHOSEN_VENUE = msg
        logger.info(f"Successfully found a venue: {msg} for {user.first_name}")
        today = datetime.datetime.now().strftime('%d %m %Y')
        today_split = today.split(" ")
        update.message.reply_text("Hooray! I found your venue! Kindly follow the 3 steps below.\n"
                                  "1. What's the date to check? (DD MM YYYY)\n"
                                  "2. How many days from today to check? (X)\n"
                                  "    Min: 0\n"
                                  "    Max: 3 for gym, swim, organised programme\n"
                                  "              15 for the everything else\n"
                                  "3. Answer in 1 sentence, with spaces in this\n"
                                  "    format: DD MM YYYY X\n"
                                  "*Eg: '1 1 2022 2' will check slots for 1 1 2022, 2 1 2022, 3 1 2022*\n\n"
                                  f"For convenience: /skip to check for *today and only today: {today} 0\n"
                                  f"(DD={today_split[0]}, MM={today_split[1]}, YYYY={today_split[2]}, X=0)*",
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=ReplyKeyboardRemove(),
                                  )
        return DATE

    logger.info(f"{user.first_name} typed: {msg}, which doesn't match with any venue. Redirecting back to VENUE")
    update.message.reply_text("Sorry, *invalid response*! Let's go back to checking another venue C:",
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardRemove())
    return VENUE


def no_venue_found(update: Update, context: CallbackContext) -> int:
    """Displays entire venue list and asks to verify the venue"""
    user = update.message.from_user
    logger.info(f"No matches found for User {user.first_name}")
    generator = Generator(activity=CHOSEN_ACTIVITY)
    venues = generator.gen_all_avail_venue_ids()
    venues_keyboard = [[venue] for venue in venues.keys()]
    update.message.reply_text("Here's all the venues in my database\n"
                              "Did you mean any of them?",
                              reply_markup=ReplyKeyboardMarkup(venues_keyboard, one_time_keyboard=True))
    return VERIFY


def date(update: Update, context: CallbackContext) -> int:
    """Generates & displays available timeslots for desired date+days then asks for date to book"""
    user = update.message.from_user
    msg = update.message.text
    msg_split = msg.split(" ")
    chosen_date = ' '.join(msg_split[:-1])
    chosen_days = int(msg_split[-1])
    logger.info(f"User {user.first_name} wants to check for {chosen_days} days from {chosen_date}")
    update.message.reply_text("Generating available slots, sit tight!", reply_markup=ReplyKeyboardRemove())

    generator = Generator(activity=CHOSEN_ACTIVITY, date=chosen_date)
    result, dates = generator.gen_availability(venue=CHOSEN_VENUE, days_num=chosen_days)
    date_btns = [[date] for date in dates]

    reply_text = f"These are the available timeslots for *{CHOSEN_ACTIVITY}* at *{CHOSEN_VENUE}* from *{chosen_date}*\n"
    if CHOSEN_ACTIVITY == "Gym": reply_text += "Opening hours:\nMon, Wed, Fri: 7am-10pm | Tues, Thurs: 9am-10pm\nSat, Sun: 9am-8pm | PH: 9am-5pm\n"
    update.message.reply_text(f"{reply_text}"
                              "-----------------------------------------------------------\n\n"
                              f"{result}"
                              "Click your *desired date* to proceed to book or /quit to restart",
                              parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardMarkup(date_btns, one_time_keyboard=True, input_field_placeholder='Book for one of the dates'))
    return BOOK


def skip_date(update: Update, context: CallbackContext) -> int:
    """Convenience function for DATE: today, 0 days"""
    user = update.message.from_user
    logger.info(f"User {user.first_name} wants to check for today, and only today")
    update.message.reply_text("Today and only today it is then, simple, I like you!\n"
                              "Click the button to continue",
                              reply_markup=ReplyKeyboardMarkup([[f"{datetime.datetime.now().strftime('%d %m %Y')} 0"]],
                                                               one_time_keyboard=True, input_field_placeholder='Click the button to continue'))

    return DATE


def book(update: Update, context: CallbackContext) -> int:
    """Asks user to log in themselves then gives link to book the slot"""
    # Problem: not sure how to implement logging user in (1. is unsafe, 2. is user-reliant and slow)
    # 1. Get user to enter their ActiveSG account credentials directly into TG (but its wholly unsafe and insecure, which begs the question
    #    of how/if I can log user on and book it. Definitely not selenium on their device (IOS/Android). Shouldn't be mine..., right?
    # 2. Simply ask them to log themselves in first, send them the link, then they'll do the rest from there onwards
    # I chose 2.
    user = update.message.from_user
    msg = update.message.text
    logger.info(f"User {user.first_name} wants to book on {msg}. Giving instructions...")

    generator = Generator(activity=CHOSEN_ACTIVITY, date=msg)
    chosen_venue_id = generator.gen_all_avail_venue_ids().get(CHOSEN_VENUE)
    chosen_activity_id, time_from = generator.activity_id, generator.time_from
    update.message.reply_text("Almost there! Follow the steps below please!\n"
                              "1. [Log into your ActiveSG account](https://members.myactivesg.com/auth)\n"
                              "2. Exit the website, and come back here for 3.\n"
                              f"3. [Redirect to booking site](https://members.myactivesg.com/facilities/view/activity/{chosen_activity_id}/venue/{chosen_venue_id}?time_from={time_from})",
                              parse_mode=ParseMode.MARKDOWN,
                              disable_web_page_preview=True,
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def quit(update: Update, context: CallbackContext) -> int:
    """Quits /check and ends the conversation."""
    user = update.message.from_user
    logger.info(f"User {user.first_name} quit /check")
    update.message.reply_text('Hope I was useful to you C: Stay fit!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def for_fun(update: Update, context: CallbackContext) -> Message:
    """Just a for_fun function for normal chatbot tings"""
    user = update.message.from_user
    msg = update.message.text
    msg_split = msg.lower().split(" ")
    logger.info(f"User {user.first_name} typed: {msg}")
    photos = ["https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F47%2F2020%2F08%2F06%2Frottweiler-headshot-678833089-2000.jpg",
              "https://www.wallpapermaiden.com/image/2021/02/03/australian-shepherd-cute-snow-tree-stare-standing-animals-43406.jpeg",
              "https://assets.orvis.com/is/image/orvisprd/AdobeStock_101064662?wid=1980&src=is($object$:7-3)",
              "https://www.boredpanda.com/blog/wp-content/uploads/2020/03/B3wvE9IhB7K-png__605.jpg",
              open("Z_OG_robat.png", "rb")]
    captions = ["Meet Sir Wally, Rott", "Lovely Luna", "I know this looks like a mix of the other 2 breeds, but NO! >:| I refuse to believe that", "What is this massive floof??", "Ze OG rottie <3"]
    if msg.lower() in ["hi", "hello"]: return update.message.reply_text(f"Simi {update.message.text}?? Go workout la")
    elif "photo" in msg_split:
        random_photo = random.choice(photos)
        return update.message.reply_photo(photo=random_photo, caption=captions[photos.index(random_photo)])
    elif "audio" in msg_split:
        return update.message.reply_audio(open(r"great_song.mp3", "rb"), duration=60, performer="Howard L33", title="Crush on UwU", caption="A great song!")
    update.message.reply_text(''.join([j.upper() if i % random.randint(2, 5) == 0 else j for (i, j) in enumerate(update.message.text)]))
    return update.message.reply_text("kk dun anyhow la, follow the instructions, or go see /help first")


def error(update: Update, context: CallbackContext) -> Message:
    """Error messages during bot usage"""
    user = update.message.from_user
    logger.info(f"ALERT! {user.first_name} caused error: {context.error}")
    return update.message.reply_text("You caused error:\n"
                                     f"{context.error}\n\n"
                                     f"YOU KILLED THE BOT!! Kidding, screenshot and send to my hooman please C:")


def main() -> None:
    """Starts up TG Bot"""
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start)) # /start to run start()
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(ConversationHandler(
                    entry_points=[CommandHandler('check', check)],
                    states={
                        # Essentially a condition (during this func, what can be accepted to proceed to next step? (Messages filtering what? Commands: /what?))
                        # Can put .text(""/["", "", ...]) to match exactly, or .regex("REGEX_PATTERN") to match a pattern
                        ACTIVITY: [MessageHandler(Filters.text(ALL_ACTIVITIES), activity)],
                        VENUE: [MessageHandler(Filters.text & ~Filters.command, venue)],
                        # If no regex/text("") specifying exact input, need to use method in VERIFY to ensure correct input to proceed,
                        VERIFY: [MessageHandler(Filters.text & ~Filters.command, verify_venue), CommandHandler('disappointed', no_venue_found)],
                                              # Only accepts __ __ ____ __
                        DATE: [MessageHandler(Filters.regex(r"[0-9]{1,2}\s{1}[0-9]{1,2}\s{1}[0-9]{4}\s{1}[0-9]{1,2}") & ~Filters.command, date), CommandHandler('skip', skip_date)],
                                              # Only accepts __ __ ____
                        BOOK: [MessageHandler(Filters.regex(r"[0-9]{1,2}\s{1}[0-9]{1,2}\s{1}[0-9]{4}") & ~Filters.command, book)],
                    },
                    # If just Filters.text, any command with / will still register as normal text (wont allow to quit bot, etc)
                    # Filters.text & ~Filters.command means accept all text but not /commands (cmds will be processed normally)
                    # fallbacks: if ~Filters.command, bot will always listen out for this command to end the conversation
                    fallbacks=[CommandHandler("help", help), CommandHandler('quit', quit)],
                ))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, for_fun)) # normal msgs
    dp.add_error_handler(error) # Handle TGBot errors

    updater.start_polling() # Connects to TG, waits for msg after _s
    updater.idle() # Keeps bot running until interrupted


if __name__ == '__main__': main()
