# Code Author: Tumisang Ramarea
# Project co-Author: Kyriakos Lotidis
# Spring 2021
# EE 384S: Performance Engineering of Computer Networks
# Final Project
# Implementation of the Supply Chain Agent Model by Tan, Li, & Cai (2015)

import numpy as np
import agent
import pandas as pd

# LEGEND
# NFU: Note for Future Update

# BUGS AND OUTSTANDING WORK
# 1. All the bugs are from the Agent Class.
# 2. Still need to write a few functions to extract the metrics data frames at the end the simulations and compare the performance of the different topologies under the various risk scenarios. Basically confirm the findings of the SC paper we are basing this off.
# 3. Compare the performance with the effect of the deltas. 


# SIMULATION PARAMETERS FOR THE DIFFERENT RISK SCENARIOS
DLSL_DR = 100 # demand rate for the low demand risk low supply risk scenario
DLSL_SR = 100 # supply rate for the low demand risk low supply risk scenario
DHSL_DR = np.random.normal(loc = 100, scale = np.sqrt(50))# demand rate for the high demand risk low supply risk scenario
DHSL_SR = 100 # supply rate for the high demand risk low supply risk scenario
DLSH_DR = 100 # demand rate for the low demand risk high supply risk scenario
DLSH_SR = np.random.normal(loc = 100, scale = np.sqrt(50)) # supply rate for the low demand risk high supply risk scenario
DHSH_DR = np.random.normal(loc = 100, scale = np.sqrt(50)) # demand rate for the high demand risk high supply risk scenario
DHSH_SR = np.random.normal(loc = 100, scale = np.sqrt(50)) # supply rate for the high demand risk high supply risk scenario
env_DLSL = [DLSL_DR, DLSL_SR] # low demand and low supply risk scenario
env_DHSL = [DHSL_DR, DHSL_SR] # high demand and low supply risk scenario
env_DLSH = [DLSH_DR, DLSH_SR] # low demand and high supply risk scenario
env_DHSH = [DHSH_DR, DHSH_SR] # high demand and high supply risk scenario
SIMULATION_DURATION = 100 # in days

# ADJACENCY MATRICES

# Efficient Strategy Configuration
A_1 = np.array([
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0],
     [1, 0, 0, 0, 1, 0],
     [0, 1, 0, 0, 0, 1],
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0]
])

# Responsive Strategy Configuration
A_2 = np.array([
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0],
     [1, 0, 0, 0, 1, 1],
     [0, 1, 0, 0, 1, 1],
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0]
])

# Risk-Hedging Strategy Configuration
A_3 = np.array([
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0],
     [1, 1, 0, 0, 1, 0],
     [1, 1, 0, 0, 0, 1],
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0]
])

# Agile Strategy Configuration
A_4 = np.array([
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0],
     [1, 1, 0, 0, 1, 1],
     [1, 1, 0, 0, 1, 1],
     [0, 0, 1, 1, 0, 0],
     [0, 0, 1, 1, 0, 0]
])

# This function creates the notes in our supply chain network. We keep things simple (but not simplistic) by having 2 agents for each of the supplier, distribution center, and retailer types.
def initializeAgents():
    s1 = agent.Agent("S1")
    s2 = agent.Agent("S2")
    d1 = agent.Agent("D1")
    d2 = agent.Agent("D2")
    r1 = agent.Agent("R1")
    r2 = agent.Agent("R2")
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

# This wrapper functions adds links between the nodes in our supply chain network.
def buildNetwork(adj_mat, agents):
    linkSuppliers(adj_mat, agents)
    linkRetailers(adj_mat, agents)

# This function updates the demand and supply rates depending on the scenario we are in.
def updateScenaRates(agents, environment):
    for agent in agents:
        agent.env_dr = environment[0]
        agent.env_sr = environment[1]

# This function runs the simulation from start to finish for some specified number of time periods. It does this for a given risk scenario on a specified configuration of the supply chain network.
def runScenarios(agents,environment):
    updateScenaRates(agents,environment)
    time = 0
    while time < SIMULATION_DURATION:
        for agent in agents:
            agent.receiveOrder()
            agent.receiveNewShipment()
            agent.processQueuedOrders()
            agent.inventoryCheck()
            agent.updateMetrics()
        time += 1

# For a fixed topology of the supply chain, this function runs the simulation across the different risk scenarios.
def runNetwork(adj_mat):
    agents = initializeAgents()
    buildNetwork(adj_mat, agents)
    runScenarios(agents, env_DLSL) # Run the DLSL scenario
    runScenarios(agents, env_DHSL) # Run the DHSL scenario
    runScenarios(agents, env_DLSH) # Run the DLSH scenario
    runScenarios(agents, env_DHSH) # Run the DHSH scenario
    print(agents[0].metrics)
    print(agents[0].current_time)
    print(agents[0].filled_orders)
    print(agents[0].discarded_orders)
    
def main():
    runNetwork(A_1) # Run simulations on ES network
    runNetwork(A_2) # Run simulations on RS network
    runNetwork(A_3) # Run simulations on RH network
    runNetwork(A_4) # Run simulations on AS network
    print("I AM RUNNING SUCCESSFULLY!!!")
    
if __name__ == '__main__':
    main()
