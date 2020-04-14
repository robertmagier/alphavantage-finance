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
    tickDate = row["time"].split(" ")
    hour = tickDate[3].split(".")[0]
    hour = hour.split(":")
    tickDate = tickDate[2].split(".")[1]
    output = "{}\n{}:{}".format(tickDate, hour[0], hour[1])
    return output


def calculateDiff(row):
    diff = row["y_close"] - row["y_open"]
    return diff


def calculateColor(row):
    diff = calculateDiff(row)
    return "green" if diff > 0 else "red"
