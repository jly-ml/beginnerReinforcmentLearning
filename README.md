# beginnerReinforcmentLearning
Simple projects to help me understand Reinforcement Learning

***************************************************************************************************************************************************
NAME: RL_fattree_pathfinder.py
          PURPOSE: Followed tutorial from https://towardsdatascience.com/finding-shortest-path-using-q-learning-algorithm-1c1f39e89505
          ** EDIT 6-30-2020 Code changes **
          *[Fixed incorrect ID assignments for Fattree ]
          *[ Code formatting, and comments for further code breakdown]
          *[made walk dynamically calculated based on 'k', helped proportionately increase walks needed for larger and larger graphs ]
          *[ inserted duration timers for benchmarks and comparisons ]           
      
      I chose a well written tutorial so I could easily implement the code and then try to:
            1. See what tuning the parameters will do for its behavior
            2. Modify it for a slightly different purpose
            
          The code is structed into two main parts
            1. Create a 'K'-ary fattree, where each switch ID or server ID are uniquely numbered
            2. Use reinforcement learning to find the simplest path between two ID numbers
 ***************************************************************************************************************************************************           
          NAME: RL_fattree_graph_path_commcost
          PURPOSE: further edititing of RL_fattree_pathfinder, but with helper functions separated for easier reading
          DATE OF LAST EDIT: 07/15/2020
          
          1. input.py  (NO input variables needed)
             gets input from user for K, vm_pairs, and F(frequency) values
             calculates total communcation cost from all vm_pairs
             RETURN nothing
             
          2. get_infofattreegraph.py (k, maxServer) 
             generates fattree and converts to a 
             RETURN graph, maxV(upper bound)
             
          3. pathfinder.py (source, dest,G,maxServer,maxV,k,f)
             finds shortest path between the given (source,dest) pair from graph G via hops
             k is used to generate a more optimal walk value to make the learning process faster and accurate
             maxServer and maxV are used to create R and Q matrices
             RETURN localcost (hops * f)
              
