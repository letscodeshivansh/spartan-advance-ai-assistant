import datetime
import os
import time
import threading

def set_alarm(alarm_time, sound_file):
    alarm_hour, alarm_minute = map(int, alarm_time.split(":"))

    print("Alarm is set for {}:{} ".format(alarm_hour, alarm_minute))

    while True:
        now = datetime.datetime.now()
        if (now.hour == alarm_hour and
            now.minute == alarm_minute):
            print("Wake Up!")
            os.system("start " + sound_file)
            break
        time.sleep(1)


    

