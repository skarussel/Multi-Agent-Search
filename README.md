# Multi-Agent-Search

This repository implements Min-Max with optional alpha-beta pruning for multi-agent-search. 
The program will be called with python3.9 using:

 `python3 main.py <search-type> <init-file>`

where `<search-type>` might be one of the following:
<ul>
  <li>min-max (no pruning)</li>
  <li>alpha-beta (pruning in MAX and MIN nodes)</li>
</ul>

`<n-actions>` determines the depth of the search tree. Eg. Suppose there are 3 opponent vacuum cleaners which all act optimal:
If <n-actions> is 5, the search will be as follows: MAX acts, MIN1, MIN2, MIN3 acts, MAX acts, and
the search stops, and the utility values after the second MAX action will be used. 

`<init-file>` will be a text file gives all details related to the initial environment.

An example environment can be found in [init.txt](https://github.com/skarussel/Single-Agent-Search/blob/master/init.txt).

The output of the programm is:
<ul>
 <li>the optimal action of the agent in its first move
 <li>the expected minmax value of the root node
 <li>number of calls for utility function
</ul>

## Introduction to the Environment:

The [Environment](https://github.com/skarussel/Single-Agent-Search/blob/master/init.txt) is as follows:
<ul>
  <li>The environment is NxM grid world</li>
  <li>Each grid in the environment might contain</li>
  <ul>
    <li>Vacuum cleaner (our agent)</li>
    <li>Obstacles that avoid entering to that grid. There is not dirt in the obstacle with grid</li>
    <li>Jumper” which moves the agent that moves an incoming agent to the next grid (if the next grid does not
contain an obstacle). For example, an agent coming from left to a jumper grid is transformed to the grid on the
right. An agent coming from up is transformed to the grid down.</li>
  </ul>
  <li> The vacuum cleaner have six actions:
  <ul>
    <li>left, right, up, down moves the cleaner one grid, unless that grid is an obstacle</li>
    <li>suck action that sucks one dirt</li>
    <li>stop action does nothing</li>
  </ul>
  <li>Costs of the actions:
  <ul>
  <li>Left and right: 1</li>
  <li>Up and down: 2</li>
  <li>Suck: 5</li>
</ul>
<li>Opponent vacuum cleaners, which are numbered with even digits, move randomly
<li>Opponent vacuum cleaners, which are numbered with odd digits, move optimally
</ul>


The Environment will be represented as textfile, where
<ul>
  <li>x corresponds to obstacles</li>
  <li>c corresponds to the vacuum-cleaner</li>
  <li>each digit corresponds to one of your opponents where/li>
  <ul>
  <li> even digit opponents move randomly
  <li> odd digit opponents move optimally
  </ul>
 <li>. (dot) corresponds to the dirt 
</ul>

## Utility Function

The utility value at any node is calculated as follows:
* If the vacuum cleaner is in the same grid with one of the any other opponent, utility is set to -100 and the episode ends.
* Otherwise, utility = (the number of dirts cleaned by our cleaner – the number of dirts cleaned by the opponents)

  
