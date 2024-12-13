
from typing import Callable
from NGPIris.hcp import HCPHandler
from configparser import ConfigParser
from pathlib import Path
from shutil import rmtree
from filecmp import cmp

hcp_h = HCPHandler("credentials/testCredentials.json")

ini_config = ConfigParser()
ini_config.read("tests/test_conf.ini")

test_bucket = ini_config.get("hcp_tests", "bucket")

test_file = ini_config.get("hcp_tests","data_test_file")
test_file_path = "tests/data/" + test_file

result_path = "tests/data/results/"

def _without_mounting(test : Callable) -> None:
    try:
        test()
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_list_buckets() -> None:
    assert hcp_h.list_buckets()

def test_mount_bucket() -> None:
    hcp_h.mount_bucket(test_bucket)

def test_mount_nonexisting_bucket() -> None:
    try:
        hcp_h.mount_bucket("aBucketThatDoesNotExist")
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_test_connection() -> None:
    test_mount_bucket()
    hcp_h.test_connection()

def test_test_connection_with_bucket_name() -> None:
    hcp_h.test_connection(bucket_name = test_bucket)

def test_test_connection_without_mounting_bucket() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    try:
        _hcp_h.test_connection()
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_list_objects() -> None:
    test_mount_bucket()
    assert type(list(hcp_h.list_objects())) == list

def test_list_objects_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.list_objects)

def test_upload_file() -> None:
    test_mount_bucket()
    hcp_h.upload_file(test_file_path)

def test_upload_file_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.upload_file)

def test_upload_file_in_sub_directory() -> None:
    test_mount_bucket()
    hcp_h.upload_file(test_file_path, "a_sub_directory/a_file")

def test_upload_nonexistent_file() -> None:
    test_mount_bucket()
    try: 
        hcp_h.upload_file("tests/data/aTestFileThatDoesNotExist")
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_upload_folder() -> None:
    test_mount_bucket()
    hcp_h.upload_folder("tests/data/a folder of data/", "a folder of data/")

def test_upload_folder_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.upload_folder)

def test_upload_nonexisting_folder() -> None:
    test_mount_bucket()
    try: 
        hcp_h.upload_folder("tests/data/aFolderOfFilesThatDoesNotExist")
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_get_file() -> None:
    test_mount_bucket()
    assert hcp_h.object_exists("a_sub_directory/a_file")
    assert hcp_h.get_object("a_sub_directory/a_file")

def test_get_folder_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.object_exists)
    _without_mounting(_hcp_h.get_object)

def test_get_file_in_sub_directory() -> None:
    test_mount_bucket()
    assert hcp_h.object_exists(test_file)
    assert hcp_h.get_object(test_file)

def test_download_file() -> None:
    test_mount_bucket()
    Path(result_path).mkdir()
    hcp_h.download_file(test_file, result_path + test_file)
    assert cmp(result_path + test_file, test_file_path)

def test_download_file_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.download_file)

def test_download_nonexistent_file() -> None:
    test_mount_bucket()
    try:
        hcp_h.download_file("aFileThatDoesNotExist", result_path + "aFileThatDoesNotExist")
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_download_folder() -> None:
    test_mount_bucket()
    hcp_h.download_folder("a folder of data/", result_path)

def test_search_objects_in_bucket() -> None:
    test_mount_bucket()
    hcp_h.search_objects_in_bucket(test_file)

def test_search_objects_in_bucket_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.search_objects_in_bucket)

def test_get_object_acl() -> None:
    test_mount_bucket()
    hcp_h.get_object_acl(test_file)

def test_get_object_acl_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.get_object_acl)

def test_get_bucket_acl() -> None:
    test_mount_bucket()
    hcp_h.get_bucket_acl()

def test_get_bucket_acl_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.get_bucket_acl)

#def test_modify_single_object_acl() -> None:
#    test_mount_bucket()
#    hcp_h.modify_single_object_acl()
#
#def test_modify_single_bucket_acl() -> None:
#    test_mount_bucket()
#    hcp_h.modify_single_bucket_acl()
#
#def test_modify_object_acl() -> None:
#    test_mount_bucket()
#    hcp_h.modify_object_acl()
#
#def test_modify_bucket_acl() -> None:
#    test_mount_bucket()
#    hcp_h.modify_bucket_acl()

def test_delete_file() -> None:
    test_mount_bucket()
    hcp_h.delete_object(test_file)
    hcp_h.delete_object("a_sub_directory/a_file")
    hcp_h.delete_object("a_sub_directory")

def test_delete_file_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.delete_object)

def test_delete_folder_with_sub_directory() -> None:
    test_mount_bucket()
    hcp_h.upload_file(test_file_path, "a folder of data/a sub dir/a file")
    try:
        hcp_h.delete_folder("a folder of data/")
    except: 
        assert True
    else: # pragma: no cover 
        assert False
    hcp_h.delete_folder("a folder of data/a sub dir/")

def test_delete_folder() -> None:
    test_mount_bucket()
    hcp_h.delete_folder("a folder of data/")

def test_delete_folder_without_mounting() -> None:
    _hcp_h = HCPHandler("credentials/testCredentials.json")
    _without_mounting(_hcp_h.delete_folder)

def test_delete_nonexistent_files() -> None:
    hcp_h.delete_objects(["some", "files", "that", "does", "not", "exist"])

def test_clean_up() -> None:
    rmtree(result_path)