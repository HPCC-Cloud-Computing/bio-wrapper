# Hướng dẫn cài đặt BIO
-	Cài đặt OpenStack (Requires: Horizon, Heat và Swift project)
-	Cài đặt Heat docker plugin
-	Cài đặt giao diện chạy các tools
-	Cài đặt Docker (docker-1.11.2)
-	Đóng gói docker image cho các ứng dụng tin sinh.

NOTE: các cài đặt dưới đây được thực hiện trên 1 máy chủ duy nhất với Ubuntu 16.04 server.

## Cài đặt OpenStack (Devstack)

- 	[https://docs.openstack.org/developer/devstack/](https://docs.openstack.org/developer/devstack/)
-	File local.conf


```
[[local|localrc]]


#Enable heat services
enable_service h-eng h-api h-api-cfn h-api-cw

#Enable heat plugin
enable_plugin heat https://git.openstack.org/openstack/heat

enable_service s-proxy s-object s-container s-account
SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
SWIFT_REPLICAS=1
SWIFT_DATA_DIR=$DEST/data/swift
```

## Cài đặt Heat docker plugin

- Hiện tại heat docker không còn được maintain bởi core reviewer, nên đã được đặt ở thư mục contrib của Heat project.
- Hướng dẫn cài đặt có sẵn tại: [https://github.com/openstack/heat/tree/master/contrib/heat_docker](https://github.com/openstack/heat/tree/master/contrib/heat_docker)

- Cài đặt docker-py:
	+ Chú ý, gói docker-py chứ không phải gói docker

```
sudo pip install docker-py==1.7.0
```

## Cài đặt giao diện chạy các tools

- Các bước có sẵn tại đây: [https://github.com/HPCC-Cloud-Computing/bioinformatics-dashboard/blob/master/README.md](https://github.com/HPCC-Cloud-Computing/bioinformatics-dashboard/blob/master/README.md)


- Chú ý: Thay thế đường dẫn `/usr/share/openstack-dashboard` bằng `/opt/stack/horizon` trong môi trường Devstack


- Bổ sung các ứng dụng lên giao diện bằng cách cập nhật file HTML template sau: [https://github.com/HPCC-Cloud-Computing/bioinformatics-dashboard/blob/master/bioinformatics/bioworkflow/templates/bioworkflow/index.html#L97](https://github.com/HPCC-Cloud-Computing/bioinformatics-dashboard/blob/master/bioinformatics/bioworkflow/templates/bioworkflow/index.html#L97):

```
<option value='{"image_name":"techbk/bio-wrapper:blastn-0.0.1"}'>BLASTN-0.0.1</option>
<option value='{"image_name":"techbk/bio-wrapper:clustalw-0.0.3"}'>CLUSTALW-0.0.3</option>
<option value='{"image_name":"newimage:v1"}'>New Image</option>
```

- Cấu hình lại các xác thực tại file constants.py [https://github.com/HPCC-Cloud-Computing/bioinformatics-dashboard/blob/master/bioinformatics/bioworkflow/constants.py](https://github.com/HPCC-Cloud-Computing/bioinformatics-dashboard/blob/master/bioinformatics/bioworkflow/constants.py) để kết quả của các ứng dụng tin sinh được đẩy vào các object của Swift.

## Cài đặt Docker:

- Cũng vì Heat Docker plugin không còn được maintain, do đó chúng ta phải sử dụng Docker phiên bản cũ để tương thích với Heat Docker plugin.

- Các bước cài đặt docker bản cũ như sau:
	+ B1: gỡ docker trên máy
	+ B2: Tải source code tại [https://github.com/docker/docker/releases/tag/v1.11.2](https://github.com/docker/docker/releases/tag/v1.11.2) và giải nén. Kết quả như sau

```
stack@ubuntu:~/docker$ ls
docker  docker-containerd  docker-containerd-ctr  docker-containerd-shim  docker-runc
```

+	
	+ B3: Sau đó copy các file trên vào thư mục /usr/bin/ thông qua quyền root.
	+ Thực hiện chạy docker như sau:

```
sudo docker daemon
```

## Đóng gói image cho các ứng dụng tin sinh.

- Đóng gói base image:
	+ Chứa mã nguồn chạy các tasks cho các tool tin sinh cụ thể và Swift client để đẩy kết quả lên các object của Swift.
	+ Thực hiện như việc build các image docker bình thường
	+ Việc build base image này sẽ làm giảm rất nhiều thời gian cho việc build các image cho các ứng dụng tin sinh sau này.
	+ Dockerfile của base image có sẵn tại: [https://github.com/HPCC-Cloud-Computing/bio-wrapper/blob/develop/Dockerfile](https://github.com/HPCC-Cloud-Computing/bio-wrapper/blob/develop/Dockerfile)

```
docker build -t base:v1 <thư mục chứa file Dockerfile>
```

- Đóng gói image cho ứng dụng tin sinh cụ thể:
	+ Thay thế "clustalw" bằng tên của ứng dụng cần cài đặt trong [https://github.com/HPCC-Cloud-Computing/bio-wrapper/blob/develop/Dockerfile.clustalw#L13](https://github.com/HPCC-Cloud-Computing/bio-wrapper/blob/develop/Dockerfile.clustalw#L13)
	+ Thực hiện build image và quay lại cập nhật tên của image vào giao diện quản lý (Restart serivce apache2 nếu cần).

```
docker build -t new:v1 <thư mục chứa file Dockerfile>
```

## NOTES

- Có thể tùy vào phiên bản Swift mà người triển khai cần cập nhật Swift client và mã nguồn của wrapper để tương tác với swift. Hiện tại, nhánh develop được cập nhật dành cho Swift ở bản Ocata với python-swiftclient==3.3.0
