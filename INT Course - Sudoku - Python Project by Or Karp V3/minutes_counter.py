# from datetime import datetime
import time
# now = datetime.now()


# returns the current hour in seconds
def current_hour_in_seconds():
    # hour = now.hour
    # minute = now.minute
    # return (hour*60) + minute
    return time.time()


# subtracting two times in seconds and returns it in minutes
def subtract_the_times_return_minutes(time1, time2):
    # if time1 > time2:
    #     time2 += 24*60
    # return time2 - time1
    return int((time2 - time1)/60)


if __name__ == '__main__':
    # print(subtract_the_times_return_minutes({"hour": 17, "minute": 13},{"hour": 17, "minute": 15}))
    # x = current_hour_in_minutes()
    # print(x)
    print(5//2)
