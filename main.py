from datetime import datetime, timedelta

""" String to datetime object
Zeitpunkt1 = "15.07.2023 18:37:45"
time = datetime.strptime(Zeitpunkt1, "%d. %B %Y %H:%M:%S")
print(time)"""

# Currenttime with format: Hours:Minutes:Seconds Day.Month.Year

now1 = datetime.now()
einstempeln = input('Einstempeln?')
if einstempeln.lower() == 'yes' or einstempeln.lower() == 'ja':
    timeIn = now1.strftime("%H:%M:%S %d.%m.%Y")
    print("Eingestempelt: ",timeIn)
else:
    print('Nicht eingestempelt! Gebe Ja oder Yes um sich einzustempeln.')
# Solange die Schleife läuft, ist man anwesend. Möchte man sich ausstempeln, bricht man die While Schleife mit einer Eingabe ab.    
while einstempeln.lower() == 'yes' or einstempeln.lower() == 'ja':
    ausstempeln = input('Beliebige Eingabe zum ausstempeln: ')
    if ausstempeln.lower() !='':
        now2 = datetime.now()
        timeOut = now2.strftime("%H:%M:%S %d.%m.%Y")
        # TimeIn und TimeOut zur einem Datetime Objekt zurückwandeln um anschließend die Differenz zu ermitteln
        time1 = datetime.strptime(timeIn, "%H:%M:%S %d.%m.%Y")
        time2 = datetime.strptime(timeOut, "%H:%M:%S %d.%m.%Y")
        timeDif = (time2 - time1)
        print('Ausgestempelt: ',timeOut, '\nSie waren für  ',timeDif , 'eingestempelt!')
        break