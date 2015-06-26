This is a python multithreaded log shipper which monitors one input, at this moment, either a file or a network port,
and passes it to one or more outputs, optionally converting the data to a custom format. py_shipper is also easily 
extensible, which means new types of input, outputs and filters/converters can be added easily. py_shipper can handle multiple sets of input, filter and output as well. The sets of input output and filter can be specified in the
'config.json' file, along with parameters such as the filename or specific port number. 
  Internally, the code forks for each set of input, filter and output, and within each process, there are seperate 
threads created for handling and monitoring the input, converting the data and seperate threads for each output type specified. Each output thread has an observer object that observes an observanle object to which the filter can publish data. This ensures that all output threads are notified of any data that the filter gives it after accepting and processing the input it got from the input_to_filter queue. 

