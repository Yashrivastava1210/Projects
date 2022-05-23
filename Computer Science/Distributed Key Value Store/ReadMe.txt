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

The application is an implementation of a distributed KV store which uses multiple consistency models to demonstrate and implement these concepts. The main consistency models are:

> Eventual Consistency
> Sequential Consistency
> Linearizability

For full description please see report.pdf.

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

>Database1
	-<key_values_for_server_1>*.json
	-<key_values_for_server_2>*.json
>servers
	- server1-impl.py
	- server2-impl.py
	- ConfigFile.py
>tests
	- eventual_consistency_test.py
	- linear_client1.py
	- linear_client2.py
	- sequential_client1.py
	- sequential_client2.py
	- linear1.py
	- linear2.py
	- linear3.py

>readme.txt
>Report Distributed KV Store.pdf
>start_servers.sh
>start_eventual_test.sh
>start_sequential_test.sh
>start_linear_test.sh

MAINTAINERS
-----------

Current maintainer:
 * Yash Shrivastava (yashriva) - yashriva@iu.edu
