import datetime
class randomFunctions:
    def getDate():
        dateTime = datetime.datetime.now()
        date = dateTime.strftime("%x")
        time = dateTime.strftime("%I") + ":" + dateTime.strftime("%M")

        return str(date) + " @ " + str(time)
