
import datetime
import loguru

def GetDateString():
    now = datetime.datetime.now()
    dateStr = now.strftime("%Y-%m-%d %H:%M:%S")
    loguru.logger.debug(dateStr)
    return dateStr
