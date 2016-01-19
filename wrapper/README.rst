==========================
Nguyen Quang "TechBK" Binh
==========================

.. contents::


Usage
=====
::

    chmod +x service.py
    ./service.py -i 0.0.0.0 -p 8080
    or
    ./service.py --ip=0.0.0.0 --port=8080

Note: Hien tai chua dung nhung option nay!!!

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
::

    {"job_done": true,
    "status": true,
    "process_out": "\n\n\n CLUSTAL 2.1 Multiple Sequence Alignments\n\n\nSequence type explicitly set to Protein\nSequence format is Pearson\nSequence 1: WD0001      1380 aa\nSequence 2: wRi         1380 aa\nSequence 3: wPip        1380 aa\nSequence 4: wBm         1380 aa\nStart of Pairwise alignments\nAligning...\n\nSequences (1:2) Aligned. Score:  99\nSequences (1:3) Aligned. Score:  91\nSequences (1:4) Aligned. Score:  88\nSequences (2:3) Aligned. Score:  91\nSequences (2:4) Aligned. Score:  88\nSequences (3:4) Aligned. Score:  87\nGuide tree file created:   [1/test.dnd]\n\nThere are 3 groups\nStart of Multiple Alignment\n\nAligning...\nGroup 1: Sequences:   2      Score:35945\nGroup 2: Sequences:   3      Score:34466\nGroup 3: Sequences:   4      Score:33810\nAlignment Score 47431\n\nCLUSTAL-Alignment file created  [1/result.out]\n\n",
    "job_error": false,
    "job_id": "1"}


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
    $ sudo pip3 install python-keystoneclient


Practice
========

1. Khong can phai @asyncio.coroutine cac ham trong class SwiftManager: Vi chi can cac method handle @asyncio.coroutine
la du


Docker Images
=============
Build docker images::

    sudo docker build -t techbk/bio-wrapper:clustalw-0.0.2 .
    sudo docker login ....
    sudo docker push techbk/bio-wrapper:clustalw-0.0.2

Bio-wrapper images is available at https://hub.docker.com/r/techbk/bio-wrapper/

Install:
::

    docker pull techbk/bio-wrapper:0.0.5


Run Test
========
Clustalw
--------
Commandline test::

    clustalw -infile={input_file[0]} -type=protein -matrix=pam -outfile={output_file} -outorder=input
    -> clustalw -infile=47.1.data.fasta -type=protein -matrix=pam -outfile=aa.align.out -outorder=input

- Step0: Run techbk/bio-wrapper:clustalw-0.0.1 images::

    sudo docker run -it -p 0.0.0.0:8080:8080 techbk/bio-wrapper:clustalw-0.0.2

- Step1: Create container name: clustalw
- Step2: Upload object name: test.fasta
- Step3: /runtask/ with parameter::

    user=demo
    key=password
    tenant=demo
    authurl=http://172.16.89.128:5000/v2.0/
    cm=clustalw -infile={input_file[0]} -type=protein -matrix=pam -outfile={output_file} -outorder=input
    input_file=clustalw/test.fasta
    output_file=clustalw/result.out

- Step4: kiem tra container clustalw da co file result.out chua. Neu co thi ok.