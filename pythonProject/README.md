In main.py click on run then follow the prompts in the terminal to run.

F.  Justify the package delivery algorithm used in the solution as written in the original program by doing the following:

1.  Describe two or more strengths of the algorithm used in the solution.
        The algorithm I ended up using was the nearest neighbor algorithm. Some strengths of this algorithm are:
            1) The NN algorithm is very fast for small datasets such as this one but if the data set grows we are able to easily expand this into the KNN algorithm.
            2) For my own sanity I used the NN algorithm as it is pretty simple to implement.
            3) This algorithm doesn't make any assumptions about the data meaning that we will always be going to the nearest neighbor not *roughly* the nearest neighbor

2.  Verify that the algorithm used in the solution meets all requirements in the scenario.
    I have verified that the algorithm I used meets all requirements for this project and I have tested every lookup function myself.

3.  Identify two other named algorithms that are different from the algorithm implemented in the solution and would meet all requirements in the scenario.
    1) Christofides' Algorithm: An approximation algorithm for the TSP, it provides solutions within a factor of 1.5 of the optimal solution. It can be used for routing and delivery optimization where exact solutions are not feasible. If this project had a massive massive dataset this would be a good option
    2) Dijkstra's Algorithm: Used to find the shortest path between nodes in a graph, Dijkstra's algorithm is applicable for optimizing delivery routes with known distances.
    
a.  Describe how both algorithms identified in part F3 are different from the algorithm used in the solution.
    1) Christofides' Algorithm is an approximation algorithm that is much much more complex than the NN. It will construct a minimum spanning tree from the graph and that find a min-weight perfect matching for odd-degree verticies and will combine them into a Eulerian circut
    2) Dijkstra's Algorithm is designed to find the shortest path from a source node to all other nodes in a weighted graph with non-negative edge weights. It's used in routing, pathfinding, and network analysis. Dijkstra's Algorithm is designed to find the shortest path overall, rather than the shortest path to the next location, ensuring optimal solutions for single-source pathfinding in graphs with non-negative edge weights.

G.
    If I did this project all over again I would  spend more time in the planning stages of development and I would write down a lot of my psudocode on pen and paper before translating it into the project. This is also the first project I have ever done in python so I feel like my naming conventions using the underline format compared to Java's standard nameLikeThis format are still very weird to me when referencing parts of the code. I would also test way more periodically than I did this time. Throughout the program you will see some of the lines I used for testing and that could mostly been avoided had I planned more thouroughly and did smaller tests more often. 

H. The datastructure I created verifies all the requirements.
    1. I could have also tried using lists of tuples and sets instead of the hashmap that I created.
        a. I could have structured the datastructure to be a list of key-value tuples to simulate hashmap like behavior. The access time would be O(n) compared to a hashmaps O(1). A list of tuples wouldnt be able to perform direct indexing it would have to iterate through the list, checking each tuple, which is very inefficient for large data sets unlike this one.
        a. Sets are pretty different from hashmaps as they are an unordered collection of unique elements (which in our case would be package ID). Sets are typically used when you need a collection of unique elements or to check for the presence of items where as a hashmap is used when you need to associate keys with values.
        a. Overall, I do not see why, for this data set of 40 packages, I would want to NOT use a hashmap however the above two data structure are reasonable alternatives that would be harder to implement but could work. 


Below are the sources I used to prepare myself for the project:

Joe James. "Python: Creating a HASHMAP using Lists” YouTube, uploaded by Oggi AI, 22 Jan 2016, https://www.youtube.com/watch?v=9HFbhPscPU0.
Zyante. zyBook: WGUC950Template2023. Chapter 6, Section 1, zyBooks, 2023, https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/6/section/1.
Mosh. "Python Tutorial - Python Full Course for Beginners" YouTube, uploaded by Programming with Mosh, 18 Feb 2019, https://www.youtube.com/watch?v=_uQrJ0TkZlc
Mosh. "Data Structures and Algorithms for Beginners" YouTube, uploaded by Programming with Most, 10 Dec 2019, https://www.youtube.com/watch?v=BBpAmxU_NQo