# test cua dai
import requests

cm = "clustalw -infile=\\{input_file[0]\\} -type=protein -matrix=pam -outfile=\\{output_file\\} -outorder=input"
data = {'user':'admin',
	'key':'vandai123',
	'tenant':'admin',
	'authurl':'http://192.168.100.11:5000/v2.0',
	'cm':cm,
	'input_file':'clustalw/test.fasta',
	'output_file':'clustalw/result.out'}

a = requests.post('http://172.17.0.1:8080/runtask/', data=data)
#a = requests.post('https://www.google.com/search', data={'q':'dola', 'gws_rd':'ssl'})
print a.text