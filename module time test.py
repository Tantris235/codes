import datetime
teraz = datetime.datetime.now()
rok = teraz.year
dzien = teraz.day
sekundy = teraz.second
minuty = teraz.minute
miesiąc = teraz.month
czas = rok, miesiąc, dzien, minuty, sekundy
print ("Teraz jest rok : ", rok, "\nTeraz jest miesiąc : ", miesiąc, "\nTeraz jest dzien : ", dzien, "\nTeraz jest minuta : ", minuty, "\nTeraz jest sekunda : ", sekundy, "\nA Razem : ", czas)