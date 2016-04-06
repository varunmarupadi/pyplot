#!/usr/bin/env python

import csv
import sys
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import datetime
import dateutil.parser

dateOrd = []
weight = []
with open(sys.argv[1], 'r') as file:
  reader = csv.reader(file);
  for row in reader:
    try:
      curDate = dateutil.parser.parse(row[0]).toordinal()
    except ValueError:
      continue
    if (curDate < datetime.date(2015, 10, 1).toordinal()):
      continue
    dateOrd.append(curDate)
    weight.append(float(row[1]))

f = interp1d(dateOrd, weight)
f2 = interp1d(dateOrd, weight, kind='cubic')

moving_avg = [weight[0]]
exp = 0.9
date = [datetime.date.fromordinal(dateOrd[0])]
diffs = []
print "Date\t\tWeight\tMovingAvg\tDiff"
for i in range(1, dateOrd[-1]-dateOrd[0] + 1):
  moving_avg.append(moving_avg[i-1]*exp + f(dateOrd[0] + i)*(1-exp))
  date.append(datetime.date.fromordinal(dateOrd[0] + i))
  diffs.append(f(dateOrd[0] + i) - moving_avg[-1])
  print "%s\t%.2f\t%.2f\t\t%.2f" % (datetime.date.fromordinal(dateOrd[0]+i).strftime("%Y-%m-%d"),  f(dateOrd[0] + i), moving_avg[-1],  diffs[-1])

print "Average diff: %.2f" % (sum(diffs)/len(diffs))

plt.subplots(1)[0].autofmt_xdate()
plt.axis((datetime.date.fromordinal(dateOrd[0] - 3), datetime.date.fromordinal(dateOrd[-1] + 3), 170, 205));

plt.plot(map(datetime.date.fromordinal,dateOrd), weight,'o', date, moving_avg,'r--', date,f(map(datetime.date.toordinal,date)), '-')
plt.legend(['weight', 'moving average'], loc='best')
plt.show()
