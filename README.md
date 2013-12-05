#Customer Service Server
This is a simulated customer service phone system. At first I just write a
naive socket server simulation, but then I realized this cannot demostrate
my love for zhihu (^_^), therefore I implemented a web application based on
Tornade.

##Solution 1: SocketSever
You may modify configuration in `config.py`. The customer service phone
number is ranged from 1000 to 1020 by default.

To use it, you should first run `server.py` and then run `client.py`. Please note that each customer service will serve exactly one minute so the user should wait at least one minute before calling when all customer services are busy.

Following commands are supported:

* No.$(service number) offline 
* No.$(service number) online
* call from $(Customer number

##Solution 2. Tornade framwork
You can see the real demo at
[http://zuozhuo.info/zhihu](http://zuozhuo.info/zhihu).

or you can run it by `python index.py`

This solution implemented many more features than the previous solution. It
can distinguish whether the client is a customer or a customer service. 

If you are customer, you can only write your phone number and call.

If you are customer service, then follwing two commands are supported:

* No.$(service number) offline 
* No.$(service number) online

