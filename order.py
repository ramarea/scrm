# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Implementation of the Supply Chain Agent Model by Tan, Li, & Cai (2015)

### ORDER CLASS

class Order:
    def __init__(self, order_qty, max_delay):
        self.quantity = order_qty
        self.time_remaining = max_delay
        
    def unableToFillAtCurrentPeriod():
        self.time_remaining = self.time_remaining - 1
