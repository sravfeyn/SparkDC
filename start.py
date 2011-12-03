#!/usr/bin/env python2

import os
import subprocess
import sys
import time
import remote

#variables
userId = ''
shareFolder = ''
proxyFolder =''
SSH_KEY_INSTR = ''
MIN_FILE_NO = 0
sharedFiles = []
HOST='/home/physics/btech/ph1080614/HOST/shared_files'
serverAddress = 'ssh1.iitd.ernet.in'

def updateHost(arr):
    all_files = ''
    for file in arr:
	namec = proxyFolder.replace('/','[[[')
	fileName = file+'_@'+userId+'_@'+namec
	all_files = all_files+' '+HOST+'/'+fileName
    os.system('ssh '+userId+'@'+serverAddress+' touch'+all_files)

#cleanup shared_files
def tellBye():
    print 'Terminating all connections...please wait'
    os.system('ssh '+userId+'@'+serverAddress+' rm '+HOST+'/*'+userId+'* '+proxyFolder+'status '+proxyFolder+'requests.up')
    print 'Bye!Have a nice day'
    sys.exit(0)

#check for valid usage and save working directory variable and userid
if len(sys.argv)!=3:
    print 'Usage:\n	python start.py ENTRY_NO FOLDER_LOCATION(relative or absolute)\nExample\n	python start.py ee1080323 ~/Videos'
    sys.exit(0)

folderPtr = os.popen('ls '+sys.argv[2])
lsShare = folderPtr.read()
fold = folderPtr.close()
if fold:
    print 'No directory: '+sys.argv[2]
    sys.exit(2)
shareFolder = sys.argv[2]
sharedFiles = lsShare.rstrip().rsplit('\n')
if len(sharedFiles)< MIN_FILE_NO:
    print 'please share more files'
    sys.exit(3)
if shareFolder[-1]!='/':
    shareFolder = shareFolder+'/'

os.system('clear')
print """
Hi,
Using Spark:
	KEEP THIS SHELL OPEN.This shell listens to file requests from other users, and uploads the requested files to corresponding users.
			                               _     
To search for files:	     ____                _    (_) _  
>>Open another shell	    (____) ____    ____ (_)__ (_)(_) 
>>change to spark directory (_)__ (____)  (____)(____)(___)  
>>Type "python get.py 	     _(__)(_)_(_)( )_( )(_)   (_)(_) 
  <Entry No> <Filename>"    (____)(____)  (__)_)(_)   (_) (_)
			          (_)                        
			          (_)
To hide this process:
	Hit Ctrl-Z to background this software, and type "fg" to return back to this process,right in this shell

To exit:
	Before closing, please have the patince to hit Ctrl-C.This is IMPORTANT.

DO NOT WORRY ABOUT THIS SHELL/WINDOW UNTIL YOU WANT TO CLOSE THE CONNECTION.

Starting network processes.
Debug:checking if id is valid"""
ptr = os.popen(r'ssh -q '+sys.argv[1]+r'@'+serverAddress+' pwd')
proxyFolder = ptr.read().rstrip() + '/spark/'
a = ptr.close()
if a:
    print 'Invalid username or password.We suggest you to add SSH keys to your proxy folder by follwoing instructions at '+SSH_KEY_INSTR
    sys.exit(1)
userId = userId + sys.argv[1]

#create reuqest counter folder if doen't exist
print 'Debug:checking if spark folder exists on server'
ptr = os.popen('ssh -q '+userId+r'@'+serverAddress+' cd spark')
ptr.read()
if ptr.close():
    print 'Debug:creating spark'
    os.system(r'ssh -q '+userId+r'@'+serverAddress+' mkdir spark ; chmod -R 777 spark')

#create a requests file, status in spark if not there
print 'Debug:Setting up requests counter'
os.system('ssh '+userId+'@'+serverAddress+' rm '+proxyFolder+'status '+proxyFolder+'requests.up')
os.system('ssh '+userId+'@'+serverAddress+' touch '+proxyFolder+'requests.up '+proxyFolder+'status')

#User is Valid now.Update HOST/shared_files
print 'Debug:uploading shared file info to the HOST'
updateHost(sharedFiles)

#start listening to requests
try:
  while True:
    os.system('touch .requests.up')
    os.system('rm .requests.up')
    os.system('touch .requests.up')
    os.system('scp '+userId+'@'+serverAddress+':'+proxyFolder+'requests.up ./.requests.up')
    ptr = open('.requests.up','r')
    a = ptr.readline().rstrip()
    if a!='':
	ptr.close()
	b = a.split('_?')
	if len(b)!=3:
	    print 'Debug:Inavlid request at requests.up'+a
	    continue
	filename = b[0]
	reqUser = b[1]
	reqPath = b[2]
	os.system('ssh '+userId+'@'+serverAddress+' "echo \''+a+'\' >> spark/status"')
	print reqUser+' '+'is downlaoding '+filename
	if reqPath[-1]!='/':
	    reqPath = reqPath+'/'
	os.system('scp '+shareFolder+filename+' '+userId+'@'+serverAddress+':'+reqPath+'.')
        print 'Debug:Moving to next request'
	os.system('ssh '+userId+'@'+serverAddress+' python spark/removeline.py spark/status 0')
	os.system('ssh '+userId+'@'+serverAddress+' python spark/removeline.py spark/requests.up 0')
	continue
    else:
        print 'Debug:Sleeping.No requests to be served '
        time.sleep(4)
except KeyboardInterrupt:
  tellBye()  
