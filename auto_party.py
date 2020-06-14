import win32com.client
import win32con
import win32gui
import pyautogui
import ctypes
import datetime
import time
import random
import math
import operator
from functools import reduce
from PIL import Image, ImageGrab, ImageDraw

ctypes.windll.user32.SetProcessDPIAware()
DEBUG_MODE = False
SCREENSHOTS_COUNTS = [0]


def save_screenshots(w_pos, draw_pos: list = None, fname: str = None):
    image = ImageGrab.grab(w_pos)
    if draw_pos is not None:
        draw = ImageDraw.Draw(image)
        pos = [draw_pos[0]-10, draw_pos[1]-10, draw_pos[0]+10, draw_pos[1]+10]
        draw.ellipse(pos, fill=(255, 0, 0))
    if fname is None:
        SCREENSHOTS_COUNTS[0] += 1
        fname = str(SCREENSHOTS_COUNTS[0]) + '.png'
    image.save('screenshots/' + fname)


def random_sleep(t):
    if t is not None:
        if t >= 1 or t == 0:
            t = t + random.random()
        time.sleep(t)
    return 0


def get_window_position(return_handle=False):
    hwnd = win32gui.FindWindow(None, r'夜神模拟器')
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    w_pos = win32gui.GetWindowRect(hwnd)
    print('Window position: {}'.format(w_pos))
    return (w_pos, hwnd) if return_handle else w_pos


def wait_until(run_time, interval=1):
    time_parsed = datetime.time(*(map(int, run_time.split(':'))))
    start_time = datetime.datetime.combine(datetime.date.today(), time_parsed)
    print(start_time)
    print(datetime.datetime.today().time())
    if start_time < datetime.datetime.today():
        start_time = datetime.date.today() + datetime.timedelta(days=1)
        start_time = datetime.datetime.combine(start_time, time_parsed)
    print("Wait until {}".format(start_time))
    while start_time > datetime.datetime.today():
        time.sleep(interval)


def press_key(msg='1'):
    pyautogui.press(msg)
    w_pos = get_window_position()
    save_screenshots(w_pos)


def move_click(w_pos, click_pos, t=.0):  # 移动鼠标并点击左键
    x = w_pos[0]+click_pos[0]
    y = w_pos[1]+click_pos[1]
    save_screenshots(w_pos, click_pos)
    pyautogui.click(x=x, y=y)
    random_sleep(0.1)
    pyautogui.click(x=x, y=y)
    random_sleep(t)
    return 0


def check_status(w_pos, fname, threshold):
    if isinstance(w_pos, str):
        image1 = Image.open('screenshots/' + w_pos)
    else:
        image1 = ImageGrab.grab(w_pos)
    image2 = Image.open('screenshots/' + fname)
    h1 = image1.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(reduce(operator.add,
                           map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
    print("Similarity: {} ".format(rms))
    return rms < threshold


def perform_click(click_pos, status_lists, random_click: list = None, sleep_time=1, max_wait: int = math.inf):
    w_pos = get_window_position()
    move_click(w_pos, click_pos, t=sleep_time)
    w_pos = get_window_position()

    def check_condition(con_lists):
        res = False
        for status_i in con_lists:
            res |= check_status(w_pos, status_i[0], status_i[1]) == status_i[2]
        return res

    start_time = time.time()
    while len(status_lists) and (not check_condition(status_lists)):
        if time.time() - start_time > max_wait:
            print('Waited longer than {} seconds, break.'.format(max_wait))
            break
        w_pos = get_window_position()
        if random_click is not None:
            move_click(w_pos, [x + random.randint(0, 10) - 5 for x in random_click], t=sleep_time)
        else:
            random_sleep(sleep_time)
        print('.', end='')
    print()


def night_party():
    # load nikki from emulator
    print('Load nikki.')
    click_pos = [650, 575]  # Nikki position in emulator
    w_pos = get_window_position()
    move_click(w_pos, click_pos, 1)
    if DEBUG_MODE:
        random_sleep(50)
    else:
        random_sleep(180)

    # Check for update
    click_pos = [710, 1130]
    w_pos = get_window_position()
    random_sleep(0.5)
    if check_status(w_pos, 'nikki_update.png', 1000):
        perform_click(click_pos, [('nikki_login.png', 1500, True), ('nikki_login_no_post.png', 500, True)],
                      max_wait=60)

    # login
    print('Begin login.')
    click_pos = [540, 1720]  # start position
    perform_click(click_pos, [('nikki_home.png', 1000, True)], random_click=[390, 1700])
    # Wait for another simulator.
    click_pos = [390, 1700]  # blank area
    random_sleep(10)
    for i in range(7):
        w_pos = get_window_position()
        move_click(w_pos, click_pos, t=1)

    # Enter union
    print('Enter union.')
    click_pos = [995, 950]  # Union button location
    perform_click(click_pos, [('nikki_union.png', 1000, True)])

    # Enter party
    click_pos = [635, 1365]  # Party button location
    w_pos = get_window_position()
    move_click(w_pos, click_pos, t=1)

    # Wait to 7:10:10
    if not DEBUG_MODE:
        wait_until('07:10:00')
    click_pos = [520, 1265]  # Join party button
    perform_click(click_pos, [('nikki_union_enter_party.png', 3000, False)], random_click=click_pos)
    move_click(w_pos, click_pos)
    move_click(w_pos, click_pos)

    # Enter something
    for i in range(2):
        click_pos = [400, 1905]  # text box
        w_pos = get_window_position()
        move_click(w_pos, click_pos)
        move_click(w_pos, click_pos, .5)
        move_click(w_pos, click_pos, .3)
        [press_key(msg=str(1)) for _ in range(0, random.randint(2, 5))]
        click_pos = [1000, 1880]  # send button
        move_click(w_pos, click_pos)
        move_click(w_pos, click_pos)
        move_click(w_pos, click_pos)

    # Take screenshots in party
    total_time = 300
    time_intervel = 10
    click_pos = [410, 470]
    for t in range(0, total_time, time_intervel):
        w_pos = get_window_position()
        time.sleep(time_intervel)
        click_pos = [x+random.randint(0, 20)-10 for x in click_pos]
        move_click(w_pos, click_pos)


def schedule_task(task, schedule_time='07:00:00'):
    if DEBUG_MODE:  # Delay 5 seconds.
        t = (datetime.datetime.today()+datetime.timedelta(seconds=2)).time()
        # wait_until(t.strftime('%H:%M:%S'), interval=1)
    else:
        wait_until(schedule_time, interval=30)
    task()


if __name__ == '__main__':
    # night_party()
    # save_screenshots(get_window_position(), None, 'test.png')
    # save_screenshots(get_window_position(), None, 'nikki_union.png')
    # save_screenshots(get_window_position(), None, 'nikki_home.png')
    # check_status(get_window_position(), 'nikki_login.png', 1000)
    # print(check_status(get_window_position(), 'nikki_home.png', 1000))
    # print(check_status('38.png', 'nikki_home.png', 1000))
    # print(check_status('nikki_update.png', 'nikki_login_no_post.png', 100))
    # print(check_status('54.png', 'nikki_union_enter_party.png', 100))
    # print(check_status('5_answer_party1.png', '5_answer_party2.png', 100))
    # print(check_status('5_answer_party2.png', '5_answer_party3.png', 100))
    # print(check_status('6_in_party0.png', '6_in_party20.png', 100))
    # print(check_status('6_in_party10.png', '6_in_party20.png', 100))

    # DEBUG_MODE = True
    schedule_task(night_party)
