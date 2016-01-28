# test cua dai
import requests
import json
# cm = "clustalw -infile=\\{input_file[0]\\} -type=protein -matrix=pam -outfile=\\{output_file\\} -outorder=input"
cm = "clustalw -infile={input_file[0]} -type=protein -matrix=pam -outfile={output_file} -outorder=input"
# print(cm)
# data = {'user': 'demo',
#         'key': 'baogavn',
#         'tenant': 'demo',
#         'authurl': 'http://172.16.89.128:5000/v2.0/',
#         'cm': cm,
#         'input_file': 'clustalw/test.fasta',
#         'output_file': 'clustalw/result.out'}
#
# a = requests.post('http://172.17.0.1:8080/runtask/', data=data)
# # a = requests.post('https://www.google.com/search', data={'q':'dola', 'gws_rd':'ssl'})
# print(a.text)

# b = requests.get("http://172.17.0.1:8080/job/", params={"job_id": json.loads(a.text)['job_id']})
b = requests.get("http://172.17.0.1:8080/job/", params={"job_id": 1})
print(b.text)
