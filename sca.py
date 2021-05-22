# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Implementation of the Supply Chain Agent Model by Tan, Li, & Cai (2015)


# LEGEND
# TVA = temporary variable added on
# CDA = code debug added on


# SIMULATION PARAMETERS FOR THE AGENT AND ORDER CLASSES
# NOTE TO SELF, DECIDE IF TO KEEP OR MODIFY
BACK_ORDER_COST = 0.2 # per unit per day
SALE_LOST_COST_MULT = 0.1 # to be multiplied by sale price per unit
INVENTORY_COST = 0.1 # per unit per day
ORDER_COST = 100 # per order
OPERATING_COST = 100 # per agent per day
PRODUCTION_COST = 20 # per unit
SUPPLIER_SALE_PRICE = 40 # per unit
DISTRIBUTION_SALE_PRICE = 50 # per unit
RETAIL_SALE_PRICE = 60 # per unit
ORDER_LEAD_TIME = 1 # day
SHIPMENT_LEAD_TIME = 1 # day
MAXIMUM_LEAD_TIME_DELAY = 5 # days
INITIAL_INVENTORY = 300 # units
SQ_POLICY_S = 200 # units
SQ_POLICY_Q = 300 # units

# SIMULATION PARAMETERS FOR THE DIFFERENT RISK SCENARIOS
# NOTE TO SELF, GAUSSIAN VS POISSON
DLSL_DR = 100 # demand rate for the low demand risk low supply risk scenario
DLSL_SR = 100 # supply rate for the low demand risk low supply risk scenario
DHSL_DR = N(100,sqrt(50)) # demand rate for the high demand risk low supply risk scenario
DHSL_SR = 100 # supply rate for the high demand risk low supply risk scenario
DLSH_DR = 100 # demand rate for the low demand risk high supply risk scenario
DLSH_SR = N(100,sqrt(50)) # supply rate for the low demand risk high supply risk scenario
DHSH_DR = N(100,sqrt(50)) # demand rate for the high demand risk high supply risk scenario
DHSH_SR = N(100,sqrt(50)) # supply rate for the high demand risk high supply risk scenario

# GAME PLAN
# 1. Build Agent Class by 5/20 DELAYED, NOW 5/22
# 2. Build Order Class by 5/21
# 2.1 Order class will have time received and quantity of order
# 3. Build Simulation by 5/23


def receiveNewShipment():
    print("Shipment Received") #CDA 5/19
    
def orderQQty():
    print("Order Q Quantity") #CDA 5/19
    
def processQueuedOrders():
    # While there is sufficient inventory:
    # Fulfill the order at the front of the queue provided the maxdelay has not been exceeded
    # If the orderquantity of front order exceeds inventory, replace the order at the front of queue and attempt to fulfill the next one.
    # Discard any expired order you come across
    # NOTE TO SELF: At what stage of the simulation should I update time? In what order should I propagate through the agents and how do the choices affect the results?
    print("Process Queued Orders") #CDA 5/19
    
def receiveNewOrders(order_time, order_quantity):
    # receive order with time and quantity information
    # Add it to the end of the order queue (Array of order objects for each instance of the agent class)
    # NOTE TO SELF: (pass order queue or make it globally accessible?)
    print("Receive New Orders") #CDA 5/19
        
def endTimestep():
    print("End Timestep") #CDA 5/19

# General Schematic of the process
# Question to self: Do I receive shipment at beginning of time step or at the end of the time step? same question for 
def startTimestep():
    inventory = 0 # TVA 5/19
    S = 5 # TVA 5/19
    receiveNewShipment()
    if (inventory < S):
        orderQQty()
    processQueuedOrders()
    receiveNewOrders(order_time, order_quantity)
    # check SQPolicy and replenish inventory as necessary
    endTimestep()

def main():
    startTimestep()
    
    
if __name__ == '__main__':
    main()
