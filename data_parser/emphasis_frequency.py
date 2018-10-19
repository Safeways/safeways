import pandas as pd
import decimal

#naive bayes

def drange(start, end, increment):
    start = decimal.Decimal(start)
    end = decimal.Decimal(end)
    while start < end:
        yield float(start)
        start += decimal.Decimal(increment)

def truncate(num):
    return float("%.4f" % num)

def emphasis_frequency(filename):
    FINENESS = .02

    dataframe = pd.read_csv(filename)
    [lat,long] = [list(dataframe.latitude), list(dataframe.longitude)]
    coordinates = [(lat[i], long[i]) for i in range(len(lat))]

    #map is blocked into sections with changes of FINENESS in latitude or longitude
    # (i.e. (40.255,-88) and (40.255 + FINENESS,-88) are considered to be the same location)

    min_lat = min(lat)
    max_lat = max(lat)

    min_long = min(long)
    max_long = max(long)

    counts = {}

    for i in drange(min_lat, max_lat + FINENESS, FINENESS):
        for j in drange(min_long, max_long + FINENESS, FINENESS):
            counts[(truncate(i),truncate(j))] = 0
            for c in coordinates:
                if truncate(c[0]) - truncate(i) < FINENESS and truncate(c[0]) - truncate(i) >= 0 and \
                    truncate(c[1]) - truncate(j) < FINENESS and truncate(c[1]) - truncate(j) >= 0:
                    counts[truncate(i),truncate(j)] += 1

    print({k:v for k,v in counts.items() if v != 0})

    return counts