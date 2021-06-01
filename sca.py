# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Implementation of the Supply Chain Agent Model by Tan, Li, & Cai (2015)

import numpy as np
import agent
import order

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
DHSL_DR = np.random.normal(loc = 100, scale = np.sqrt(50))# demand rate for the high demand risk low supply risk scenario
DHSL_SR = 100 # supply rate for the high demand risk low supply risk scenario
DLSH_DR = 100 # demand rate for the low demand risk high supply risk scenario
DLSH_SR = np.random.normal(loc = 100, scale = np.sqrt(50)) # supply rate for the low demand risk high supply risk scenario
DHSH_DR = np.random.normal(loc = 100, scale = np.sqrt(50)) # demand rate for the high demand risk high supply risk scenario
DHSH_SR = np.random.normal(loc = 100, scale = np.sqrt(50)) # supply rate for the high demand risk high supply risk scenario

# ADJACENCY MATRICES
A_1 = np.array([
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0],
     [1, 0, 0, 0, 1, 0],
     [0, 1, 0, 0, 0, 1],
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0]
])

A_2 = np.array([
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0],
     [1, 0, 0, 0, 1, 1],
     [0, 1, 0, 0, 1, 1],
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0]
])

A_3 = np.array([
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0],
     [1, 1, 0, 0, 1, 0],
     [1, 1, 0, 0, 0, 1],
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0]
])

A_4 = np.array([
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0],
     [1, 1, 0, 0, 1, 1],
     [1, 1, 0, 0, 1, 1],
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0]
])



        
def endTimestep():
    print("End Timestep") #CDA 5/19

# General Schematic of the process
# Question to self: Do I receive shipment at beginning of time step or at the end of the time step? same question for 
def startTimestep():
    inventory = 0 # TVA 5/19
    S = 5 # TVA 5/19
    order_time = 0
    order_quantity = 50
    #receiveNewShipment()
    #if (inventory < S):
     #   orderQQty()
    #processQueuedOrders()
    #receiveNewOrders(order_time, order_quantity)
    # check SQPolicy and replenish inventory as necessary
    endTimestep()

def runNetwork1():
    startTimestep()



def initializeAgents():
    s1 = agent.Agent("S1", INITIAL_INVENTORY)
    s2 = agent.Agent("S2", INITIAL_INVENTORY)
    d1 = agent.Agent("D1", INITIAL_INVENTORY)
    d2 = agent.Agent("D2", INITIAL_INVENTORY)
    r1 = agent.Agent("R1", INITIAL_INVENTORY)
    r2 = agent.Agent("R2", INITIAL_INVENTORY)
    return [s1, s2, d1, d2, r1, r2]

# This helper function adds a link between every node i and j that are connected in the adjancency matrix. It assumes there are 2 objects of each agent type.
def addLinks(start, end, adj_mat, agents):
    for i in range(start, end + 1):
        for j in range(start + 2, end + 3):
            if adj_mat[i,j] == 1:
                agents[i].customers.append(agents[j])
                agents[j].suppliers.append(agents[i])

# This function adds links between suppliers and distribution centers. It assumes 6 agents with 0,1 as suppliers, 2,3 as distribution centers, and 4,5 as retailers.
def linkSuppliers(adj_mat, agents):
    sup_start_ndx = 0
    sup_end_ndx = 1
    addLinks(sup_start_ndx, sup_end_ndx, adj_mat, agents)
    
# This function adds links between retailers and distribution centers. It assumes 6 agents with 0,1 as suppliers, 2,3 as distribution centers, and 4,5 as retailers.
def linkRetailers(adj_mat, agents):
    ret_start_ndx = 2
    ret_end_ndx = 3
    addLinks(ret_start_ndx, ret_end_ndx, adj_mat, agents)

def buildNetwork(adj_mat, agents):
    linkSuppliers(adj_mat, agents)
    linkRetailers(adj_mat, agents)
    print(agents[2].customers)
    print(agents[2].suppliers)
    
def main():
    agents = initializeAgents()
    network = buildNetwork(A_4, agents)
    runNetwork1()
    
    
if __name__ == '__main__':
    main()
