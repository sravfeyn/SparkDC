import os
import sys
import time
import subprocess

serverAddress = 'ssh1.iitd.ernet.in'
proxyFolder = ''
userId = ''
SSH_KEY_INSTR = ''
sharedFiles = []
HOST='/home/physics/btech/ph1080614/HOST/shared_files'
fileName= ''

#checking usage and ID validity
if len(sys.argv)!=3:
    print 'Usage is wrong.It is "python get.py <ENTRY_NO> <FILE_NAME>".\nFor e.g. to search and download Minors.pdf:\n	python get.py ch1070632 Minors.pdf'
    sys.exit(2)

fileName= sys.argv[2]
if fileName.find('/')!=-1:
    print 'Inavlid filename.Filename should not contain "/" charecter' 
    sys.exit(4)

print 'Preparing interactive search.This overhead is only for first search.\nDebug:checking if Id is valid'
ptr = os.popen(r'ssh -q '+sys.argv[1]+r'@'+serverAddress+' pwd')
proxyFolder = ptr.read().rstrip() + '/spark'
a = ptr.close()

if a:
    print 'Invalid username or password.We suggest you to add SSH keys to your proxy folder by follwoing instructions at '+SSH_KEY_INSTR
    sys.exit(1)
userId = userId + sys.argv[1]

print 'Debug:checking if Spark is running'
ptr = os.popen(r'ssh -q '+sys.argv[1]+r'@'+serverAddress+' ls '+proxyFolder)
test = ptr.read().rstrip()
a = ptr.close()
if a or test.find('requests.up')==-1:
    print 'Spark is not yet running.First start Spark by the command:\n"python start.py <ENTRY_NO> <FOLDER_TO_BE SHARED>" '
    sys.exit(2)

while True:
  deco = []
  search_results = []
  found = 0
  print 'Interactive search has started.You can stop this by Ctrl-C\nDebug:searching for file '+fileName
  ptr = os.popen('ssh -q '+userId+r'@'+serverAddress+' ls '+HOST)
  sharedFiles = ptr.read().rstrip().rsplit('\n')
  b = ptr.close()
  if b:
     print 'There are no files currently shared.If you are repeatedly getting this error, your HOST info may not be valid.Change it according to the online instructions.'
  for name in sharedFiles:
     if name.lower().find(fileName.lower())==0:
	  search_results.append(name)
	  found = found + 1	  
  if found==0:
     print 'None has that file'
     if raw_input('Do you want to search for another file [Yes]/[No]').lower().find('y'):
	  print 'Bye!'
	  sys.exit(0)
     else:
	  fileName = raw_input('Enter the filename to search\n')
       	  continue 
  else:
     print 'Matching[s] for your search.'
     counter = 1
     for result in search_results:
	  resulted = result.rsplit('_@')
	  print 'File.No '+str(counter)+'. '+resulted[0]+'	at  '+resulted[1]
     wish = raw_input('Enter the File.No of the file you want from above results\nOr enter 0 search for another file\nOr enter -1 to exit this interactive get.py')
     if int(wish)== -1:
          sys.exit(0)
     elif int(wish)== 0:
	   continue
     else:
        print 'Requesting file to your proxy folder '+proxyFolder
	source_a = search_results[int(wish)-1].rstrip().rsplit('_@')
	namec = source_a[2].replace('[[[','/')
        os.system('python .download.py '+fileName+' '+namec+' '+proxyFolder+' '+userId)
	if raw_input('Do you want to search for another file [Yes]/[No]').lower().find('y'):
           sys.exit(0)
        else:
           fileName = raw_input('Enter the filename to search\n')
           continue

