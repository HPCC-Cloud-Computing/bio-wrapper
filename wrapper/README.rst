==========================
Nguyen Quang "TechBK" Binh
==========================

.. contents::


Idea
====


API
===

The following section describes the available resources in bio-wrapper JSON API.

/runtask/
---------
Create a job.

* Supported Request Methods: POST
* Parameters:
    - user (string, required): username
    - key (string, required): password
    - tenant (string, required): tenant name
    - authurl (string, required):
    - cm (string, required): commandline shell
        + example: "blastn –db nt –query nt.fsa –out results.out"
          -> "blastn -db {input_file[0]} -query {input_file[1]} -out {output_file}"
    - input_file (string, unrequited): array input file.
        + example: "container_name/inputfilename0|inputfilename1|..."
    - output_file (string, unrequited): out put file.


Explain reponse:

* When ok:
    - status: true -> request done.
    - job_id: id of job of wrapper service.
* When fail:
    - status: false -> request unsuccess.
    - error_message: error message.

Example request:
::

    http://localhost:8080/runtask/

Example response:
::

    when ok:
    {"status": true, "job_id": "2"}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}

/job/
-----
Get statement of job.

* Supported Request Methods: GET
* Parameters:
    - job_id (string, required): id of job.

Example request:
::

    http://localhost:8080/job/

Explain reponse:

* When job done without error:
    - status: true -> request done.
    - job_id: id of job of wrapper service.
    - job_done: (true) true if job done, false if job unsuccess.
    - job_error: (false) true if job have error, false if otherwise.
    - process_out: result of commandline. (Note: ko can thiet lam)
* When job done but have error:
    - status: true -> request done.
    - job_id: id of job of wrapper service.
    - job_done: (true)
    - job_error: (true) true if job have error, false if otherwise.
    - error_message: message
* When job not done:
    - status: true -> request done.
    - job_id: id of job of wrapper service.
    - job_done: (false)
    - job_error: true if job have error, false if otherwise.

Example response:
::

    when ok:
    {"job_id": "2", "job_done": true, "error": "", "status": true, "job_error": false,
    "out": "total 56\n-rw-rw-r-- 1 techbk techbk   82 Th01  6 23:33 config.py"}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}

/listjobs/
----------
Get list of jobs.

* Supported Request Methods: GET
* Parameters: None

Example request:
::

    http://localhost:8080/listjobs/

Example response:
::

    when ok:
    {"status": true, "empty": false, "jobs": ["2", "3"]}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}


/canceljob/
-----------
Cancel job.

* Supported Request Methods: POST
* Parameters:
    - job_id (string, required): id of job.

Example request:
::

    http://localhost:8080/canceljob/

Example response:
::

    when ok and job is running:
    {"job_id": "2", "prevstatus": true, "status": true}

    when ok and job is done:
    {"job_id": "2", "prevstatus": false, "status": true}

    when fail:
    {"status": false, "error_message": "Exception: This code is wrong!!!!!!!!!!!!!!!!!!!!!!!!"}


Settup
======

SwiftClient
-----------
::

    $ sudo pip3 install python-swiftclient


Practice
========

1. Khong can phai @asyncio.coroutine cac ham trong class SwiftManager: Vi chi can cac method handle @asyncio.coroutine
la du


Docker Images
=============
Bio-wrapper images is available at https://hub.docker.com/r/techbk/bio-wrapper/

Install:
::

    docker pull techbk/bio-wrapper:0.0.5


Run Test
========

::

    blastn -db {input_file[0]} -query {input_file[1]} -out {output_file}
    blastn –db nt –query nt.fsa –out results.out



