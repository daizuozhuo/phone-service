import logging
from threading import Timer
from config import (CUSTOMER_SERVICE_ENDNUMBER, CUSTOMER_SERVICE_STARTNUMBER)

class CustomerService():
    BUSY, FREE, OFFLINE = 0, 1, 2
    def __init__(self, number, work_time=0):
        self.number = number
        self.work_time = work_time
        self.status = CustomerService.FREE
   
    def __lt__(self, other):
        return self.work_time < other.work_time

    def __eq__(self, other):
        return self.number == other.number

    def free(self):
        self.status = CustomerService.FREE

    def busy(self):
        timer = Timer(60.0, self.free)
        self.status = CustomerService.BUSY
        timer.start()
        self.work_time += 1
            
    def offline(self):
        if self.status == CustomerService.BUSY: return False
        self.status = CustomerService.OFFLINE
        return True

#this class is singleton
class ServiceManager():
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = (ServiceManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.services=dict()
        for i in range(CUSTOMER_SERVICE_STARTNUMBER,
                       CUSTOMER_SERVICE_ENDNUMBER):
            self.services[i] = CustomerService(i)

    def handle(self):
        data = self.rfile.readline().strip()
        self.process(data)
        logging.info("%s wrote %s" % (self.client_address[0], data))

    def process(self, data):
        parts = data.split()
        if len(parts) == 2:
            return self.responseCustomerService(parts)
        elif len(parts) == 3:
            return  self.responseCustomer(parts[2])
        else:
            return "unsupported command"

    def responseCustomerService(self, parts):
        number = int(parts[0].split(".")[1])
        if not self.isValidNumber(number):
            return "invalid phone number" 
            return
        if parts[1] == "offline" and number in self.services:
            if not self.services[number].offline():
                return "sorry, you can't leave when calling" 
            else:
                return "ok, you can leave for now" 
        elif parts[1] == "online":
            self.services[number].free()
            return "welcome back" 
        else:
            return "unsupported command" 

    def responseCustomer(self, customer):
        service_number = self.assignService()
        if service_number:
            return "Hello %s, no. %s is servering for you"\
                             % (customer, service_number)
        else:
            return "Sorry %s, our system is busy, please\
                             call us later" % customer
                    
    def isValidNumber(self, number):
        return number in range(CUSTOMER_SERVICE_STARTNUMBER, CUSTOMER_SERVICE_ENDNUMBER)

    def assignService(self):
        min_time = float("inf")
        mark = -1
        for key in self.services:
            if self.services[key].status == CustomerService.FREE\
                and min_time > self.services[key].work_time:
                mark = key
                min_time =  self.services[key].work_time
        if mark == -1: return None
        else: 
            self.services[mark].busy()
            return mark


