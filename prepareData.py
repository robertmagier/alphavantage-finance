def calculateHighBase(row):
    maxValue = max(row["y_open"], row["y_close"])
    return maxValue


def calculateLowBase(row):
    minValue = min(row["y_open"], row["y_close"])
    return minValue


def calculateHighError(row):
    highErr = row["y_high"] - calculateHighBase(row)
    return highErr


def calculateLowError(row):
    lowErr = row["y_low"] - calculateLowBase(row)
    return lowErr

def generateLegend(row):
    tickDate =  row["time"].split(' ')
    hour = tickDate[3].split('.')[0]
    hour = hour.split(':')
    tickDate = tickDate[2].split('.')[1]
    return '{}\n{}:{}'.format(tickDate,hour[0],hour[1])
