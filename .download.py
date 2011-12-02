import os
import sys
import time

HOST = 'home/physics/btech/ph1080614/HOST/shared_files/'

serverAddress = 'ssh1.iitd.ernet.in'
myId = sys.argv[4]
fileName = sys.argv[1]
myAddress = sys.argv[3]
urAddress = sys.argv[2]
if myAddress[-1]!='/':
    myAddress = myAddress + '/'
if urAddress[-1]!='/':
    urAddress = urAddress + '/'

def cleanupInfo():
    sli = urAddress.rsplit('/')
    toB = sli[-3]
    os.system('ssh '+myId+'@'+serverAddress+' rm '+HOST+'*'+toB+'*')

print 'Debug:checking for slots'
ptr = os.popen('ssh '+myId+'@'+serverAddress+' head -1 '+urAddress+'status')
test = ptr.read().rstrip()
a = ptr.close()
if a:
   cleanupInfo()
   print 'The user went offline.'
   sys.exit(0)
theRequest = fileName+'_?'+myId+'_?'+myAddress
print 'Slot seems free.Seeding the request to source'
os.system('ssh '+myId+'@'+serverAddress+' '+'"echo \''+theRequest+'\' >> '+urAddress+'requests.up"')
print 'The request has been put up.And file should be getting downloaded to your spark folder.You can check it or watch for report from this process.This will not show you trasnfer dialogue.It onnly make sures the trasnfer is taking place.'
time.sleep(2)
size = 0
for i in range (0,3):
	if i>=1:
	    print 'Checking on trasnfer status.Check '+str(i)+' of 2.'
	ptr = os.popen('ssh '+myId+'@'+serverAddress+' head -1 '+urAddress+'/status')
	test = ptr.read().rstrip()
	b = ptr.close()
	th = test.rsplit('_?')
	if b :
	    cleanupInfo()
	    print 'User just went offline!!'
	    sys.exit(0)
	if len(th)!=3:
	    continue
	downloader = ''
	if th[2][-1]!='/':
	    downloader = th[2]+'/'
	else:
	    downloader = th[2]
	sizePtr = os.popen('ssh '+myId+'@'+serverAddress+' stat -c %s '+downloader+th[0])
	stemp = int(sizePtr.read().rstrip())   
	if sizePtr.close():
	    continue    
	if size ==0 and size!=stemp:
	    size = stemp
	    continue
	if size == stemp:
	    continue
	else:
	    if th[0]==fileName:
		print fileName +' is successfuly being downloaded to your Spark folder '+myAddress
		sys.exit(0) 
	    else:
		print 'Slot is not free.Check again later.'+'The user is uploading '+th[0]+' to '+th[2]
		print 'You can wait or you can try downloading it from any other user by use of search.py and download.py' 
		sys.exit(0)
cleanupInfo()
print 'User is not online.Search again to find other sources'
sys.exit(0)
