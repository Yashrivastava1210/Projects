---------------------
CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Installation
 * Organization
 * Maintainers

INTRODUCTION
------------

The application is an implementation of concepts of map reduce which supports two
applications "Word Count" and "Inverted Index". The word count application gives the
count of all words in a file and saves the result in an output location provided
by the user. The inverted index application gives the mapping from content, to its
location in the document. For full description please see report.pdf.

REQUIREMENTS
------------

This module requires python3 to be installed in the system to be able to run the client and server.
There are no configurations or libraries required apart from the basic python 3 packages.

INSTALLATION
------------

To install python3 in a linux based environment run the below command on the terminal.

	* sudo apt-get install python3.8

ORGANIZATION
------------

>Data
	-<holds all Input files>.txt
>src
	- Master.py
	- MapReduce.py
	- ConfigFile.py
>tests
	- client_inverted_index.py
	- client_word_count.py
	- multiple_clients.py
>logs
	-<holds sample Log files>.log
>readme.txt
>Report.pdf
>start_server.sh
>run_tests.sh

MAINTAINERS
-----------

Current maintainer:
 * Yash Shrivastava (yashriva) - yashriva@iu.edu
