# Here's the idea:

###  We have the master server here created first
| MASTER |

This runs on its own server and will store metadata about each worker server created.

### Then we create worker servers
 MASTER
  
| | |

W1 W2 W3 

Each worker acts indepedently of each other, the load of requests is balanced between each. Each is on its own server again.


