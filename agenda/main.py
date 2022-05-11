#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Jaemok Jeong(jmjeong@gmail.com)
#
# [2013/03/20]

import subprocess
import re
import sys
import alfred

# regular expression
entrySpliterRe = re.compile("^\*|^!\s+",re.M)
lineSpliterRe = re.compile("\n\s+", re.M)

# command line
iCalBuddyProg = "./iCalBuddy -tf '%H:%M' -b '*' "

parameter = alfred.args() # proper decoding and unescaping of command line arguments

param = parameter[0] if len(parameter) >= 1 else 0
progList = []    

try:
    param = int(param)
    progList.extend(
        (
            [iCalBuddyProg + "eventsToday+%d" % param, 'ical.png'],
            [
                iCalBuddyProg + "tasksDueBefore:today+%d" % (param + 1),
                'reminder.png',
            ],
        )
    )

except ValueError:
    progList.append([f"{iCalBuddyProg}undatedUncompletedTasks", 'reminder.png'])

results = []
count = 0
for prog in progList:
    iCalBuddyOutput = subprocess.check_output(prog[0], shell=True)
    entries = entrySpliterRe.split(iCalBuddyOutput)[1:]

    for entry in entries:
        e = lineSpliterRe.split(entry)

        results.append(alfred.Item(attributes={},
                        title = alfred.decode(e[0]),
                        subtitle = alfred.decode(','.join(e[1:])),
                        icon = prog[1]))
        count += 1

alfred.write(alfred.xml(results))
