# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Implementation of the Supply Chain Agent Model by Tan, Li, & Cai (2015)
# VERSION 1.0

### AGENT CLASS

import order
import numpy as np
import pandas as pd

# SIMULATION PARAMETERS FOR THE AGENT AND ORDER CLASSES
SALE_LOST_COST_MULT = 0.1 # to be multiplied by sale price per unit
INVENTORY_COST = 0.1 # per unit per day
ORDER_COST = 100 # per order
OPERATING_COST = 100 # per agent per day
PRODUCTION_COST = 20 # per unit
SUPPLIER_SALE_PRICE = 40 # per unit
DISTRIBUTION_SALE_PRICE = 50 # per unit
RETAIL_SALE_PRICE = 60 # per unit
INITIAL_INVENTORY = 300 # units
SQ_POLICY_S = 200 # units
SQ_POLICY_Q = 300 # units
# THE FOLLOWING PARAMETERS ARE EITHER NOT USED OR USED IMPLICITLY IN THE CURRENT VERSION OF THIS PROGRAM
BACK_ORDER_COST = 0.2 # per unit per day
ORDER_LEAD_TIME = 1 # day # CHANGING THIS REQUIRES CHANGING THE CODE ON THIS VERSION
SHIPMENT_LEAD_TIME = 1 # day # CHANGING THIS REQUIRES CHANGING THE CODE ON THIS VERSION

class Agent:
    def __init__(self, name):
        self.name = name # naming will come from adjacency matrix
        self.type = self.name[0] # R = retailer, D = distribution center, S = supplier
        self.orders_queue = [] # NTS: IS AN ARRAY THE BEST STRUCTURE TO USE FOR A QUEUE?
        self.inventory = INITIAL_INVENTORY
        self.suppliers = [] # Agents upstream of current agent, empty if self.type = "S"
        self.customers = [] # Agents downstream of current agent, empty if self.type = "R"
        self.discarded_orders = 0
        self.filled_orders = 0
        self.current_time = 0
        self.shipments_out = {"D1":0, "D2":0,"R1":0,"R2":0,"S1":0,"S2":0}
        self.orders_out = {"D1":0, "D2":0,"R1":0,"R2":0,"S1":0,"S2":0}
        self.num_orders_placed = 0
        self.qty_orders_placed = 0
        self.cost = 0
        self.revenue = 0
        self.env_dr = 100 # demand rate into retailer in scenario
        self.env_sr = 100 # supply rate into supplier in scenario
        self.metrics = pd.DataFrame(columns = ['Time','Filled Orders', 'Discarded Orders', 'Revenue', 'Costs'])
    
    # This function receives all the orders from the previous time period.A special case is defined for the retailer whose customers are not considered nodes in our model. We use the demand rates based on the risk scenario for the incoming order in that case.
    def receiveOrder(self):
        if self.type != "R":
            for customer in self.customers:
                the_order = order.Order(customer.name, customer.orders_out.get(self.name))
                self.orders_queue.append(the_order)
                #print(self.orders_queue[0].quantity)
        else:
            the_order = order.Order("customer", self.env_dr)
            self.orders_queue.append(the_order)
            
    # This function places an order of Q units to suppliers in order to replenish the inventory level after it falls below level S according to the specified SQ Policy. It divides the orders evenly amongst all the supplier of the agent. One edge case is when the agent is a supplier, we do not consider the suppliers of suppliers as nodes in our model. So the supply rates into the supplier are based on the risk scenario rates. As such an agent with type "S" for supply, does not "place an order" to replenish their supply.
    def replenishInventory(self, reorder_qty):
        if self.type != "S":
            for supplier in self.suppliers:
                self.orders_out[supplier.name] = 1 / len(self.suppliers) * reorder_qty
    
    # This function implements the agent's SQ inventory policy.
    def inventoryCheck(self):
        if self.inventory < SQ_POLICY_S:
            self.replenishInventory(SQ_POLICY_Q)
    
    # This function adds incoming shipments from the agent's suppliers into the inventory. As explained above, agents of type "S" get their supply from the risk scenario supply rates as their suppliers are not considered nodes in our network.
    def receiveNewShipment(self):
        if self.type != "S":
            for supplier in self.suppliers:
                self.inventory += supplier.shipments_out.get(self.name)
        else:
            self.inventory += self.env_sr

   # This function sends out a processed order to the agent's customer.
    def shipToCustomer(self,customer,quantity):
        self.shipments_out[customer] = quantity
   
   # This function processes an agent's queued orders.
   # DEBUGGING NOTES: THE ELSE WORKS AS EXPECTED
    def processQueuedOrders(self):
        for order in self.orders_queue:
            if order.quantity <= self.inventory and order.time_remaining >= 0:
                self.filled_orders += 1
                self.inventory -= order.quantity
                self.shipments_out[order.customer] = order.quantity
            elif order.quantity < self.inventory and order.time_remaining >= 0:
                order.unableToFillAtCurrentPeriod()
            else:
                self.discarded_orders += 1
                self.orders_queue.remove(order)
        
    # Think about how to capture the different cost rates
    def calculateCosts(self):
        qty_cost = 0
        qty_price = 0
        if self.type == "S":
            qty_cost = PRODUCTION_COST
            qty_price = SUPPLIER_SALE_PRICE
        elif self.type == "D":
            qty_cost = SUPPLIER_SALE_PRICE
            qty_price = DISTRIBUTION_SALE_PRICE
        else:
            qty_cost = DISTRIBUTION_SALE_PRICE
            qty_price = RETAIL_SALE_PRICE
        self.cost = OPERATING_COST + INVENTORY_COST * self.inventory + self.num_orders_placed * ORDER_COST + self.qty_orders_placed * qty_cost + self.discarded_orders * qty_price * SALE_LOST_COST_MULT
    
    def calculateRevenue(self):
        qty_price = 0
        if self.type == "S":
            qty_price = SUPPLIER_SALE_PRICE
        elif self.type == "D":
            qty_price = DISTRIBUTION_SALE_PRICE
        else:
            qty_price = RETAIL_SALE_PRICE
        self.revenue = self.filled_orders * qty_price
    
    # This function resets back to zero every single value that is measured on a per period basis for the agent.
    def resetPeriodValues(self):
        self.num_orders_placed = 0
        self.qty_orders_placed = 0
        self.filled_orders = 0
        self.discarded_orders = 0
        self.cost = 0
        self.revenue = 0
    
    # This function will keep track of and update the VA and CSL metrics to measure the performance of the supply chain under various network topologies and risk scenarios.
    def updateMetrics(self):
        temp = pd.DataFrame({'Time':[self.current_time], 'Filled Orders': [self.filled_orders], 'Discarded Orders': [self.discarded_orders], 'Revenue': [self.revenue], 'Costs':[self.cost]})
        og_df = self.metrics
        og_df = og_df.append(temp,ignore_index=True)
        self.metrics = og_df
