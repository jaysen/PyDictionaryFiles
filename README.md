pyDictionaryFiles
=================

##Description:
Reads key/value pairs to and from being embedded within
normal text files.
Leaves all non key:value text alone / preserves comments and non key:value pairs.
Processes multiple key:value formats.

by Jaysen Naidoo (2014.06.28)


##Features:
* Read key:value pairs from normal text file
* Set key:value pairs in file
* Set type of dictionary pair
** key:value
** key=value
** [key:value]


##ChangeLog:
version 0.3

* 2014.06.28: v0.3 starts with fixes:
    - leaves comments and non key pairs alone.
    - only replaces a line if it contains a keypair and the value has changed
* 2006.08.21: fixed update - to properly update the file when a keyword is changed

##Todo List:
* TODO: Handle Key:Values in the following formats:
        - [key:value]
        - [key=value]
* TODO: handle multi-line key:value pairs (?)
* TODO: Allow the reading of multiple key:value formats
* TODO: change dictionary to component instead of parent (?)