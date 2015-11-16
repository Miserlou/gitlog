#! /usr/bin/env python

from dateutil import parser
from datetime import datetime

import argparse
import os
import pprint
from subprocess import Popen, PIPE

name = "Rich Jones"

arg_parser = argparse.ArgumentParser(description='Gitlog. Get days worked from Git history..\n')
arg_parser.add_argument('-r','--repos', nargs='+', help='<Required> List of repos', required=True)

args = arg_parser.parse_args()
vargs = vars(args)

if not any(vargs.values()):
    arg_parser.error('Please list repos to log!')

lines = ''
command = 'git log --format=format:"%ad %C(green)%aN%Creset %s" --author="Rich" --date=local'
command_arguments = ['git', 'log', '--format=format:"%ad %C(green)%aN%Creset %s"', '--author="Rich"', '--date=local']

days = {}
for repo in vargs['repos']:
    try:
        p = Popen('git log --format=format:"%ad %aN %s" --author="Rich" --date=local', cwd=repo, shell=True, stdout=PIPE)
        (log, _) = p.communicate()
        lines = lines + log + "\n"
    except Exception, e:
        continue

for line in lines.split('\n'):
    if name not in line:
        continue
    else:
        date_s, task_s = line.split(name) #[0].strip()
        day_s = ' '.join(date_s.split(':')[0].split(' ')[:-1])
        dt = parser.parse(day_s.strip())
        if days.has_key(dt):
            days[dt].append(task_s.strip())
        else:
            days[dt] = [task_s]

for day in sorted(days.keys()):
    print day.strftime("%A, %B %d, %Y")
    for stamp in days[day]:
        print '\t - ' + stamp
   
