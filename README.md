This is a python multithreaded log shipper which monitors one input, at this moment, either a file or a network port,
and passes it to one or more outputs, optionally converting the data to a custom format. py_shipper is also easily 
extensible, which means new types of input, outputs and filters/converters can be added easily. py_shipper can handle 
multiple sets of input, filter and output as well.
    The sets of input output and filter can be specified in the 'config.json' file, along with parameters such as the 
filename or specific port number.
