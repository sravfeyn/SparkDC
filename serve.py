import os
import time

print 'uplaoding remove'
os.system('scp removeline.py ph1080614@ssh1.iitd.ernet.in:/home/physics/btech/ph1080614/.')
try:
 while True:
    print 'downlaoding req.up'
    os.system('scp ph1080614@ssh1.iitd.ernet.in:/home/physics/btech/ph1080614/req.up .')
    ptr = open('req.up','rb')
    a = ptr.readline().rstrip()
    if a!='':
	print 'uploading '+a
	os.system('scp '+a+' '+'ph1080614@ssh1.iitd.ernet.in:HOST') 
        os.system('ssh ph1080614@ssh1.iitd.ernet.in python removeline.py req.up')
    else:
	print 'sleeping '
	time.sleep(4)
except KeyboardInterrupt:
 print 'interrupted'
 os.system('ssh ph1080614@ssh1.iitd.ernet.in rm req.up')
