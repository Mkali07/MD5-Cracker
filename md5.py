#!/usr/bin/python
# -*- coding: utf-8 -*-
#####Begin import modules######

import re,requests,random,threading,sys,json,time
from termcolor import colored

try:
    from termcolor import colored
except:
    print "no install module termcolor for setup command down:\npip install termcolor"
    sys.exit()

#####End import modules######

class view_info(object):
    def __init__(self):

        global hashvalue,hashtype,flag
        self.hashvalue = list(open(sys.argv[1],'r').read().splitlines())
        self.hashtype = sys.argv[2]

    	self.user_agents = ["Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko)",
                           "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1",
                           "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko)",
                           "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
                           "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
                           "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))"]


        self.head = {
                        'UserAgent':random.choice(self.user_agents)
                    }

        self.crack_md5(self.hashvalue,self.hashtype)




    def crack_md5(self,hashvalue,hashtype):
        thread = []
        cracked = []
        try:
            for hash in self.hashvalue:
		    if hash.strip():
                    	run = threading.Thread(target=self.md5_1, args=(hash, self.hashtype))
                    	run.start()
                    	thread.append(run)
                    	time.sleep(0.05)
            for j in thread:
                    j.join()
        except:
            print "Erro"
	    print (colored("[-]",'red')),("try Crack hash  %s Not Cracked" % hashvalue)
            with open('faild_crack_md5.txt', 'a') as notmd5:
                    notmd5.write(hashvalue+'\n')
            pass


    def Auxiliary_1(self,hashvalue,hashtype):
	url = "https://md5.gromweb.com/?md5="+hashvalue
        response = requests.get(url,headers=self.head,timeout=20)
	if "was succesfully reversed into the string:" not in response.text:
		self.md5_3(hashvalue,self.hashtype)
	else:
        	match = re.search(r'<em class="long-content string">(.*?)</em></p>', response.text).group(1)
        	if match:
            		flag = True
	    		print (colored("[+]",'blue')),("try Crack hash  %s Cracked" % hashvalue)
            		with open('crack_md5.txt', 'a') as cmd5:
                    		cmd5.write(hashvalue+":"+match+'\n')
        	else:
            		flag = False
            		self.md5_4(hashvalue,self.hashtype)




    def md5_1(self,hashvalue,hashtype):
        self.flag = False
        res = requests.get('http://lea.kz/api/hash/' + hashvalue,headers=self.head)
        if res.status_code == 200:
            flag = True
            resp = json.loads(res.text)
            md5 = resp['password']
	    print (colored("[+]",'blue')),("try Crack hash  %s Cracked" % hashvalue)
            with open('crack_md5.txt', 'a') as cmd5:
                    cmd5.write(hashvalue+":"+md5+'\n')

        elif self.flag == False:
            self.md5_2(hashvalue,self.hashtype)
                

    def md5_2(self,hashvalue,hashtype):
        self.flag = False
        response = requests.get("http://www.nitrxgen.net/md5db/"+hashvalue,headers=self.head).text
	if hashvalue == "":
		self.md5_3(hashvalue,self.hashtype)
        if response:
            flag = True
	    print (colored("[+]",'blue')),("try Crack hash  %s Cracked" % hashvalue)
            with open('crack_md5.txt', 'a') as cmd5:
                    cmd5.write(hashvalue+":"+response+'\n')
        else:
	    self.md5_3(hashvalue,self.hashtype)
            flag = False
            


    def md5_3(self,hashvalue,hashtype):
        url = "http://hashtoolkit.com/reverse-hash/?hash="+hashvalue
        response = requests.get(url,headers=self.head,timeout=120)
	if "No hashes found for" in response.text:
		self.md5_4(hashvalue,self.hashtype)
	else:
        	match = re.findall('<span title="decrypted md5 hash">(.*)</span>', response.text.encode('utf-8'))[0]
        	if match:
            		flag = True
	    		print (colored("[+]",'blue')),("try Crack hash  %s Cracked" % hashvalue)
            		with open('crack_md5.txt', 'a') as cmd5:
                    		cmd5.write(hashvalue+":"+match+'\n')
        	else:
            		flag = False
            		self.md5_4(hashvalue,self.hashtype)


    def md5_4(self,hashvalue,hashtype):
        data = {'auth':'8272hgt', 'hash':hashvalue, 'string':'','Submit':'Submit'}
        response = requests.post('http://hashcrack.com/index.php' , data,headers=self.head).text
        match = re.search(r'<span class=hervorheb2>(.*?)</span></div></TD>', response)
        if match:
            flag = True
            with open('crack_md5.txt', 'a') as cmd5:
                    cmd5.write(hashvalue+":"+match.group(1)+'\n')
        else:
            flag = False
            self.md5_5(hashvalue,self.hashtype)

    def md5_5(self,hashvalue,hashtype):
        response = requests.get('http://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=cec59329@iencm.com&code=fb3e1d8681b6a438' % (hashvalue, self.hashtype)).text
        if len(response) != 0:
            flag = True
	    print (colored("[-]",'blue')),("try Crack hash  %s Cracked" % hashvalue)
            with open('crack_md5.txt', 'a') as cmd5:
                    cmd5.write(hashvalue+":"+response+'\n')
        else:
            flag = False
	    print (colored("[+]",'blue')),("try Crack hash  %s Cracked" % hashvalue)
            with open('faild_crack_md5.txt', 'a') as notmd5:
                    notmd5.write(hashvalue+'\n')





view_info()

