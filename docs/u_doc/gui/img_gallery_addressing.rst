
Image Gallery - addressing
###############################################



.. figure:: img/subnet_scanner.png
   :scale: 25%
   :alt: ip subnet scanner
   :align: right

+-----------------------------------------------------------------------------+
| **IP Subnet Scanner**                                                       |
+=============================================================================+
|Use this for subnet(s) ip scan for bunch of subnets at at time               |
|                                                                             |
|  * **inputs:** list of subnets;                                             |
|    output folder: output result path;                                       |
|    [n]: to ping only first n number of ips only from all provided subnets;  |
|    Concurrent connections: alter based on pc and network performace/ability;|
|    checkbox: to create separate tab for each individual subnet or to club   |
|  * **output:** Excel output file with ping results                          |
+-----------------------------------------------------------------------------+

----

.. figure:: img/subnet_scan_compare.png
   :scale: 25%
   :alt: ip subnet scan result comparator
   :align: left

+-----------------------------------------------------------------------------+
| **IP Subnet scan comparator**                                               |
+=============================================================================+
| Use this to quickly compare and see differences between two ip scanner      |
| outputs                                                                     |
| Note: differences will be displayed on screen and on console                |
|                                                                             |
|  * **input:** two ip scanner output excel files                             |
|  * **output:** differences on screen/console                                |
+-----------------------------------------------------------------------------+

----


.. figure:: img/create_ping_batch.png
   :scale: 25%
   :alt: make batch file for ping ips
   :align: right

+-----------------------------------------------------------------------------+
| **Create Ping batch script file**                                           |
+=============================================================================+
| Want to keep a continuous ping for list of ip addresses?                    |
| This section will help you preparing an execuatable batch file for that     |
| Note: if any existing batch found with same name, it will be overwrite      |
|                                                                             |
|  * **input:** List of prefixes: from which ips requires to be ping          |
|    Prefix List names: provide this to identify which prefix belongs to what |
|    IP(s): list of n-th ips to be include from each prefix provided          |
|    output folder: where resulted batch file is to be created                |
|  * **input:** List of prefixes from which ips requires to be ping           |
|  * **output:** result batch file(s)                                         |
+-----------------------------------------------------------------------------+

----


.. figure:: img/create_summaries.png
   :scale: 25%
   :alt: create summaries
   :align: left

+-----------------------------------------------------------------------------+
| **Create Summaries**                                                        |
+=============================================================================+
|Want to create summaries for the list of prefixes?                           |
|This is perfect spot for you.                                                |
|                                                                             |
|  * **input:** List of prefixes to be summarized                             |
|  * **output:** summaries of provided prefixes                               |
|                                                                             |
+-----------------------------------------------------------------------------+

----


.. figure:: img/break_prefix.png
   :scale: 25%
   :alt: break prefix
   :align: right

+-----------------------------------------------------------------------------+
| **Break the prefix**                                                        |
+=============================================================================+
|Want to split the subnet in to multiple pieces?                              |
|This is what you are looking for.                                            |
|                                                                             |
|  * **input:** a Subnet/Supernet to be broken in to                          |
|    /n: number of pieces to be broken subnet in to                           |
|    - n will be considered to the power of 2                                 |
|  * **output:** list of broken subnets                                       |
+-----------------------------------------------------------------------------+

----


.. figure:: img/isSubset.png
   :scale: 25%
   :alt: check is subset of
   :align: left

+-----------------------------------------------------------------------------+
| **isSubset**                                                                |
+=============================================================================+
|This is to check, if a subnet is part of another subnet or not               |
|Result will be boolean - Yes/No                                              |
|                                                                             |
|  * **input:** Two prefixes, (one subnet, one supernet)                      |
|  * **output:** Yes/No                                                       |
|                                                                             |
+-----------------------------------------------------------------------------+

