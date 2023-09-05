from datetime import datetime
import csv

""" String to datetime object
Zeitpunkt1 = "15.07.2023 18:37:45"
time = datetime.strptime(Zeitpunkt1, "%d. %B %Y %H:%M:%S")
print(time)"""

# Currenttime with format: Hours:Minutes:Seconds Day.Month.Year
header = ['Modus', 'Zeit']
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

        with open('data.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerow(data)

        break
    elif mode.lower() == 'a':
        now_out = datetime.now()
        f_time_Out = now_out.strftime("%H:%M:%S %d.%m.%Y")
        data = {
            "Modus": 'a',
            "Zeit": f_time_Out
            }

        # Needs READING first so its not overwriting the old Data! 
        # INSERT HERE!

        with open('data.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerow(data)

        # Calculate difference here (PLACEHOLDER CODE!!) - have to read csv first and get "e" Data
        # time1 = datetime.strptime(timeIn, "%H:%M:%S %d.%m.%Y")
        # time2 = datetime.strptime(timeOut, "%H:%M:%S %d.%m.%Y")
        # timeDif = (time2 - time1)
        # print(f'Ausgestempelt: {timeOut} \nSie waren für {timeDif} eingestempelt!')

        break
    else:
        print('Falsche eingabe. gebe e oder a ein!!')
