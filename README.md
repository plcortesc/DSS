# Distributed-Storage-System (GAE)

APP

You can find the application deployed on:
http://cs553ape.appspot.com
Its use is trivial and it is briefly explained in the same web site. 

PERFORMANCE

How to run the runtest from command line:
First of all the half of the whole experimets requires memcache that has to be modified in the source code. Exactly in "main.py", that there is a flag called MEMCACHE that can be true or false depending on if it is used or not memcache.
Once the application has been uploaded it is too easy to carry out the benchmarking stated in this assignment with the class “benchmark.py” that is run like follows:

$ python benchmark.py “operation(insert,find or remove)” “number of threads”

It is necessary to take into account that there must be a folder in the same directory of the benchmark.py named “files” that will contain the files used. This files are generated with the file generator that is explained after that.

FILE GENERATOR

There is a folder called Generation. Inside the folder src/com/gen/ you can find the java file for creating the files.
To compile and run just type, in the folder where it is the code:

$ javac GenerateFile.java java GenerateFile

When executing, it will ask you to enter the corresponding string to generate files of this size. Example: 100KB
Take into account that the files are created in this workspace, and for running the benchmark it is needed to move these files into folder performance/files/ which is in the same directory as "benchmark.py"
