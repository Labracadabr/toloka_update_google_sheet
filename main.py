import schedule
import time
from datetime import datetime

from new_pools import pools
from all_accounts import accounts_update


# корректировка по часовому поясу. например при gmt+3 превратить 22 в '01'
def gmt_shift(hour: int) -> str:
    gmt = int(-(time.timezone if (time.localtime().tm_isdst == 0) else time.altzone) / 60 / 60)  # часовой пояс компа
    hour = str((hour + gmt) % 24).zfill(2)
    return hour


# большой скрипт - запускать неск раз в день
update_hours = [7, 15]  # часы указать в gmt 0
for h in update_hours:
    t = f"{gmt_shift(h)}:05"
    schedule.every().day.at(t).do(accounts_update)

# скрипт поменьше - запускать каждые 24 ч в полночь по gmt 0
t = f"{gmt_shift(23)}:55"
schedule.every().day.at(t).do(pools)

print('Сейчас', datetime.now().strftime("%H:%M:%S"))

# поллинг каждые n секунд
n = 20
while 1:
    # проверить, не настало ли время
    schedule.run_pending()
    time.sleep(n)
