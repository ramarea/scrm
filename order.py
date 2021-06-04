# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Implementation of the Supply Chain Agent Model by Tan, Li, & Cai (2015)

### ORDER CLASS

MAXIMUM_LEAD_TIME_DELAY = 5

class Order:
    def __init__(self, customer, order_qty):
        self.quantity = order_qty #int(order_qty or -9)
        self.time_remaining = MAXIMUM_LEAD_TIME_DELAY
        self.customer = customer # where it should be sent when it is fulfilled
    
    # This function reduces the time remaining for an agent to try and fill the order against the Maximum Lead Time Delay if an order is not filled in the current time period. 
    def unableToFillAtCurrentPeriod(self):
        self.time_remaining -= 1
