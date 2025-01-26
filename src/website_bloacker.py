
"""
NOT WORKING 

Run this file by first changing the user to root -> su root
then change permissoion to all -> chmod a+rwx /etc/hosts

then by pythonr run this file

"""

import datetime 
import time 

end_time = datetime.datetime(2024 , 2 , 27)

site_block = ["www.instagram.com" , "www.facebook.com"]

hostpath  = "/etc/hosts"
# host file looks like 
"""
127.0.0.1	localhost
127.0.1.1	NB-DELL-INSP-5430--1898

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
"""

redirect = "127.0.1.1"


while True:
    if datetime.datetime.now() <  end_time: 
        print("Blocking")
        with open(hostpath ,"r+") as hostfile:
            content = hostfile.read()
            for website in site_block:
                if website not in content:
                    hostfile.write(redirect + " " + website  + "\n")
    else:
        with open(hostpath ,"r+") as hostfile:
            content = hostfile.readlines()
            hostfile.seek(0)
            for lines in content:
                if not any (website in lines for website in site_block):
                    hostfile.write(lines)
            hostfile.truncate()
        time.sleep(5)
            
        

            

