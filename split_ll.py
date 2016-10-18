#!/usr/bin/python
# 
# Read a llvm backend output due to option -print-after-all and split
# the output by pass.

import sets, re, sys, string

## read file to a list
def read_file(fn):
    with open(fn, 'rb') as f:
        content = f.readlines()
        f.close()
        return content

## write a list of string to a file
def write_file(content, fn):
    with open(fn, 'wb') as newf:
        for line in content:
            newf.write(line)
        newf.close()
        
# find ranges starting with label
# the range includes the lable
def find_ranges(content, label):
    i = 0
    start = -1
    ranges = []
    for line in content:
        line = line.rstrip()
        if line.find(label)!=-1:
            if start != -1:
                end = i
                #print start, end
                ranges.append([start, end])
            start = i
        i = i + 1
    return ranges

## checks if any line of a list contains any of patterns
## in a list.
def contains(content, patterns):
    for line in content:
        for pattern in patterns:
            if re.search(pattern, line):
                return True
    return False


def delete_ranges(content, ranges):
    for [start, end] in reversed(ranges):
        content[start:end+1] = []

## Extract pass description from content.
def getPassDesc(contents):
    for line in contents:
        result = re.search(r'\*\*\* IR Dump After (.*) \*\*\*', line)
        if result:
            return result.group(1)
    return ''

## Regularize file name.
## Remove white space and / chars.
def regularize(name):
    name = re.sub(r'\s+', '', name)
    name = re.sub(r'/', '', name)
    return name

## Dump ranges of content to different files if the
## range of content contains the pattern.
def dump_ranges(content, ranges, pattern, file_name):
    i = 1
    for [start, end] in ranges:
        sub_content = content[start:end]
        if contains(sub_content, pattern):
            pass_desc = getPassDesc(sub_content)
            #print 'Pass: ' + pass_desc
            pass_desc = regularize(pass_desc)
            new_name = '{0}.{1:03d}.{2}.ll'.format(file_name, i, pass_desc)
            print 'save ' + new_name
	    write_file(sub_content, new_name)
            i = i + 1
        
############################################################################
## main program
##
## read debug output from -print-after-all and split them into ll files.
##

if len(sys.argv) != 3:
    print 'split_ll.py: Split llvm backend -print-after-all output by function'
    print 'Usage: split_ll.py file functioin'
    sys.exit()

content = read_file(sys.argv[1])
function = sys.argv[2]

print 'Split -print-after-all output for function ' + function

ranges = find_ranges(content, 'IR Dump After')
patterns = [r'define .*@' + re.escape(function) + r'\(',
           r'# Machine code for function ' + re.escape(function) + r':']

dump_ranges(content, ranges, patterns, sys.argv[1])

