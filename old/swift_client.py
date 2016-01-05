import swiftclient # $ sudo pip3 install python-swiftclient
user = 'admin'
key = 'baogavn'
tenant = 'admin'

conn = swiftclient.client.Connection(
        user=user,
	    tenant_name=tenant,
	    auth_version='2.0',
        key=key,
        authurl='http://controller:5000/v2.0'
)

container_name = 'my-new-container'
conn.put_container(container_name)

with open('hello.txt', 'r') as hello_file:
        conn.put_object(container_name, 'hello.txt',
                                        contents= hello_file.read(),
                                        content_type='text/plain')


for container in conn.get_account()[1]:
        print container['name']


for data in conn.get_container(container_name)[1]:
        print '{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified'])

