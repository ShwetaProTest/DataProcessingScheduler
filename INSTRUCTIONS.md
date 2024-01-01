# zeroG Python Coding Exercise

In this exercise you are playing the role of an engineer in zeroG. You have been given
this prototype library and asked to improve it by adding some new features.

The Python library in this exercise, and its test suite, are deliberately badly written.
Part of the exercise is to improve the overall code quality, paying attention to 
readability, maintainability, performance and security. 


# What the library does

The `schedule_data_processing` library connects to an Azure Blob Storage container and
downloads three files containing simplified schedule data for a fictitious airline
called zeroG Airlines (ZG).

It has two modes, depending on the parameters passed. 

In `lookup` mode it prints a string to the console containing information for a single flight.

In `merge` mode it joins together all three input files and outputs the result in CSV format.


# Your tasks

 1. Add the attribute "distance_nm", the distance flown in nautical miles, to the outputs from 
    both `lookup` and `merge` modes. Hint: The GeoPy library may be useful for this.
 2. In `lookup` mode the feature to look up multiple flights (see the README.md) has stopped
    working. Provide a fix for this.
 3. Make it so that when a flight is not found in `lookup` mode, the application prints
    a valid JSON string with one attribute, "error", and a suitable error message.
 4. Append a message to a log file, "log.txt", and log the success or failure of every
    request to the application as well as the content of any responses generated.
 5. Refactor the code and its tests to improve readability, maintainability and performance,
    and make any other changes you think would be appropriate. 

# How to send us your work

Please send us a zip file of the entire repository folder (including git history) containing
your amended code.

This exercise is confidential and copyright (c) zeroG GmbH 2021. 
Please do not share this exercise or your solution to it with anyone except your interviewers.