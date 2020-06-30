# beginnerReinforcmentLearning
Simple projects to help me understand Reinforcement Learning

          
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
            
           
