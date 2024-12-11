-- external_volume_put.sql

--!! tmp_file file1.txt 100
--!! tmp_file sub1/1.txt 101
--!! tmp_file sub1/2.txt 102

PUT '{path_prefix}/file1.txt' to VOLUME `{volume_name}`;
-->> {path_prefix}/file1.txt,file1.txt,100

SHOW VOLUME DIRECTORY `{volume_name}`;
-->> file1.txt,{volume_location}/file1.txt,100,...

PUT '{path_prefix}/file1.txt' to VOLUME `{volume_name}` FILE 'data1.txt';
-->> {path_prefix}/file1.txt,data1.txt,100

SHOW VOLUME DIRECTORY `{volume_name}`;
-->> data1.txt,{volume_location}/data1.txt,100,...
-->> file1.txt,{volume_location}/file1.txt,100,...

PUT '{path_prefix}/sub1/' to VOLUME `{volume_name}` SUBDIRECTORY 'sub1';
-->> {path_prefix}/sub1/1.txt,sub1/1.txt,101
-->> {path_prefix}/sub1/2.txt,sub1/2.txt,102

SHOW VOLUME DIRECTORY `{volume_name}` LIKE '%sub1/%';
-->> sub1/1.txt,{volume_location}/sub1/1.txt,101,...
-->> sub1/2.txt,{volume_location}/sub1/2.txt,102,...

GET VOLUME `{volume_name}` FILE 'data1.txt' TO '{path_prefix}/';
-->> data1.txt,{path_prefix}/data1.txt,100

GET VOLUME `{volume_name}` SUBDIRECTORY 'sub1' TO '{path_prefix}/get/';
-->> 1.txt,{path_prefix}/get/1.txt,101
-->> 2.txt,{path_prefix}/get/2.txt,102

--!! compare_file data1.txt file1.txt
--!! compare_file get/1.txt sub1/1.txt
--!! compare_file get/2.txt sub1/2.txt
