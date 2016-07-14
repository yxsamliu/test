import sets, re
from Tkconstants import LAST

## reference file where you get some info
ref_file = 'C:/p4/stg_win60/git-llvm-tot/llvm/test/CodeGen/AMDGPU/kernel-metadata.s'

## the file you want to modify
target_file = 'C:/p4/stg_win60/git-llvm-tot/llvm/test/CodeGen/AMDGPU/kernel-metadata.ll'

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
        
# find ranges starting with label and end with empty line
# the range does not include the lable and the empty line
def find_ranges_end_with_empty_line(content, label):
    i = 0
    start = -1
    ranges = []
    for line in content:
        line = line.rstrip()
        if line.find(label)!=-1:
            start = i + 1
            #print start
        elif start != -1 and line == '':
            end = i -1
            ranges.append([start, i-1])
            #print start
            start = -1
        i = i + 1
    return ranges

# find ranges starting with label_start and end with label_end
def find_ranges(content, label_start, label_end):
    i = 0
    start = -1
    ranges = []
    for line in content:
        line = line.rstrip()
        if line.find(label_start)!=-1:
            start = i + 1
        elif start != -1 and line.find(label_end)!=-1:
            end = i -1
            #print start,end
            ranges.append([start, i-1])
            start = -1
        i = i + 1
    return ranges

def delete_ranges(content, ranges):
    for [start, end] in reversed(ranges):
        content[start:end+1] = []

def dump_ranges(content, ranges):
    for [start, end] in ranges:
        for i in range(start, end+1):
            print content[i]

def dump_list(content):
    for line in content:
        print line
        
## replace the ranges1 in content1 with ranges2 in content2
def replace_ranges(content1, ranges1, content2, ranges2):
    len1 = len(ranges1)
    len2 = len(ranges2)
    if len1 != len2:
        print 'number of ranges different',len1,len2
        return
    i = len1 - 1
    while i != -1:
        [start1, end1] = ranges1[i]
        [start2, end2] = ranges2[i]
        content1[start1:end1+1] = content2[start2:end2+1]
        i = i -1

def update_runtime_md(content1, content2):
    ranges1 = find_ranges_end_with_empty_line(content1, '.AMDGPU.runtime_metadata')
    ranges2 = find_ranges(content2, '.AMDGPU.runtime_metadata', '.section')
    #dump_ranges(content1, ranges1)
    #dump_ranges(content2, ranges2)
    replace_ranges(content1, ranges1, content2, ranges2)
    
############################################################################
## main program
#constfun = getConstFuncs()
#for f in constfun:        
#    print f

content1 = read_file(target_file)
#dump_list(content1)

content2 = read_file(ref_file)
#dump_list(content2)

update_runtime_md(content1, content2)

write_file(content1, target_file)

print('done!')