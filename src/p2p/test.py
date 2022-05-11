import socket
hostname = socket.gethostname()
local_ip=socket.gethostbyname(hostname)
print(socket.getfqdn())
#print(hostname)
print(local_ip=='10.0.0.124')
socket.getfqdn

lista = ['192.168.126',50000,'172.12.34.2',50000,'1.12.34.2',50000]
mystring = ' '.join(map(str,lista))

encoded_string = mystring.encode()

decoded_string = encoded_string.decode()
# new_list=[]
li = list(decoded_string.split(" "))
# a=0
# for val in li:
#     if a%3 == 0:
#         new_list.append(val)
#     else:
#         new_list.append(int(val))
#     a+=1
b=0
c=0
newnew_list= []
for i,val in enumerate(li):

    if b == 0:
        newnew_list.append(list())
        newnew_list[c].append(val) 
        b+=1
    #elif b == 1:
    #    newnew_list[c].append(val)
    #    b+=1
    else:
        newnew_list[c].append(int(val))
        b=0
        c+=1
newnewnew_list=[]        

for val in newnew_list:
    newnewnew_list.append(tuple(val))             

for i in newnewnew_list:
    print(i[0],' ',i[1],' ')
    
