""" unit and integration tests """
import json
import os

import pytest

from conftest import skip_gitlab_ci

from ae.base import load_dotenvs, os_path_join, read_file  # type: ignore
from ae.cloud_storage import DigiApi, GoodriveApi, csh_api_class                # type: ignore


load_dotenvs()
tst_digi_root_folder = os.environ.get('TEST_DIGI_ROOT_FOLDER_PATH')
tst_digi_email = os.environ.get('TEST_DIGI_API_EMAIL')
tst_digi_password = os.environ.get('TEST_DIGI_API_PASSWORD')

tst_google_drive_root_id = os.environ.get('TEST_GOOGLE_DRIVE_ROOT_FOLDER_ID')

tst_source_path = 'requirements.txt'
tst_remote_root = 'tst_root_dir'
tst_remote_sub1 = 'sub_dir'
tst_remote_sub2 = 'sub_sub_dir'
tst_remote_file = 'tst.txt'
tst_remote_path = f'{tst_remote_root}/{tst_remote_sub1}/{tst_remote_sub2}/{tst_remote_file}'
tst_invalid_file_path = '/:/// invalid path :::/any_tst_file.txt'


@pytest.fixture
def digi_api_path_content():
    """ provide DigiApi instance, remote path and content of uploaded test file """
    api = DigiApi(root_folder=tst_digi_root_folder, email=tst_digi_email, password=tst_digi_password)
    assert api.error_message == ""
    remote_path = tst_remote_path

    file_path = api.deploy_file(remote_path, source_path=tst_source_path)
    assert api.error_message == ""
    assert file_path == remote_path

    content = api.deployed_file_content(remote_path)
    assert api.error_message == ""
    assert content == read_file(tst_source_path, extra_mode='b')

    yield api, remote_path, content

    api.error_message = ""
    err = api.delete_file_or_folder(tst_remote_root + '/')
    assert api.error_message == ""
    assert err == ""
    assert api.list_dir(tst_remote_path) is None
    assert api.error_message


@pytest.fixture
def drive_api_path_id_content():
    """ provide Goodrive instance, remote path and content of uploaded test file """
    api = GoodriveApi(root_folder=tst_google_drive_root_id)
    assert api.error_message == ""

    file_id = api.deploy_file(tst_remote_path, source_path=tst_source_path)
    assert api.error_message == ""
    assert file_id
    # wait because needs sometime up to 17 seconds until file/path is fully deployed
    api.wait_for_deployment_finish(tst_remote_path, file_id=file_id, verbose=True)

    content = api.deployed_file_content(tst_remote_path)
    assert api.error_message == ""
    assert content == read_file(tst_source_path, extra_mode='b')

    yield api, tst_remote_path, file_id, content

    api.error_message = ""
    err = api.delete_file_or_folder(tst_remote_root + '/', empty_trash=True)
    assert api.error_message == ""
    assert err == ""

    assert not api.folder_file_ids(tst_remote_path)[1]
    assert api.error_message


def test_import():
    """ test import to have at least one test on GitLab CI """
    assert DigiApi, GoodriveApi


def test_csh_api_class():
    assert csh_api_class('Digi') is DigiApi
    assert csh_api_class('Goodrive') is GoodriveApi


@skip_gitlab_ci
class TestDigiApi:
    def test_create_dirs_invalid_folder_name(self):
        api = DigiApi(root_folder=tst_digi_root_folder, email=tst_digi_email, password=tst_digi_password)
        ret = api._create_dirs(':invalid_folder\\name')
        assert ret

    def test_delete_file_or_folder_not_existing_error(self):
        api = DigiApi(root_folder=tst_digi_root_folder, email=tst_digi_email, password=tst_digi_password)
        assert api.delete_file_or_folder("not_existing_file_path/_not_existing_file.zyx")
        assert api.error_message

    def test_deployed_file_content(self, digi_api_path_content):
        api, remote_path, content = digi_api_path_content

        assert api.deployed_file_content(remote_path) == content

    def test_deployed_file_content_err(self, digi_api_path_content):
        api, remote_path, content = digi_api_path_content

        assert not api.deployed_file_content(os_path_join('not_existing_root', remote_path))
        assert not api.deployed_file_content(os_path_join(remote_path, 'not_existing_file.xyz'))

    def test_deploy_file_locally_not_found_error(self):
        api = DigiApi(root_folder=tst_digi_root_folder, email=tst_digi_email, password=tst_digi_password)
        not_existing_file_path = 'any_locally_non_existing_file__.xyz'
        assert api.deploy_file(not_existing_file_path) == ""
        assert not_existing_file_path in api.error_message

    def test_deploy_file_remote_path_invalid(self):
        api = DigiApi(root_folder=tst_digi_root_folder, email=tst_digi_email, password=tst_digi_password)
        assert api.deploy_file(tst_invalid_file_path, source_path=tst_source_path) == ""
        assert tst_invalid_file_path in api.error_message

        api.error_message = ""
        invalid_empty_dir_name = "/tst_root//tst_sub//tst_file.xxx"
        assert api.deploy_file(invalid_empty_dir_name, source_path=tst_source_path) == ""
        assert os.path.split(invalid_empty_dir_name)[0] in api.error_message

    def test_deploy_file_update(self, digi_api_path_content):
        api, remote_path, content = digi_api_path_content

        assert api.deploy_file(remote_path, source_path=tst_source_path) == remote_path
        assert api.error_message == ""

        assert api.list_dir(os.path.dirname(remote_path))[0] == tst_remote_file

        upd_content = api.deployed_file_content(remote_path)
        assert api.error_message == ""
        assert upd_content == content == read_file(tst_source_path, extra_mode='b')

    def test_err_msg_reset(self, digi_api_path_content):
        api, remote_path, content = digi_api_path_content
        assert not api.error_message

        api.error_message = "some error message"
        assert api.error_message

        api.error_message = ""
        assert not api.error_message

    def test_list_dir(self, digi_api_path_content):
        api, remote_path, content = digi_api_path_content

        path = tst_remote_root
        files = api.list_dir(path)
        assert len(files) == 1
        assert files[0] == tst_remote_sub1 + '/'

        path += '/' + tst_remote_sub1
        files = api.list_dir(path)
        assert len(files) == 1
        assert files[0] == tst_remote_sub2 + '/'

        path += '/' + tst_remote_sub2
        files = api.list_dir(path)
        assert len(files) == 1
        assert files[0] == tst_remote_file

        path += '/'
        files = api.list_dir(path)
        assert len(files) == 1
        assert files[0] == tst_remote_file

        assert not api.error_message

    def test_list_dir_on_my_digi_cloud_storage_root(self):
        api = DigiApi(email=tst_digi_email, password=tst_digi_password)
        files = api.list_dir('Videos')
        assert len(files) >= 7

        files_and_folders = api.list_dir('Pictures')
        assert len(files_and_folders) >= 61
        assert len([_ for _ in files_and_folders if _.endswith('/')]) >= 7

    def test_upload_create_sub_dir_in_path(self, digi_api_path_content):
        api, remote_path, content = digi_api_path_content
        assert api.deployed_file_content(remote_path) == content


@skip_gitlab_ci
class TestGoodriveApi:
    def test_create_folder(self):
        api = GoodriveApi(root_folder=tst_google_drive_root_id)
        assert api.error_message == ""
        root_dir = 'created_root_folder_tst'
        sub_dir = 'created_sub_folder_tst'

        root = {}
        try:
            root = api._create_folder(root_dir, tst_google_drive_root_id)
            assert isinstance(root, dict)
            assert root['id']
            assert root['mimeType'] == GoodriveApi.FOLDER_MIMETYPE

            sub = api._create_folder(sub_dir, root['id'])
            assert isinstance(sub, dict)
            assert sub['id']
            assert sub['mimeType'] == GoodriveApi.FOLDER_MIMETYPE

            folder_path = os.path.join(root_dir, sub_dir) + '/'
            ids, _tries, _wait = api.wait_for_deployment_finish(folder_path, verbose=True)
            assert ids[1] == sub['id']
            ids2, _tries, _wait = api.wait_for_deployment_finish(folder_path, file_id=sub['id'], verbose=True)
            assert ids2[1] == sub['id']

        finally:
            assert not root or not api.delete_file_or_folder(root_dir + '/', empty_trash=True)

    def test_cred_info_dict(self):
        cred_dict = json.loads(read_file('.service_account_credentials.json', extra_mode='b'))
        api = GoodriveApi(root_folder=tst_google_drive_root_id, sa_cred_dict=cred_dict)
        assert api.service
        assert not api.error_message

    def test_delete_file_or_folder_not_existing_error(self):
        api = GoodriveApi(root_folder=tst_google_drive_root_id)
        assert api.delete_file_or_folder("not_existing_file_path/_not_existing_file.zyx", empty_trash=True)
        assert api.error_message

    def test_deploy_file_errors(self):
        api = GoodriveApi(root_folder=tst_google_drive_root_id)
        api.deploy_file(tst_invalid_file_path, source_path=tst_source_path)
        assert tst_invalid_file_path in api.error_message

    def test_deploy_file_update(self, drive_api_path_id_content):
        api, remote_path, create_id, content = drive_api_path_id_content

        update_id = api.deploy_file(remote_path, source_path=tst_source_path)
        assert api.error_message == ""
        assert update_id == create_id
        assert api.folder_file_ids(remote_path)[1] == create_id

        upd_content = api.deployed_file_content(remote_path)
        assert api.error_message == ""
        assert upd_content == content == read_file(tst_source_path, extra_mode='b')

    def test_deployed_file_content_not_existing_error(self):
        api = GoodriveApi(root_folder=tst_google_drive_root_id)
        assert api.deployed_file_content("_not_existing_file_path/not_existing_file.zyx") is None
        assert api.error_message

    def test_err_msg_reset(self, drive_api_path_id_content):
        api, remote_path, create_id, content = drive_api_path_id_content
        assert not api.error_message

        api.error_message = "some error message"
        assert api.error_message

        api.error_message = ""
        assert not api.error_message

    def test_folder_file_ids(self, drive_api_path_id_content):
        api, remote_path, create_id, content = drive_api_path_id_content

        dir1_id, sub1_id = api.folder_file_ids('/' + tst_remote_root + '/')
        assert not api.error_message
        assert dir1_id == tst_google_drive_root_id
        assert sub1_id

        dir1_id, sub1_id = api.folder_file_ids(tst_remote_root + '/')   # path relative to root folder
        assert not api.error_message
        assert dir1_id == tst_google_drive_root_id
        assert sub1_id

        dir1_id2, sub1_id2 = api.folder_file_ids(tst_remote_root + '/', folder_id=tst_google_drive_root_id)
        assert not api.error_message
        assert dir1_id2 == tst_google_drive_root_id
        assert sub1_id2 == sub1_id

        dir2_id, sub2_id = api.folder_file_ids(f'{tst_remote_root}/{tst_remote_sub1}/')
        assert not api.error_message
        assert dir2_id == sub1_id
        assert sub2_id

        dir2_id2, sub2_id2 = api.folder_file_ids(tst_remote_sub1 + '/', folder_id=sub1_id)
        assert not api.error_message
        assert dir2_id2 == dir2_id
        assert sub2_id2 == sub2_id

        dir3_id, fil3_id = api.folder_file_ids(tst_remote_sub2 + '/', folder_id=sub2_id)
        assert not api.error_message
        assert dir3_id == sub2_id
        assert fil3_id

    def test_folder_file_ids_errors(self, drive_api_path_id_content):
        api, remote_path, create_id, content = drive_api_path_id_content

        assert not api.folder_file_ids('not_existing_file.xxy_yzz')[1]
        assert api.error_message
        api.error_message = ""

        dir1_id, sub1_id = api.folder_file_ids(tst_remote_root)
        assert dir1_id == tst_google_drive_root_id
        assert sub1_id == ""
        assert tst_remote_root in api.error_message
        api.error_message = ""

        assert not api.folder_file_ids(tst_remote_path + '/_not_exising_tst_fil.xxx')[1]
        assert api.error_message
        api.error_message = ""

        assert not api.folder_file_ids(f'/{tst_remote_root}/_not_exising_tst_fil.xxx')[1]
        assert api.error_message
        api.error_message = ""

        assert not api.folder_file_ids('/tst_folder_not_existing', folder_id=tst_google_drive_root_id)[1]
        assert api.error_message
        api.error_message = ""

        assert not api.folder_file_ids('/tst_folder_not_existing/')[1]
        assert api.error_message
        api.error_message = ""

        assert not api.folder_file_ids('/oaio_root/')[1]                                # exists, but outside the root
        assert 'oaio_root' in api.error_message

        assert not api.folder_file_ids('/music/PlaylistBackups/2018oct/00sh.txt')[1]    # exists, but outside the root
        assert '00sh.txt' in api.error_message

    def test_google_docs(self):
        api = GoodriveApi(root_folder=tst_google_drive_root_id)
        nam = "Tst Google Document"
        mim = f'{GoodriveApi.SKIPPED_FILES_MIMETYPE_PREFIX}document'    # == 'application/vnd.google-apps.document'
        doc = {}
        try:
            body = {'name': nam, 'mimeType': mim, 'parents': [tst_google_drive_root_id]}
            doc = api.service.files().create(body=body, fields='*').execute()
            assert doc
            assert doc.get('name') == nam
            assert doc.get('mimeType') == mim
            assert not api.error_message
            did = doc.get('id')

            metadata = api.service.files().get(fileId=did).execute()
            assert metadata.get('name') == nam
            assert metadata.get('mimeType') == mim
            assert metadata.get('id') == did

            # instead of ids = api.folder_file_ids(nam), we wait because the drive needs sometime much longer
            max_tries = 129
            ids, tries, wait = api.wait_for_deployment_finish(nam, max_tries=max_tries, verbose=True)
            if tries > 1:
                print(f"**** Google Doc {'' if ids[1] else 'NOT '}created after {tries} tries and {wait} seconds")
            assert nam in api.error_message
            assert tst_google_drive_root_id == ids[0]
            assert did == ids[1]

        finally:
            if doc:
                api.error_message = ""
                api.delete_file_or_folder(nam)
                assert nam in api.error_message

    def test_request_error(self):
        api = GoodriveApi(root_folder=tst_google_drive_root_id)
        assert api.error_message == ""

        assert api._request(None) == {}
        assert api.error_message
