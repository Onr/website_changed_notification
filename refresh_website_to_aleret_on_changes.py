# refresh website to aleret  on changes
import urllib.request
import time
import random
from tqdm import tqdm
import python_telegram_notification
import argparse

def main(website_address=None, minutes_to_wait_between_checks=None, max_checks=10_000,
         add_random_of_pulse_minus_sec=25, num_of_notifications_to_send_in_case_of_change=5):
    print('Setting up telegram notifications')
    telegram_bot = python_telegram_notification.telegram_notification()
    if website_address is None:
        website_address = input('insert a web site address to checks: ')
    if minutes_to_wait_between_checks is None:
        minutes_to_wait_between_checks = int(input('how many minutes to approximately wait between checks? : '))
    sleep_before_checks_for_seconds = 60 * minutes_to_wait_between_checks

    html = urllib.request.urlopen(website_address).read()

    original = str(html)
    begin_str = f'Checking {website_address} for {max_checks} iterations with about {minutes_to_wait_between_checks} minutes between checks'
    print(begin_str)
    telegram_bot.send_message(bot_message=begin_str)
    for i in range(max_checks):
        add_rand = random.randint(1, 2 * add_random_of_pulse_minus_sec)
        sleep_for = sleep_before_checks_for_seconds - add_random_of_pulse_minus_sec + add_rand
        print(f'Wating for {sleep_for} secondes')
        for _ in tqdm(range(sleep_for)):
            time.sleep(1)
        html = urllib.request.urlopen(website_address).read()
        new = str(html)
        did_web_site_changed = not (new == original)
        if did_web_site_changed:
            send_changed_str = f'web site Changed: \n {website_address}'
            print(send_changed_str)
            for _ in range(num_of_notifications_to_send_in_case_of_change):
                telegram_bot.send_message(bot_message=send_changed_str)
                time.sleep(1)
        else:
            print('web site did NOT Changed')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get notification when a website changes')
    parser.add_argument("--website",  nargs="?", help="website address the check for updates")
    parser.add_argument("--time_between_checks", type=int, nargs='?', default=1,
                        help="approximately minutes between checks")
    args = parser.parse_args()
    main(website_address=args.website, minutes_to_wait_between_checks=args.time_between_checks)