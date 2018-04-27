#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import subprocess
import shlex
import datetime
import os
import httplib
import wget

#from subprocess import call


class ConnctAndDownld():
	def __init__(self):
		self.url = 'http://172.20.1.70:8000/file' #http server'in kurulu oldugu pc'nin ip adresi, portu ve kalip dosya ismi
		self.ext = ''	#dosya uzantisi gir
		self.sFcount=0	#serverdaki indirilecek dosya sayisi

	def listFD(self,url, ext=''):
    		page = requests.get(url).text
    		#print page
    		soup = BeautifulSoup(page, 'html.parser')
		#print(soup.get_text())
    		return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
	
	def fileList(self):
 		for file in self.listFD(self.url, self.ext):
  			#print "listedeki %s" %file[file.index("/file/")+6:]
			self.sFcount+=1
			print "file %s " %file
			if (file[file.index("/file/")+6:] == "listServer.py"):    
                                if not os.path.exists("listServer.py"):
                                    self.createFile("ThreadControl",file,1)
                                else:
                                    print "bole bir dosya var indirilemez..."                   
			elif file[file.index("/file/")+6:] == "test1.sh":
                                if not os.path.exists("test1.sh"):
                                    self.createFile("ThreadControl",file,1)
                                else:
                                    print "bole bir dosya var indirilemez... %s " % file[file.index("/file/")+6:][-1:]
                        elif file[file.index("/file/")+6:][-1:] == "/":                                
                                self.url=self.url +"/" +file[file.index("/file/")+6:-1]
                                print "url: %s " % self.url
                                self.fileList()                            
                        elif "ThreadControl/" in file:#elif not (file.index("ThreadControl/") == -1):
                                print "ThreadControl/ file..."
                                self.createFile("ThreadControl",file,0)
                        elif file[file.index("/file/")+6:] == "KW41Z-hostcontrol-serial-upgrade-vX.Y.Z.bin":
                                if os.path.exists("KW41Z-hostcontrol-serial-upgrade-vX.Y.Z.bin"):
                                        self.callShellCommand("rm KW41Z-hostcontrol-serial-upgrade-vX.Y.Z.bin")
                                        print "siliniyor..."
                                        
                                else:
                                        print "KW41Z-hostcontrol-serial-upgrade-vX.Y.Z.bin yok .. indiriliyor.."
                                self.createFile("ThreadControl",file,1)
                        else:
                            print "bilinmiyor..."
                        

	def createFile(self,fileName,url,isCreate):
		if not os.path.exists(fileName):
    			os.makedirs(fileName)
		else :
                    print "dosya var"
                r = requests.get(url)
                name=""
                if isCreate ==1:
                    name=url[url.index("/file/")+6:]# url'de /file/ ifadesinden sonraki dosya ismini aliyoruz.
                elif isCreate == 0:
                    name=url[url.index("/ThreadControl/")+15:] #url 'de /ThreadControl/ ifadesinden sonra gelen dosya ismini aliyoriz.
                with open(name, 'wb') as f:  
                    f.write(r.content)

                # Retrieve HTTP meta-data
                print(r.status_code)  
                #print(r.headers['content-type'])  
                #print(r.encoding) 
                if r.status_code==200:
                        print "200"
                        if isCreate==0:
                            os.rename(name, "ThreadControl/%s" % name) #inen dosyalari ThreadControl dosyasinin icine kopyaliyiruz.
                        #self.sFcount-=1
                        #print "%s tasindi..." % name
                        
                if self.sFcount==13: # toplamda 12 tane dosya inmis ise derlemeyi baslatiyoruz.
                       # self.compile()
                        print "compileeeeeeeee......"
                print self.sFcount
				
				
	def compile (self):
		#subprocess.call('chmod +777 ~/test/selam/test1.sh')
                #subprocess.call('chown -R $USER selam/test1.sh')
                self.callShellCommand("chmod +777 test1.sh")
		subprocess.call(shlex.split('./test1.sh')) #shell command calistiriyoruz...
		
        def callShellCommand(self,command):
                subprocess.call(shlex.split(command))

if __name__=='__main__':

	lists=ConnctAndDownld()
	lists.fileList()
	
	
	
