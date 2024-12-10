# Differences from CST-JAVA

CST-Python is a port of the CST-Java to Python. However, the intention is only to port the existing elements in cst.core and the Ideas functionalities, to enable the creation of basic CST applications for prototyping and interaction with other architectures in Java.

At this time, the following elements are not implemented:
- Coalition
- CodeRack
- CodeletContainer
- MemoryBuffer
- MemoryContainer
- REST functionalities
- Ideas functionalities

Other differences between the versions:
- All get and set methods have been replaced by properties with the name of the attribute you want to access, except in the case of methods coming from interfaces and abstract classes and their implementations.
- Interfaces have been converted to abstract classes.
- Synchronization features have not been implemented, as the GIL prevents most of these issues from occurring.