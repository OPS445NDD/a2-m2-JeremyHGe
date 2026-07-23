#!/usr/bin/env python3

'''
OPS445 Assignment 2 - Winter 2023
Program: assignment2.py 
Author: Jeremy Hernandez
The python code in this file is original work written by
Jeremy Hernandez. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This will be a script that presents information about process memory usage in a user friendly way.

Date: 7/22/2026

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",
                                     epilog="Copyright 2023") # Through description we get text at the top of the help
                                                              # Epilog would be at the bottom of the help message
    parser.add_argument("-H", # Short for of our argument
                        "--human-readable", # Long form of our argument
                        action="store_true", # If -H or --Human-readable is called, will be set as true; then saved in args.human_readable
                        help="Prints sizes in human readable format",
                        )
    parser.add_argument("-l", 
                        "--length", 
                        type=int, # Expects an integer
                        default=20, # Default length if not provided
                        help="Specify the length of the graph. Default is 20.")
    # Create an entry for human-readable. Check the docs to make it a True/False option.
    parser.add_argument("program", 
                        type=str, 
                        nargs='?', # It says how much output to expect, in this case ? referes to 0 or more
                        help="if a program is specified, show memory use of all associated processes. Show only total use if not.")
    args = parser.parse_args() # Gets the data by user
    return args

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    filled = int(percent*length) # How filled it should be
    return "#" * filled + " " * (length-filled) # Creates this filling bar

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    # open the meminfo file to do this!
    meminfo = open('/proc/meminfo','r')
    for line in meminfo: # Checks every line until memtotal
        if line.startswith('MemTotal:'):
            return int(line.split()[1]) # Gets the value
            
    meminfo.close()
    pass

def get_avail_mem() -> int:
    "return total memory that is currently available"
    # open the meminfo file to do this!
    meminfo = open('/proc/meminfo','r')
    for line in meminfo: # Checks every line  until memavailable
        if line.startswith('MemAvailable:'):
            return int(line.split()[1]) # Gets the value after memAvailable
            
    meminfo.close()
    pass

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    # please use os.popen('pidof <app>') to do this!
    output = os.popen(f"pidof {app_name}").read().strip() 
    # Runs pidof with the name of our app, gets the output of the command and removes spaces and newlines from start and end
                      
    if not output:
        return []             # Checks if there was content when the command was ran
    return output.split()       # Converts into separate values in a list
            
    

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the Resident memory used"
    # for a process, open the smaps file and return the total of each
    # Rss line.
    to_rss = 0 
    try:
        smaps = open(f'/proc/{proc_id}/smaps', 'r') # Opens the smaps files in read mode
        for line in smaps: # Goes through every line what starts with Rss: 
            if line.startswith('Rss:'):
                to_rss += int(line.split()[1]) # It will split the output found taking the value number then adding
        smaps.close()
    except FileNotFoundError:
        # Returns 0 if the process terminates before it can be read
        pass
    return to_rss

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:  # not program name is specified.
        pass
    else:
        pass