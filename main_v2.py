from datetime import datetime
import csv

""" String to datetime object
Zeitpunkt1 = "15.07.2023 18:37:45"
time = datetime.strptime(Zeitpunkt1, "%d. %B %Y %H:%M:%S")
print(time)"""

header = ['Modus', 'Zeit']

# Auslesen der Datei
try:
    with open('data_v2.csv', mode='r') as file:
        reader = csv.DictReader(file)
except FileNotFoundError:
    with open('data_v2.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

# Currenttime with format: Hours:Minutes:Seconds Day.Month.Year

while True:
    mode = input('Einstempeln (e) oder Ausstempeln (a):')

    if mode.lower() == 'e':
        now_in = datetime.now()
        f_time_In = now_in.strftime("%H:%M:%S %d.%m.%Y")
        print(f"Eingestempelt: {f_time_In}")
        data = {
            "Modus": 'e',
            "Zeit": f_time_In
            }

        with open('data_v2.csv', mode='r') as file:
            reader = csv.DictReader(file)
            last_item = list(reader)[-1]

        if last_item['Modus'] == "a":
            with open('data_v2.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writerow(data)
        else:
            print("Du bist bereits eingestempelt!")
        break

    elif mode.lower() == 'a':
        now_out = datetime.now()
        f_time_Out = now_out.strftime("%H:%M:%S %d.%m.%Y")
        data = {
            "Modus": 'a',
            "Zeit": f_time_Out
            }

        with open('data_v2.csv', mode='r') as file:
            reader = csv.DictReader(file)
            last_item = list(reader)[-1]

        if last_item['Modus'] == "e":
            with open('data_v2.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writerow(data)
        else:
            print("Du musst dich erst einstempeln!")

        # Calculate difference here (PLACEHOLDER CODE!!) - have to read csv first and get "e" Data
        # time1 = datetime.strptime(timeIn, "%H:%M:%S %d.%m.%Y")
        # time2 = datetime.strptime(timeOut, "%H:%M:%S %d.%m.%Y")
        # timeDif = (time2 - time1)
        # print(f'Ausgestempelt: {timeOut} \nSie waren für {timeDif} eingestempelt!')

        break
    else:
        print('Falsche eingabe. gebe e oder a ein!!')
