# coding: utf-8
# Get tag messages from git depository.
# How to use ?  Command :python git_tag_msg.py <parameter>.
# Parameter is the name of git depository folder. for example: lz4,log4j,etc. [ note : Do not + '/ '].
from __future__ import print_function
import subprocess
import os
import sys
import re
import pandas as pd
import time
from tqdm import tqdm

make_cmd = 'make'
git_cmd = 'git'
cloc_cmd = 'cloc'

def proc(cmd_args, pipe=True, dummy=False):
    if dummy:
        return
    if pipe:
        subproc = subprocess.Popen(cmd_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    else:
        subproc = subprocess.Popen(cmd_args)
    return subproc.communicate()

def make(args, pipe=True):
    return proc([make_cmd] + args, pipe)

def git(args, pipe=True):
    return proc([git_cmd] + args, pipe)

def cloc(args, pipe=True):
    return proc([cloc_cmd] + args, pipe)

if __name__ == '__main__':

    git_name = sys.argv[1]
    base_path=os.getcwd()
    git_path = base_path
    if str(git_name) != './':
        git_path=os.getcwd()+'/'+git_name
    # Switch path to git_path
    os.chdir(git_path)
    # Get git_name if git_name is './';
    if str(git_name) == './' :
        g_name = str(git_path).split('/')
        git_name = g_name[len(g_name)-1]

    # Get time of all tags and tags_time
    stdout, stderr = git(['log', '--tags','--simplify-by-decoration','--pretty=format:"%ci,%d"'])
    stdout = str(stdout).split('\\n')
    tags =[]
    tags_time = []
    if len(stdout) <= 1:
        stdout = stdout[0].split('\n')
    for st in stdout:
        sn = st.split("tag: ")
        try:
            tag_time = sn[0].split(' ')[0]
            tag_time = re.findall(r'\d{4}-\d{2}-\d{2}',tag_time)[0]
        except BaseException:
            print("error: your operation is not true !")
        for i in range(len(sn) - 1):
            snn = sn[i + 1].split(',')
            snn = snn[0].split(')')
            tags.append(snn[0])
            tags_time.append(tag_time)
    print("Retrieve all release tags:\n",tags)
    print("The Time of all release tags:\n",tags_time)

    code1 = []
    code2 = []
    # Count CodeSize of all tags
    print("Begin to count CodeSize:")
    for tag in tqdm(tags,ncols=120):
        git(['checkout',tag])
        # Count the CodeSize of tag
        code_count = cloc(['.'])
        code_count = str(code_count[0])
        code_count = code_count.split(' ')
        CodeSize = (code_count[len(code_count) - 1].split('\\n'))[0].split('\n')[0]
        code1.append(CodeSize)
        # Remove tests and count CodeSize of tag
        code_count_no_tests = cloc(['--exclude-dir=tests,test', '.'])
        code_count_no_tests = str(code_count_no_tests[0])
        code_count_no_tests = code_count_no_tests.split(' ')
        CodeSize_no_tests = (code_count_no_tests[len(code_count_no_tests) - 1].split('\\n'))[0].split('\n')[0]
        code2.append(CodeSize_no_tests)
        # print("CodeSize:",CodeSize)
        time.sleep(0.1)
    print("The CodeSize of all release tags :\n",code1)
    print("The CodeSize of all release tags (removed test):\n", code2)

    # write data to git_name.csv file
    os.chdir(base_path)
    dict = {'版本号': tags, '版本时间': tags_time, 'CodeSize': code1, 'CodeSize去除测试': code2}
    writer = pd.ExcelWriter(git_name + '.xlsx')
    df = pd.DataFrame(dict)
    df.to_excel(writer, columns=['版本号', '版本时间', 'CodeSize', 'CodeSize去除测试'],index=False,encoding='utf-8',sheet_name='Sheet')
    writer.save()


