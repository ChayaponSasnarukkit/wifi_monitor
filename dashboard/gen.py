
import csv
import random
import time
from datetime import datetime

x_value = 0
total_1 = 1000
total_2 = 1000

fieldnames = ["Time", "Tx_power", "Signal", "Noise", "Bit_Rate"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

Tx_power = 30
Signal = -15
Nosie = -90
Bit_Rate = 866.7
x = 0

while x < 1000:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "Time": datetime.now().strftime('%H:%M:%S'),
            "Tx_power": Tx_power+random.randint(-2, 2),
            "Signal": Signal+random.randint(-2, 2),
            "Noise" : Nosie+random.randint(-2, 2),
            "Bit_Rate" : f"{Bit_Rate+random.randint(-9, 9)/10:.1f}"
        }

        csv_writer.writerow(info)
        x += 1

    time.sleep(1)