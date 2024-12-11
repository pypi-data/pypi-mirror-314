-- table_volume_put.sql

--!! tmp_file file1.txt 100
--!! tmp_file sub1/1.txt 101
--!! tmp_file sub1/2.txt 102

PUT '{path_prefix}/file1.txt' TO TABLE VOLUME `{table_name}`;
-->> {path_prefix}/file1.txt,file1.txt,100

SHOW TABLE VOLUME DIRECTORY `{table_name}`;
-->> file1.txt,**/file1.txt,100,...

PUT '{path_prefix}/file1.txt' TO TABLE VOLUME `{table_name}` FILE 'data1.txt';
-->> {path_prefix}/file1.txt,data1.txt,100

SHOW TABLE VOLUME DIRECTORY `{table_name}`;
-->> data1.txt,**/data1.txt,100,...
-->> file1.txt,**/file1.txt,100,...

PUT '{path_prefix}/sub1/' TO TABLE VOLUME `{table_name}` SUBDIRECTORY 'sub1';
-->> {path_prefix}/sub1/1.txt,sub1/1.txt,101
-->> {path_prefix}/sub1/2.txt,sub1/2.txt,102

SHOW TABLE VOLUME DIRECTORY `{table_name}` LIKE '%sub1/%';
-->> sub1/1.txt,**/sub1/1.txt,101,...
-->> sub1/2.txt,**/sub1/2.txt,102,...

GET TABLE VOLUME `{table_name}` FILE 'data1.txt' TO '{path_prefix}/';
-->> data1.txt,{path_prefix}/data1.txt,100

GET TABLE VOLUME `{table_name}` SUBDIRECTORY 'sub1' TO '{path_prefix}/get/';
-->> 1.txt,{path_prefix}/get/1.txt,101
-->> 2.txt,{path_prefix}/get/2.txt,102

--!! compare_file data1.txt file1.txt
--!! compare_file get/1.txt sub1/1.txt
--!! compare_file get/2.txt sub1/2.txt
