# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Implementation of the Supply Chain Agent Model by Tan, Li, & Cai (2015)

### AGENT CLASS

class Agent:
    def __init__(self, name, INITIAL_INVENTORY):
        self.name = name # naming will come from adjacency matrix
        self.type = self.name[0] # R = retailer, D = distribution center, S = supplier
        self.orders_queue = [] # NTS: IS AN ARRAY THE BEST STRUCTURE TO USE FOR A QUEUE?
        self.inventory = INITIAL_INVENTORY
        self.suppliers = [] # Agents upstream of current agent, empty if self.type = "S"
        self.customers = [] # Agents downstream of current agent, empty if self.type = "R"
        self.discarded_orders = 0
        self.filled_orders = 0
        self.current_time = 0
        self.value_add = 0
    
    def receiveOrder(self, order):
        self.orders_queue.append(order)
        
    # policy is a tuple with S at 0 and Q at 1
    def inventoryCheck(self, policy):
        if self.inventory < policy[0]:
            self.replenishInventory(current_time, policy[1])
            
    def replenishInventory(current_time, reorder_qty):
        print("I am here")
        
    def receiveNewShipment():
        print("Shipment Received") #CDA 5/19
        
    def processQueuedOrders():
        # While there is sufficient inventory:
        # Fulfill the order at the front of the queue provided the maxdelay has not been exceeded
        # If the orderquantity of front order exceeds inventory, replace the order at the front of queue and attempt to fulfill the next one.
        # Discard any expired order you come across
        # NOTE TO SELF: At what stage of the simulation should I update time? In what order should I propagate through the agents and how do the choices affect the results?
        print("Process Queued Orders") #CDA 5/19
