from datetime import datetime
import csv

""" String to datetime object
Zeitpunkt1 = "15.07.2023 18:37:45"
time = datetime.strptime(Zeitpunkt1, "%d. %B %Y %H:%M:%S")
print(time)"""

# Currenttime with format: Hours:Minutes:Seconds Day.Month.Year

while True:
    einstempeln = input('Einstempeln?')

    if einstempeln.lower() == 'yes' or einstempeln.lower() == 'ja':
        now1 = datetime.now()
        timeIn = now1.strftime("%H:%M:%S %d.%m.%Y")
        print(f"Eingestempelt: {timeIn}")
        break
    else:
        print('Nicht eingestempelt! Gebe Ja oder Yes um sich einzustempeln.')

# Solange die Schleife läuft, ist man anwesend. Möchte man sich ausstempeln, 
# bricht man die While Schleife mit einer Eingabe ab
while True:
    ausstempeln = input('Beliebige Eingabe zum ausstempeln: ')

    if ausstempeln.lower() != '':
        now2 = datetime.now()
        timeOut = now2.strftime("%H:%M:%S %d.%m.%Y")
        break

# TimeIn und TimeOut zur einem Datetime Objekt zurückwandeln um anschließend 
# die Differenz zu ermitteln
time1 = datetime.strptime(timeIn, "%H:%M:%S %d.%m.%Y")
time2 = datetime.strptime(timeOut, "%H:%M:%S %d.%m.%Y")
timeDif = (time2 - time1)
print(f'Ausgestempelt: {timeOut} \nSie waren für {timeDif} eingestempelt!')

with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    header = ['Eingestempelt', 'Ausgestempelt', 'Anwesenheit']
    writer.writerow(header)
    data = [timeIn, timeOut, timeDif]
    writer.writerow(data)