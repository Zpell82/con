#!/usr/bin/env python3
from os import environ
import pexpect
from sys import argv, exit
import time , socket

class login:
    def __init__(self,host=None):
        self.host = host
        if len(argv) > 1:
            self.host = argv[1]
        elif self.host == None:
            self.host = input("host:" )
         
        self.password = environ.get("PASSWORD")
        self.username = environ.get("USERNAME")
        self.inst_password = environ.get("HUA_PASS")
        self.mw_password = environ.get("TN_PASS")
        self.ssh = f"ssh {self.host}"
        
    def printer(self):
        print(self.host,self.ssh)

    def test(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host,22))
        data=s.recv(4096)
        s.close()
        self.data = data.decode('utf-8')
        self.data = self.data.strip()
        print(self.data)
        if "OpenSSH_6.0" in self.data:
            self.unit = "juniper"
        elif "SSH-2.0-OpenSSH_6.1" in self.data:
            self.unit = "mw"
        elif "SSH-2.0-Cisco-2.0" in self.data:
            self.unit = "cisco"
        else:
            self.unit = "hua"
        return self.unit

    def login(self):
        
        s = self.test()
        
    
        values = {
            "juniper":f"{self.username}@",
            "mw":f"{environ.get('TN_USER')}@",
            "cisco":f"{self.username}@",
            "hua":f"{environ.get('HUA_USER')}@"
        }
        passvalues = {
            "juniper":self.password,
            "mw":self.mw_password,
            "cisco":self.password,
            "hua":self.inst_password
        }
        print(values.get(self.unit))
        login_str = f"ssh {values.get(self.unit)}{self.host} -o StrictHostKeyChecking=no"
        passw = passvalues.get(self.unit)

        try:
            pssh = pexpect.spawn(login_str)
            #pssh.logfile = sys.stdout.buffer ##debug line
            
            try:
                
                print(pssh.expect(["The ","yes", pexpect.EOF],timeout=3))
                pssh.sendline("yes")
            except:
                pass
            
            pssh.expect ('[Pp]assword:', timeout=1)
            time.sleep(0.1)
            passw = passvalues.get(self.unit)
            pssh.sendline(passw)
            pssh.interact()
        except KeyboardInterrupt:
            pssh.spawn.close()
            exit()
        finally:
            pssh.close()
            print("closing ssh spawn")
            exit()
if __name__ == "__main__":
    s = login()
    s.login()
