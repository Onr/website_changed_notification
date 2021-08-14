# refresh website to aleret  on changes
import urllib.request
import time
import random
from tqdm import tqdm

import python_telegram_notification
print('Setting up telegram notifications')
telegram_bot = python_telegram_notification.telegram_notification()
website_address = input('insert a web site address to chaeck: ')
minutes_to_wait_between_chacks = int(input('how many minutes to approximately wait between checks? : '))
sleep_befor_checks_for_secondes = 60 * minutes_to_wait_between_chacks
max_checks = 10_000 
add_random_of_pulse_minus_sec = 25
num_of_notifiction_to_send_in_case_of_chenge = 5

html = urllib.request.urlopen(website_address).read()

original = str(html)
begin_str = f'Checking {website_address} for {max_checks} iterations with about {minutes_to_wait_between_chacks} minutes between checkes'
print(begin_str)
telegram_bot.send_message(bot_message=begin_str)
for i in range(max_checks):
    add_rand = random.randint(1 , 2 * add_random_of_pulse_minus_sec)
    sleep_for = sleep_befor_checks_for_secondes - add_random_of_pulse_minus_sec + add_rand
    print(f'Wating for {sleep_for} secondes')
    for _ in tqdm(range(sleep_for)):
        time.sleep(1)
    html = urllib.request.urlopen(website_address).read()
    new = str(html)
    did_web_site_changed = not(new == original)
    if did_web_site_changed:
        send_changed_str = f'web site Changed: \n {website_address}'
        print(send_changed_str)
        for _ in range(num_of_notifiction_to_send_in_case_of_chenge):
            telegram_bot.send_message(bot_message=send_changed_str)
            time.sleep(1)
    else:
        print('web site did NOT Changed')