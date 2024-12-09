import datetime as dt
import requests
import time

station = 'kunv'

def main():
    day = dt.date(2021, 3, 1)
    dayend = dt.date(2024, 8, 17)
    while True:
        times = range(0, 24, 6)
        for z in times:
            t0 = 0
            # request bufkit data
            response = requests.get(f'https://mtarchive.geol.iastate.edu/{day.year}/{day.month:02}/{day.day:02}/bufkit/{z:02}/gfs/gfs3_{station}.buf')

            # save to folder
            with open(f'data/gfs/{station}-{day.year}-{day.month:02}-{day.day:02}-{z:02}.buf', mode='wb') as file:
                file.write(response.content)
            print(f'SAVED {station}-{day.year}-{day.month}-{day.day}-{z}') 
            time.sleep(0.3)
        day = day + dt.timedelta(days = 1)
        if day == dayend:
            print('RUN FINISHED')
            break

if __name__ == '__main__':
    pass
