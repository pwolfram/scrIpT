#!/usr/bin/env python

import os
import datetime
import pickle
import subprocess
import numpy as np

def folder_exists(folder, create=True, verbose=True):
    if not os.path.exists(folder):
        if create:
            print 'Creating folder at ', folder
            os.makedirs(folder)
        return False
    else:
        return True

def load_stored_sets(setlocation):
    if os.path.isfile(setlocation):
        with open(setlocation, 'r') as af:
            setvalues = pickle.load(af)
    else:
        setvalues = set()
    return setvalues

def save_stored_sets(aset, setlocation):
    print 'saving %s at %s'%(aset, setlocation)
    with open(setlocation, 'w') as af:
        pickle.dump(aset, af)

def sanitize_response(response):
    # separate comma separated items
    values = response.split(',')
    # remove spaces in front or back of string
    values = [av.rstrip() for av in values]
    values = [av.lstrip() for av in values]
    return values

def make_log_entry(logfile, timestamp, projname, taskname, entry):
    with open(logfile, 'a') as lf:
        if entry == 'START' or entry == 'END':
            log = entry + '\n'
        else:
            log =  'PROJ={' + projname + '}, TASK={' + taskname + '}, LOG={' + entry + '}\n'
        line = timestamp + '\t '+ log
        lf.write(line)
        print 'wrote:\n   %s to\n%s'%(line, logfile)

def undo_log_entry(logfile, timestamp):
    # remove last line
    with open(logfile, 'r+') as lf:
        lines = lf.readlines()
        lastline = lines[-1]
        lf.seek(0)
        for li in lines[:-1]:
            lf.write(li)
        lf.truncate()

    undofile = logfile + '.undo'
    with open(undofile, 'a') as lf:
        undoline = 'Undo at %s:'%(timestamp) + lastline
        lf.write(undoline)
        print 'wrote:\n   %s to\n%s'%(undoline, undofile)

def file_locations(database):
    now = datetime.datetime.now()
    yearfolder = database + '/' + "%.4d"%(now.year)
    monthfolder = yearfolder + '/' + "%.2d"%(now.month)
    dayfolder = monthfolder + '/' + "%.2d"%(now.day)
    logfile = dayfolder + '/' + 'daily.log'
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # make sure file locations are available
    for afold in [database, yearfolder, monthfolder, dayfolder]:
        folder_exists(afold)

    return logfile, timestamp

def print_items(prompt, items, nitems=3):
    # break items up into sets of 5
    print "================================================================================"
    print prompt
    print "--------------------------------------------------------------------------------"
    thelist = list(items)
    n = len(thelist)
    for i in np.arange(int(np.ceil(n/float(nitems)))):
        print thelist[nitems*i:(nitems*i+nitems)]
    print "================================================================================"

def log_work(database, start, end, continued, undo):

    logfile, timestamp = file_locations(database)

    projectfile = database + '/projects.p'
    projects = load_stored_sets(projectfile)

    taskfile = database + '/tasks.p'
    tasks = load_stored_sets(taskfile)

    if undo:
        undo_log_entry(logfile, timestamp)
    elif start:
        make_log_entry(logfile, timestamp, '', '', 'START')
    elif end:
        make_log_entry(logfile, timestamp, '', '', 'END')
    elif continued:
        make_log_entry(logfile, timestamp, '', '', 'CONTINUED')
    else:
        print_items('Projects', sorted(projects))
        response = raw_input("Please enter project names, e.g., 'proj1, proj2, etc':\n")
        projname = sanitize_response(response)
        projects = projects | set(projname)

        print_items('Tasks', sorted(tasks))
        response = raw_input("Please enter task names, e.g., 'analysis, lit_review, misc':\n")
        taskname = sanitize_response(response)
        tasks = tasks | set(taskname)

        entry = raw_input("Please log entry:\n")
        # refresh time stamp to follow once entry is committed
        logfile, timestamp = file_locations(database)
        make_log_entry(logfile, timestamp, ','.join(projname), ','.join(taskname), entry)

        save_stored_sets(projects, projectfile)
        save_stored_sets(tasks, taskfile)


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-d", "--database_location", dest="database", help="Location for work database", metavar="FOLDER")
    parser.add_option("-s", "--start", dest="start", help="Starting entry", action='store_true')
    parser.add_option("-e", "--end", dest="end", help="Ending entry", action='store_true')
    parser.add_option("-c", "--continued", dest="continued", help="Continued entry", action='store_true')
    parser.add_option("-u", "--undo", dest="undo", help="Undo last entry", action='store_true')
    parser.add_option("-p", "--print", dest="printlog", help="Print daily work log", action='store_true')
    parser.add_option("-r", "--edit", dest="editlog", help="Edit daily work log", action='store_true')
    parser.set_defaults(start=False, end=False, undo=False, printlog=False)


    options, args = parser.parse_args()
    if not options.database:
        options.database = os.path.expanduser('~') + '/Documents/WorkLogDatabase'

    print "Using database at " + options.database

    if options.printlog:
        logfile, timestamp = file_locations(options.database)
        print "================================================================================"
        print 'Current time is %s'%(timestamp)
        print 'Outputing daily log %s:'%(logfile)
        print "--------------------------------------------------------------------------------"
        with open(logfile,'r') as lf:
            print lf.read()
            lf.close()
        print "--------------------------------------------------------------------------------"
        print logfile
    elif options.editlog:
        logfile, timestamp = file_locations(options.database)
        edit_call = [ "mvim", logfile]
        edit = subprocess.Popen(edit_call)
    else:
        log_work(options.database, options.start, options.end, options.continued, options.undo)
