# -*- coding: utf-8 -*-
"""

Initial author: nargo : Azas Dimitrios
Part of the master thesis  :  https://ikee.lib.auth.gr/record/297191/?ln=en
Refactoring : K.Draziotis, drazioti@gmail.com

licence : GPL v.2
"""

import socket,ssl,OpenSSL.crypto
from Crypto.Util import asn1
from Crypto.PublicKey import RSA
from OpenSSL.crypto import FILETYPE_PEM,FILETYPE_ASN1
from datetime import datetime
import subprocess

def checkIfTrusted(hostname,port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_default_certs()
    context.check_hostname = True # check_hostname enabled so that we are able to validate the certificate
    sock = socket.create_connection((hostname, port))
    sslsock = context.wrap_socket(sock, server_hostname=hostname)
    if context.check_hostname:
        #to validate a certificate we check that the obtained certificate matches the desired service
        if ssl.match_hostname(sslsock.getpeercert(), hostname) == None:
            print "Trusted: Yes"
        else:
            print "Trusted: No"
    sock.close()
    return

#Gets Certificate details 
def getCertificateDetails(hostname,port):  
    
    #Server Certificate
    cert1 = ssl.get_server_certificate( (hostname,port) )
    request = OpenSSL.crypto.load_certificate(FILETYPE_PEM,cert1)


    key = request.get_pubkey()
    if key.type() == OpenSSL.crypto.TYPE_RSA:
        key_type = 'RSA'
    else:
        key_type = 'DSA'
    if key_type == 'RSA':
        print key_type+" key type"
        print "Key size:", key.bits()
        print "serial: ", request.get_serial_number()
        subject = request.get_subject()
        components = dict(subject.get_components())
        d = components
        if 'CN' in d.keys():
            print "Common name:", d['CN']
        if 'O' in d.keys():
            print "Organisation:", d['O']
        if 'L' in d.keys():
            print "City/locality:", d['L']
        if 'ST' in d.keys():
            print "State/province:", d['ST']
        if 'C' in d.keys():
            print "Country:", d['C']
        issuer = request.get_issuer()
        issued_by = issuer.CN
        print "issued by: ", issued_by        
        try:
            expire_date = datetime.strptime(request.get_notAfter(),"%Y%m%d%H%M%SZ")
            print 'Valid until: ',expire_date
            expires_in = expire_date - datetime.now()
            if expires_in.days >= 0:
                print 'Expires in',expires_in.days, 'days'
            else:
                print 'Certificate expired.'
        except:
            print 'Certificate date format unknown.'        
        
        # 1. we convert PEM to ASN format
        # 2. we export the rsa_modulus and public exponent e

        pub_asn1= OpenSSL.crypto.dump_privatekey(FILETYPE_ASN1, key)
        pub_der=asn1.DerSequence()
        pub_der.decode(pub_asn1)
        pub_modulus=pub_der[1]
        pub_exponent=pub_der[2]
        print "rsa modulus N:",pub_modulus
        print "e:",pub_exponent

        

def getSupportedCiphers(hostname,port):
    #Get all the available ciphers and saves them in a list
    cipherlist = subprocess.Popen("openssl ciphers 'ALL:eNULL' | sed -e 's/:/ /g'",shell=True, stdout =subprocess.PIPE).stdout.read()
    cipher=""
    count=0
    sslv2=[]
    sslv3=[]
    tlsv1=[]
    tlsv1_1=[]
    tlsv1_2=[]
    ciphers_supported=0
    ciphers_unsupported =0
    rc4_flag = False
    versions = ['tls1_2','tls1_1','tls1','ssl3','ssl2']
    #We iterate in every ssl protocol version
    for v in versions: 
        #we iterate through all the available ciphers that we got from the previous command
        for i in cipherlist:
            if i!=" ":
                cipher = cipher + i
            else:
                command = "openssl s_client -cipher " + str(cipher)+ " -"+ str(v) + " -connect " + str(hostname) + ":" + str(port) + " < /dev/null > /dev/null 2>&1" 
                try:    
                    result = subprocess.check_output(command,shell=True) 
#                    print "Cipher",cipher,"is supported"
                    ciphers_supported = ciphers_supported +1
#                    if v == 'ssl3':
#                        count_ssl3 = count_ssl3 + 1
                    if v == 'tls1_2':
                        tlsv1_2.append(cipher)
                    elif v == 'tls1_1':
                        tlsv1_1.append(cipher)
                    elif v == 'tls1':
                        tlsv1.append(cipher)
                    elif v == 'ssl3':
                        sslv3.append(cipher)
                    elif v == 'ssl2':
                        sslv2.append(cipher)
                except subprocess.CalledProcessError:
                    ciphers_unsupported = ciphers_unsupported +1
                cipher = ""
                count = count + 1
    
    print " "
    if len(tlsv1_2) == 0:
        del versions[0]
    if len(tlsv1_1) == 0:
        del versions[1]
    if len(tlsv1) == 0:
        del versions[2]
    if len(sslv3) == 0:
        del versions[3]
#    if len(sslv2) == 0:
#        del versions[4]
    print "Protocols:"
    for v in versions:
        if v == 'tls1_2':
            print "TLS v1.2"
        elif v == 'tls1_1':
            print "TLS v1.1"
        elif v == 'tls1':
            print "TLS v1"
        elif v == 'ssl3':
            print "SSL v3"
        elif v == 'sslv2':
            print "SSL v2"
    print " "
    
    print "Total Ciphers supported:",ciphers_supported
    print " "
    print "Protocol version: TLS v1.2"
    if len(tlsv1_2) != 0:
        for x in tlsv1_2:
            if "RC4" in x:
                rc4_flag = True
            print "Cipher",x,"is supported"
    else:
        print "-"
    print " "
    print "Protocol version: TLS v1.1"
    if len(tlsv1_1) != 0:
        for x in tlsv1_1:
            if "RC4" in x:
                rc4_flag = True
            print "Cipher",x,"is supported"
    else:
        print "-"
    print " "
    print "Protocol version: TLS v1"
    if len(tlsv1) != 0:
        for x in tlsv1:
            if "RC4" in x:
                rc4_flag = True
            print "Cipher",x,"is supported"
    else:
        print "-"
    print " "
    print "Protocol version: SSL v3"
    if len(sslv3) != 0:
        for x in sslv3:
            if "RC4" in x:
                rc4_flag = True
            print "Cipher",x,"is supported"
    else:
        print "-"
    print " "
    print "Protocol version: SSL v2"
    if len(sslv2) != 0:
        for x in sslv2:
            if "RC4" in x:
                rc4_flag = True
            print "Cipher",x,"is supported"
    else:
        print "-"
    print " "
        
    if len(sslv3) == 0:
        print "POODLE (SSLv3) : No, SSLv3 not supported"
    else:
        print "POODLE (SSLv3) : Yes"
    print " "
    if rc4_flag == True:
        print "RC4: Yes"
    else:
        print "RC4: No"

try:
    print "Give server name:"
    hostname = raw_input()
    print "port:"
    port = eval( raw_input() )
    print " "
    getCertificateDetails(hostname,port)
    #checkIfTrusted(hostname,port)
    getSupportedCiphers(hostname,port)
    
except SyntaxError:
        print 'You set something in the input either wrong or NULL'
