## Start RDFox
Start RDFox in a terminal using the following command, replacing [your path to RDFox executable] with the actual path to your RDFox executable:

```
$ [your path to RDFox executable] sandbox . start.rdfox
``` 
The "start.rdfox" file contains commands to import the ontology, flight plan data (currently, there is only one flight plan), and the rule that calculates the distance.

## Visualise the flight plan data in RDFox console
1. In the console, copy the query below, paste it into the query window, and click “Run”. You should see “:flightplan001” being returned as shown in the following screenshot.

    `SELECT ?S WHERE {?S a :FlightPlan}`
    ![Screenshot-01](/screenshot-01.png)

1. There is an icon next to `:flightplan001`, ![Screenshot-02](/screenshot-02.png). Click on it to explore the results.

1. Once you click on the icon, you will be taken to the exploration interface, as shown in the following screenshot.
    ![Screenshot-03](/screenshot-03.png)

1. Right- click on the `flightplan001` node and a small window will display the edges its incoming and outgoing edges (if any). You can check the “All” option in the top right corner and then click “Update” at the bottom.
    ![Screenshot-04](/screenshot-04.png)

1. All nodes and edges that connected to `:flightplan001` will be displayed as the following screenshot:
    ![Screenshot-05](/screenshot-05.png)

1. You can perform the same action for any node in the graph to expand it even further.

## Simulate data points
1. In another terminal, run the Python file main.py with the function `create_trajectory_graph`.
1. This will generate the data points and send them one by one to RDFox.
1. After that, you can run the query below to check all the instances of data points that have been added to RDFox:
    `SELECT ?S WHERE {?S a :DataPoint}`

1. You can visualize the results in the same way as described above. If you expand any instance of `:DataPoint`, you should see the results from the distance calculation, as shown in the following screenshot.
    ![Screenshot-06](/screenshot-06.png)
