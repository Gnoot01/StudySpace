"""
https://www.miniclip.com/games/sushi-go-round/en/#
Order of Ingredients:
1:Shrimp | 2:Rice
3:Nori   | 4:Roe
5:Salmon | 6:Unagi
Can simply run the script and will complete all 7 days (continues/retries automatically), taking ~45 mins for the entire game
If stopped in mid-game, can just rerun as long as on mid_game_screen screen (meaning not others like try_again screen, etc),
because variables like player_side_belt and table are needed, as they are used as region and to click respectively.
Depending on mid-game progress, might need to adjust locating ingredient's confidence then run again.
grayscale sometimes make imgs look too similar to each other, esp if few colors, hard to differentiate
sake & waste are only additional, since wont matter if fast service/no mistakes
"""
import pyautogui as pg
import keyboard
import time


def ready():
    to_check = [mid_game_screen, player_side_belt, table, phone, shrimp, rice, nori, roe, salmon, unagi]
    for any in to_check:
        if any is None:
            print(f"{to_check.index(any)+1}th in to_check is None! Fix first!")
            return False
    return True


def check_day_end():
    # if day_success, continue x2/3. Else, continue, continue in diff spot, yes (to try agn), continue
    continue_btn = pg.locateCenterOnScreen("continue_btn.png", region=mid_game_screen, confidence=0.8, grayscale=True)
    if continue_btn is not None:
        click(continue_btn)
        time.sleep(0.5)
        click(pg.locateCenterOnScreen("continue_btn.png", region=mid_game_screen, confidence=0.8, grayscale=True))
        try_agn_btn = pg.locateCenterOnScreen("try_agn_btn.png", region=mid_game_screen, confidence=0.7, grayscale=True)
        if try_agn_btn is not None:
            click(try_agn_btn)
            time.sleep(0.5)
        click(continue_btn)


def click(sth):
    pg.click(sth, tween=pg.easeOutQuad)


def give_sake(sake, angry_customer):
    pg.mouseDown(sake, button="left")
    pg.moveTo(angry_customer, duration=0.2, tween=pg.easeOutQuad)
    pg.mouseUp()


def serve():
    click(table)
    time.sleep(0.5)
    check_quantity()
    check_plate(plates)
    check_waste(waste)


def make_californiaroll():
    # 1 rice + 1 nori + 1 roe
    click(rice)
    click(nori)
    click(roe)
    serve()


def make_gunranmaki():
    # 1 rice + 1 nori + 2 roe
    click(rice)
    click(nori)
    for _ in range(2): click(roe)
    serve()


def make_onigiri():
    # 2 rice + 1 nori
    for _ in range(2): click(rice)
    click(nori)
    serve()


def make_salmonroll():
    # 1 rice + 1 nori + 2 salmon
    click(rice)
    click(nori)
    for _ in range(2): click(salmon)
    serve()


def make_shrimpsushi():
    # 1 rice + 1 nori + 2 shrimp
    click(rice)
    click(nori)
    for _ in range(2): click(shrimp)
    serve()


def make_unagiroll():
    # 1 rice + 1 nori + 2 unagi
    click(rice)
    click(nori)
    for _ in range(2): click(unagi)
    serve()


def make_dragonroll():
    # 2 rice + 1 nori + 1 roe + 2 unagi
    for _ in range(2): click(rice)
    click(nori)
    click(roe)
    for _ in range(2): click(unagi)
    serve()


def make_combosushi():
    # 2 rice + 1 nori + 1 roe + 1 salmon + 1 unagi + 1 shrimp
    for _ in range(2): click(rice)
    click(nori)
    click(roe)
    click(salmon)
    click(unagi)
    click(shrimp)
    serve()


def order(i: int):
    click(phone)
    time.sleep(0.1)
    # Need to i+1 to maintain order of ingredients while using list indexing
    if i+1 == 2:  # rice needs to be ordered separately
        click(pg.locateCenterOnScreen(f"misc/order_menu/order_rice.png", region=mid_game_screen, confidence=0.9))
        time.sleep(0.1)
        rice_order = pg.locateCenterOnScreen(f"misc/order_menu/order{i+1}.png", region=mid_game_screen)
        time.sleep(0.1)
        if rice_order is not None:
            click(rice_order)
            time.sleep(0.1)
            click(pg.locateCenterOnScreen(f"misc/normal_delivery.png", region=mid_game_screen, confidence=0.9))
            time.sleep(3)
        else: click(pg.locateCenterOnScreen(cancel_phone, region=mid_game_screen, confidence=0.8))
    elif i == 6:
        click(pg.locateCenterOnScreen("misc/order_menu/order_sake1.png", region=mid_game_screen, confidence=0.9))
        time.sleep(0.1)
        sake_order = pg.locateCenterOnScreen("misc/order_menu/order_sake2.png", region=mid_game_screen)
        time.sleep(0.1)
        if sake_order is not None:
            click(sake_order)
            time.sleep(0.1)
            click(pg.locateCenterOnScreen(f"misc/normal_delivery.png", region=mid_game_screen, confidence=0.9))
        else: click(pg.locateCenterOnScreen(cancel_phone, region=mid_game_screen, confidence=0.8))
    else:
        click(pg.locateCenterOnScreen("misc/order_menu/order_topping.png", region=mid_game_screen, confidence=0.9))
        time.sleep(0.1)
        ingredient_order = pg.locateCenterOnScreen(f"misc/order_menu/order{i+1}.png", region=mid_game_screen)
        time.sleep(0.1)
        if ingredient_order is not None:
            click(ingredient_order)
            time.sleep(0.1)
            click(pg.locateCenterOnScreen(f"misc/normal_delivery.png", region=mid_game_screen, confidence=0.9))
            time.sleep(3)
        else: click(pg.locateCenterOnScreen(cancel_phone, region=mid_game_screen, confidence=0.8))


def check_quantity():
    # Checking if low_quantity & need to phone
    for i in range(len(low_ingredients)):
        if pg.locateOnScreen(low_ingredients[i], region=mid_game_screen) is not None:
            order(i)
            break
    # second layer catch
    for i in range(len(lower_ingredients)):
        if pg.locateOnScreen(lower_ingredients[i], region=mid_game_screen) is not None:
            order(i)
            break
    # last catch in case value drops to 0 and never gets replenished
    for i in range(len(lowest_ingredients)):
        if pg.locateOnScreen(lowest_ingredients[i], region=mid_game_screen) is not None:
            order(i)
            break


def check_sake(empty_sake_area):
    if pg.locateOnScreen(empty_sake_area, region=mid_game_screen) is not None:
        order(6)


def check_angry(angry_bars, sake, empty_sake_area):
    # Check if angry customers & need to give sake & phone
    for angry_bar in angry_bars:
        angry_customer = pg.locateCenterOnScreen(angry_bar, region=mid_game_screen, confidence=0.95)
        if angry_customer is not None:
            sake = pg.locateCenterOnScreen(sake, region=mid_game_screen, confidence=0.6)
            if sake is not None:
                give_sake(sake, angry_customer)
            check_sake(empty_sake_area)
            break


def check_plate(plates):
    # Check if have plates & need to clear
    for plate in plates:
        plate_to_clear = pg.locateCenterOnScreen(plate, region=mid_game_screen, confidence=0.8)
        if plate_to_clear is not None: click(plate_to_clear)


def check_waste(waste):
    # Check if have waste & need to clear
    # Problem: Can only click & clear waste if waste comes to player's side. Else, once 1 waste gets past, since pg
    #          views img right then down, will never be able to click & clear waste, since keeps clicking waste
    #          on customer's side
    # Solution: use region to restrict to clicking when on player's side only
    waste = pg.locateCenterOnScreen(waste, region=player_side_belt, confidence=0.8, grayscale=True)
    if waste is not None: click(waste)


pg.PAUSE = 0.01
start_game_screen = pg.locateOnScreen("start_game_screen.png", confidence=0.9, grayscale=True)
click(pg.locateCenterOnScreen("play_btn.png", region=start_game_screen, confidence=0.9, grayscale=True))
time.sleep(0.2)
continue_btn = pg.locateCenterOnScreen("continue_btn.png", region=start_game_screen, confidence=0.8, grayscale=True)
click(continue_btn)
time.sleep(0.2)
click(pg.locateCenterOnScreen("skip_btn.png", region=start_game_screen, confidence=0.9, grayscale=True))
time.sleep(0.2)
click(continue_btn)
time.sleep(0.2)
mid_game_screen = pg.locateOnScreen("mid_game_screen.png", region=start_game_screen, confidence=0.7, grayscale=True)
player_side_belt = pg.locateOnScreen("player_side_belt.png", region=mid_game_screen, confidence=0.5, grayscale=True)

table = pg.locateCenterOnScreen("misc/serve.png", region=mid_game_screen, confidence=0.8, grayscale=True)
phone = pg.locateCenterOnScreen("misc/phone.png", region=mid_game_screen, confidence=0.9, grayscale=True)
shrimp = pg.locateCenterOnScreen("ingredients/1.png", region=mid_game_screen, confidence=0.8)
rice = pg.locateCenterOnScreen("ingredients/2.png", region=mid_game_screen, confidence=0.7)
nori = pg.locateCenterOnScreen("ingredients/3.png", region=mid_game_screen, confidence=0.8)
roe = pg.locateCenterOnScreen("ingredients/4.png", region=mid_game_screen, confidence=0.85)
salmon = pg.locateCenterOnScreen("ingredients/5.png", region=mid_game_screen, confidence=0.8)
unagi = pg.locateCenterOnScreen("ingredients/6.png", region=mid_game_screen, confidence=0.8)

food = ["food/CaliforniaRoll.png", "food/GunranMaki.png", "food/Onigiri.png", "food/SalmonRoll.png",
        "food/ShrimpSushi.png", "food/UnagiRoll.png", "food/DragonRoll.png", "food/ComboSushi.png"]
days_food = [food[:3], food[:4], food[:5], food[:6], food[:7], food, food]
days = ["days/1.png", "days/2.png", "days/3.png", "days/4.png", "days/5.png", "days/6.png", "days/7.png"]
lowest_ingredients = ["ingredients/0_1.png", "ingredients/0_2.png", "ingredients/0_3.png", "ingredients/0_4.png", "ingredients/0_5.png", "ingredients/0_6.png"]
lower_ingredients = ["ingredients/1_1.png", "ingredients/2_2.png", "ingredients/2_3.png", "ingredients/2_4.png", "ingredients/1_5.png", "ingredients/1_6.png"]
low_ingredients = ["ingredients/2_1.png", "ingredients/4_2.png", "ingredients/4_3.png", "ingredients/4_4.png", "ingredients/2_5.png", "ingredients/2_6.png"]
plates = ["misc/plates/pink_plate.png", "misc/plates/big_blue_plate.png", "misc/plates/small_blue_plate.png", "misc/plates/big_red_plate.png", "misc/plates/small_red_plate.png"]
waste = "misc/waste.png"
angry_bars = ["misc/angry_bar1.png", "misc/angry_bar2.png"]
sake = "misc/sake.png"
empty_sake_area = "misc/empty_sake_area.png"
cancel_phone = "misc/cancel_phone.png"
time.sleep(1)

if ready():
    while not keyboard.is_pressed("f2"):
        check_day_end()
        """
        To give sake when customers angry (1.5 bar & 1 bar)
        Problem: at the start of the game, money is needed more than ever, so using on sakes instead of ingredients will only
                 make less food->more angry customers->more sake->less money and so on
        Possible to implement, say by i++ that counts number of iterations by experimentation / 
        a variable that locates half-day meter (once >= half, shld have enough money, can buy sake?)
        """
        # check_angry(angry_bars, sake, empty_sake_area)
        check_plate(plates)
        check_waste(waste)
        for day in days:
            if pg.locateOnScreen(day, region=mid_game_screen, grayscale=True) is not None:
                """
                Problem: for-loop progresses sequentially using a list. But what if a customer at last spot orders food[0]?
                Bot will keep making food[0] while it travels down all the way to last spot, even if no other spots want food[0]
                Solution: 
                1. Not sure how to implement, but say going from screen left to right..? appends & removes from list as order is done
                   I guess can combine 2. too after all spots are done. Still problematic since doesn't guarantee making necessary orders only
                2. time.sleep() can help, but it's too simple. Essentially delays making food, so food has time to travel before
                   same one is made inevitably until food travels to its spot
                3. Random can help, but won't solve 100%, which is what I'll go with for now, along with 2.
                Edit: Random sometimes isn't very reliable and once more choices are made available, contrary to my initial belief, makes it harder for 
                      specific food to be chosen & made. Not sure how to speed up random calls too, and that is a very limiting factor. Initial
                      implementation simply looped thru the food list, regardless which day it was, and this made things very slow.
                      Hence, decided to go with an in-order for-loop, locating the day and instead using only food recipes present for that day, meaning
                      it doesn't make unnecessary elif calls and checks.
                """
                for fd in days_food[days.index(day)]:
                    if pg.locateOnScreen(fd, region=mid_game_screen, confidence=0.95, grayscale=True) is not None:
                        # Suggestion: giving sake, ordering sake when customers angry(1 bar?)?
                        if fd == food[0]: # is CaliforniaRoll
                            make_californiaroll()
                        elif fd == food[1]: # is GunranMaki
                            make_gunranmaki()
                        elif fd == food[2]: # is Onigiri
                            make_onigiri()
                        elif fd == food[3]: # is SalmonRoll
                            make_salmonroll()
                        elif fd == food[4]: # is ShrimpSushi
                            make_shrimpsushi()
                        elif fd == food[5]: # is UnagiRoll
                            make_unagiroll()
                        elif fd == food[6]: # is DragonRoll
                            make_dragonroll()
                        else: # is ComboSushi
                            make_combosushi()
                break
