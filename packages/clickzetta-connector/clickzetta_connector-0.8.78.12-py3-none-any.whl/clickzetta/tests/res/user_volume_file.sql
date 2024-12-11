-- user_volume_put.sql

--!! tmp_file file1.txt 100
--!! tmp_file sub1/1.txt 101
--!! tmp_file sub1/2.txt 102

PUT '{path_prefix}/file1.txt' to USER VOLUME SUBDIRECTORY '{subdir}';
-->> {path_prefix}/file1.txt,{subdir}/file1.txt,100

SHOW USER VOLUME DIRECTORY LIKE '%{subdir}/%';
-->> {subdir}/file1.txt,**/{subdir}/file1.txt,100,...

PUT '{path_prefix}/file1.txt' to USER VOLUME FILE '{subdir}/data1.txt';
-->> {path_prefix}/file1.txt,{subdir}/data1.txt,100

SHOW USER VOLUME DIRECTORY LIKE '%{subdir}/%';
-->> {subdir}/data1.txt,**/{subdir}/data1.txt,100,...
-->> {subdir}/file1.txt,**/{subdir}/file1.txt,100,...

PUT '{path_prefix}/sub1/' to USER VOLUME SUBDIRECTORY '{subdir}/sub1';
-->> {path_prefix}/sub1/1.txt,{subdir}/sub1/1.txt,101
-->> {path_prefix}/sub1/2.txt,{subdir}/sub1/2.txt,102

SHOW USER VOLUME DIRECTORY LIKE '%{subdir}/sub1%';
-->> {subdir}/sub1/1.txt,**/{subdir}/sub1/1.txt,101,...
-->> {subdir}/sub1/2.txt,**/{subdir}/sub1/2.txt,102,...

GET USER VOLUME FILE '{subdir}/data1.txt' TO '{path_prefix}/';
-->> data1.txt,{path_prefix}/data1.txt,100

GET USER VOLUME SUBDIRECTORY '{subdir}/sub1' TO '{path_prefix}/get/';
-->> 1.txt,{path_prefix}/get/1.txt,101
-->> 2.txt,{path_prefix}/get/2.txt,102

--!! compare_file data1.txt file1.txt
--!! compare_file get/1.txt sub1/1.txt
--!! compare_file get/2.txt sub1/2.txt
