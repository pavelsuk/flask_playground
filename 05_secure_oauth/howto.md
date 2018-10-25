# How To Secure the App

*Based on on book
[Python Microservices Development - by Tarek Ziadé](https://www.safaribooksonline.com/library/view/python-microservices-development/9781785881114/) and [tokendealer code on github](https://github.com/Runnerly/tokendealer/tree/master/runnerly/tokendealer)*

## Generate private/public key

You can do it on Linux distro. I tried to use git bash (MINGW64) on Windows, but it didn't work. Alternatively puttygen should also work, but it failed on win machine as well. Generating it on RPI works fine.

These keys should not be stored in git, I have them here only for testing purpose.

``` bash
$ openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
Generating a 4096 bit RSA private key
..........................++
..........................++
writing new private key to 'key.pem'
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields, but you can leave some blank

 For some fields, there will be a default value,

 If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CZ
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (e.g., company) [Internet Widgits Pty Ltd]:Token Dealer

Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:Token
Email Address []:token@token.com

$ openssl x509 -pubkey -noout -in cert.pem > pubkey.pem
```

and

``` bash
$ openssl rsa -in key.pem -out privkey.pem
Enter pass phrase for key.pem:
writing RSA key
```