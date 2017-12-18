import unittest
from util import *
import os

FILE_SIZE = 1024 * 1024


class ResetEnv(unittest.TestCase):
    def test_delete_all_rules(self):
        """
        delete all rules
        """
        rules = list_rule()
        for rule in rules:
            # Delete all rules
            if rule['state'] != 'DELETED':
                delete_rule(rule['id'])
        rules = [r for rule in list_rule() if rule['state'] != 'DELETED']
        self.assertTrue(len(rules) == 0)

    # def test_delete_all_actions(self):
    #     """
    #     delete all actions, currently not supported
    #     """
    #     pass

    def test_delete_all_files(self):
        try:
            subprocess.call("hdfs dfs -rm " + TEST_DIR + "*", shell=True)
        except OSError:
            print "HDFS Envs is not configured!"

    def test_create_1M_DFSIO(self):
        """
        Using DFSIO to generte 10M files.
        Each time generate 100K * 2 files (100K io_data and 100K io_control)
        """
        dir_number = 50
        dfsio_cmd = "hadoop jar /usr/lib/hadoop-mapreduce/hadoop-" + \
            "mapreduce-client-jobclient-*-tests.jar TestDFSIO " + \
            "-write -nrFiles 10000 -fileSize 0KB"
        for i in range(dir_number):
            subprocess.call(dfsio_cmd)
            subprocess.call("hdfs dfs -mv /benchmarks/TestDFSIO/io_control " +
                      TEST_DIR + str(i) + "_control")
            subprocess.call("hdfs dfs -mv /benchmarks/TestDFSIO/io_data " +
                      TEST_DIR + str(i) + "_data")

    def test_create_10M_DFSIO(self):
        """
        Using DFSIO to generte 10M files.
        Each time generate 100K * 2 files (100K io_data and 100K io_control)
        """
        dir_number = 500
        dfsio_cmd = "hadoop jar /usr/lib/hadoop-mapreduce/hadoop-" + \
            "mapreduce-client-jobclient-*-tests.jar TestDFSIO " + \
            "-write -nrFiles 10000 -fileSize 0KB"
        for i in range(dir_number):
            subprocess.call(dfsio_cmd)
            subprocess.call("hdfs dfs -mv /benchmarks/TestDFSIO/io_control " +
                      TEST_DIR + str(i) + "_control")
            subprocess.call("hdfs dfs -mv /benchmarks/TestDFSIO/io_data " +
                      TEST_DIR + str(i) + "_data")

    def test_create_100M_0KB(self):
        """
        Create 100M=500K * 200 files in /ssmtest/.
        Files will be kept in dir named from 1 to 200.
        Files are named from 0-499999.
        """
        max_number = 500000
        dir_number = 200
        for i in range(dir_number):
            cids = []
            dir_name = TEST_DIR + str(i)
            # 200 dirs
            for j in range(max_number):
                # each has 500K files
                cid = create_file(dir_name + "/" + str(j), 0)
            cids.append(cid)
            wait_for_cmdlets(cids)

    def test_create_500K_0KB(self):
        """
        Create 500K files in /ssmtest/.
        All files will be kept in one dir with random name.
        Files are named from 0-499999.
        """
        max_number = 500000
        cids = []
        dir_name = TEST_DIR + random_string()
        for i in range(max_number):
            # each has 500K files
            cid = create_file(dir_name + "/" + str(i), 0)
        cids.append(cid)
        wait_for_cmdlets(cids)

    def test_create_10000_1MB(self):
        """
        Create 10000 * 1 MB files in /1MB/
        """
        max_number = 10000
        file_paths = []
        cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel("/1MB/", FILE_SIZE)
            file_paths.append(file_path)
            cids.append(cid)
        wait_for_cmdlets(cids)

    def test_create_10000_10MB(self):
        """
        Create 10000 * 10 MB files in /10MB/
        """
        max_number = 10000
        file_paths = []
        cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel("/10MB/", FILE_SIZE)
            file_paths.append(file_path)
            cids.append(cid)
        wait_for_cmdlets(cids)

    def test_create_1000_100MB(self):
        """
        Create 1000 * 100 MB files in /100MB/
        """
        max_number = 1000
        file_paths = []
        cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel("/100MB/", FILE_SIZE)
            file_paths.append(file_path)
            cids.append(cid)
        wait_for_cmdlets(cids)

    def test_create_files_10000(self):
        """
        Create 10000 * 1 MB files in /ssmtest/
        """
        max_number = 10000
        file_paths = []
        cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel(FILE_SIZE)
            file_paths.append(file_path)
            cids.append(cid)
        wait_for_cmdlets(cids)

    def test_create_files_1000(self):
        """
        Create 1000 * 1 MB files  in /ssmtest/
        """
        max_number = 10000
        file_paths = []
        cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel(FILE_SIZE)
            file_paths.append(file_path)
            cids.append(cid)
        wait_for_cmdlets(cids)

    def test_create_files_100(self):
        """
        Create 100 * 1 MB files  in /ssmtest/
        """
        max_number = 10000
        file_paths = []
        cids = []
        for i in range(max_number):
            # 1 MB files
            file_path, cid = create_random_file_parallel(FILE_SIZE)
            file_paths.append(file_path)
            cids.append(cid)
        wait_for_cmdlets(cids)


if __name__ == '__main__':
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    unittest.main()
