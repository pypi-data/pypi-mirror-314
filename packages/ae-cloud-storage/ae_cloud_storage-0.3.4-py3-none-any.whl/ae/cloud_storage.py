""" distribute files to and retrieve them from cloud storage hosts.

supported cloud storage hosts:
* Google Drive: https://developers.google.com/drive/api/guides/about-sdk
* DigiStorage: https://storage.rcs-rds.ro/help/developers

a comparison of cloud storage hosts, including free ones, can be found here: https://comparisontabl.es/cloud-storage/
(or https://docs.google.com/spreadsheets/d/1cEd65XDW3gBHnRsJ0rbq3V_B28mKySHiMPAZvArHiiA/).
but not all of them offer an API, see some recommendations in:
* https://blog.apilayer.com/5-cloud-storage-apis/#Filestack_API
* https://www.jsonapi.co/public-api/category/Cloud%20Storage%20&%20File%20Sharing

"""
import io
import json
import os
import time

from abc import ABC, abstractmethod
from typing import Any, Optional, Type, Union

import requests

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow                                          # type: ignore
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build                                                     # type: ignore
from googleapiclient.errors import HttpError                                                    # type: ignore
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload                           # type: ignore

from ae.base import os_path_basename, os_path_isfile, os_path_join, read_file, ErrorMsgMixin    # type: ignore


__version__ = '0.3.4'


_registered_csh_classes = {}  #: cloud storage class ids map to their related api classes, used by :func:`csh_api_class`


class CshApiBase(ErrorMsgMixin, ABC):
    def __init__(self, **csh_args):
        """ cloud storage host api instantiation and argument check.

        :param csh_args:        individual arguments, like host root path and credentials, of a cloud storage host api.
        """
        assert not csh_args, f"abstract CshApiBase.__init__() got unrecognized kwargs: {csh_args}"

    def __init_subclass__(cls):     #: base class to automatic map of cloud storage api classes declared in this module
        super().__init_subclass__()
        assert cls.__name__.endswith('Api')
        _registered_csh_classes[cls.__name__[:-3]] = cls

    @abstractmethod
    def deployed_file_content(self, file_path: str) -> Optional[bytes]:
        """ determine the file content of a file deployed to a server.

        :param file_path:       path of a deployed file relative to the host root.
        :return:                file content as bytes or None if error occurred (check self.error_message).
        """

    @abstractmethod
    def deploy_file(self, file_path: str, source_path: str = '') -> str:
        """ add or update a binary file to the cloud storage host.

        :param file_path:       path (relative to the host root) and name of the file to be deployed (added or updated).
        :param source_path:     source path if differs from the destination path given in
                                :paramref:`~deploy_file.file_path`.
        :return:                created/updated file path or empty string on error (see self.error_message for details).
        """

    @abstractmethod
    def delete_file_or_folder(self, file_path: str) -> str:
        """ delete a file or folder on the cloud storage host.

        :param file_path:       path relative to the host root of the file/folder to be deleted.
                                to delete a folder a trailing slash character has to be added.
                                .. note:: deleting a folder will also delete all files/folders underneath it.
        :return:                error message if deletion failed else on success an empty string.
        """


def csh_api_class(csh_id: str) -> Type[CshApiBase]:
    """ determine from the specified cloud storage host id the associated api class

    :param csh_id:              id of the cloud storage api class.
    :return:                    cloud storage api class if registered/declared, else the abstract class CshApiClass.
    """
    return _registered_csh_classes.get(csh_id, CshApiBase)


class DigiApi(CshApiBase):
    """ upload, update, download and delete files from Digi Movil Storage.

    the requests package is the only requirement of this class, which can be installed via `pip install requests`.

    """
    def __init__(self, root_folder: str = "", email: str = "", password: str = "", **csh_args):
        """ DigiStorage host instantiation.

        :param root_folder:     host root folder name/path.
        :param email:           host account email address to authenticate.
        :param password:        host account password to authenticate.
        :param csh_args:        generic cloud storage host arguments.
        """
        super().__init__(**csh_args)
        self.base_url = 'https://digistorage.es'
        self.session = requests.Session()
        token = self.session.get(self.base_url + '/token',
                                 headers={'X-Koofr-Email': email, 'X-Koofr-Password': password},
                                 ).headers['X-Koofr-Token']
        self.session.headers['Authorization'] = 'Token ' + token

        api_prefix = '/api/v2/mounts'
        res = self.session.get(self.base_url + api_prefix).json()
        mount = [x for x in res['mounts'] if x['name'] == 'DIGIstorage'][0]
        self.files_mount_id = api_prefix + '/' + mount['id'] + '/files/'

        self.root_folder = ""
        if root_folder:
            self._create_dirs(root_folder)  # create root folder if not exists
            self.error_message = ""         # ignore and reset error of root folder already exists
            self.root_folder = root_folder  # root folder instance var can be set NOW, to prevent access outside of it

    def _create_dirs(self, folder_path: str) -> str:
        if '//' in folder_path:
            self.error_message = f"folder path '{folder_path}' containing multiple consecutive slash characters"
            return self.error_message

        walk_path = ''
        for part in folder_path.strip('/').split('/'):
            walk_path += '/' + part
            parent_path, folder_name = os.path.split(walk_path)
            entry = [_ for _ in self.list_dir(parent_path) or [] if _.endswith('/')]
            if folder_name + '/' not in entry:
                res = self._request('post', self.files_mount_id + 'folder', parent_path,
                                    data=json.dumps({"name": folder_name}),
                                    headers={'content-type': 'application/json'}
                                    )
                if not res:
                    break

        return self.error_message

    def _request(self, method: str, slug: str, path: str, **kwargs) -> Optional[requests.Response]:
        url = self.base_url + slug
        kwargs['params'] = {'path': os_path_join(self.root_folder, path.lstrip('/'))}
        try:
            met = getattr(self.session, method)
            res = met(url, **kwargs)
            res.raise_for_status()
            self.error_message = ""
            return res
        except (requests.HTTPError, requests.ConnectionError, Exception) as ex:
            self.error_message = f"request {method}-method error '{ex}' for URL {url}, path {path} and kwargs={kwargs}"
        return None

    def deployed_file_content(self, file_path: str) -> Optional[bytes]:
        """ determine the file content of a file deployed to a server.

        :param file_path:       path of a deployed file relative to the host root path.
        :return:                file content as bytes or None if error occurred (check self.error_message).
        """
        res = self._request('get', '/content' + self.files_mount_id + 'get', file_path)
        if res:
            return res.content

        return None

    def deploy_file(self, file_path: str, source_path: str = '') -> str:
        """ add or update a binary file to the cloud storage host.

        :param file_path:       path (relative to the host root) and name of the file to be deployed (added or updated).
        :param source_path:     source path if differs from the destination path given in
                                :paramref:`~deploy_file.file_path`.
        :return:                created/updated file path or empty string on error (see self.error_message for details).
        """
        if ':' in file_path:
            self.error_message = f"invalid character ':' in remote file name/path '{file_path}'"
            return ""

        source_path = source_path or file_path
        try:
            content = read_file(source_path, extra_mode='b')
        except (FileNotFoundError, Exception):
            content = None
        if content is None:
            self.error_message = f"error reading the source file '{source_path}'"
            return ""

        path, file = os.path.split(file_path)

        items = self.list_dir(path)
        if items is None:
            self.error_message = ""
            self._create_dirs(path)
            if self.error_message:
                return ""
        elif file in items:
            self.delete_file_or_folder(file_path)   # prevent creating of path + "/" + file_stem + " (1)" + file_ext

        res = self._request('post', '/content' + self.files_mount_id + 'put', path,
                            files={'file': (file, content)},
                            )                       # res.json()[0]['name'] contains file name
        return file_path if res else ""

    def delete_file_or_folder(self, file_path: str) -> str:
        """ delete a file or folder on the cloud storage host.

        :param file_path:       path relative to the host root of the file/folder to be deleted.
                                to delete a folder a trailing slash character has to be added.
                                .. note:: deleting a folder will also delete all files/folders underneath it.
        :return:                error message if deletion failed else on success an empty string.
        """
        res = self._request('delete', self.files_mount_id + 'remove', file_path)
        return "" if res else self.error_message

    def list_dir(self, folder_path: str) -> Optional[list[str]]:
        """ determine files and folders in the specified folder.

        :param folder_path:     path to the folder (relative to the host root folder) to determine items of.
        :return:                list of files/folders names in the specified folder (sub-folders have a trailing slash)
                                or None if the folder does not exist.
        """
        res = self._request('get', self.files_mount_id + 'list', folder_path)
        if res and res.ok:
            files = res.json()['files']
            return [_['name'] + ('/' if _['type'] == 'dir' else '') for _ in files]
        return None

    def __del__(self):
        if self.session:
            self.session.close()


class GoodriveApi(CshApiBase):
    """ upload, update, download and delete files from a Google Drive.

    to prepare Google Drive host api instance (root folder and authentication), create in your console (at
    https://console.cloud.google.com/apis/credentials?orgonly=true&project=oaio-project&supportedpurview=organizationId)
    the credentials for a service account (or an OAuth 2.0 Client) and activate it for your Google Drive project.
    then download the credential json file and store it, and specify its location in the instantiation of the class.

    .. hint:: the Google ``API Keys`` cannot be used for Google Drive authentication.

    to install the required packages run in your virtual environment the following command::

        pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

    """
    CRED_SCOPES = ['https://www.googleapis.com/auth/drive']
    FOLDER_MIMETYPE = 'application/vnd.google-apps.folder'
    GOOGLE_DRIVE_DEFAULT_ROOT_FOLDER = 'root'
    SKIPPED_FILES_MIMETYPE_PREFIX = 'application/vnd.google-apps.'

    GoodriveRequestReturnType = dict[str, Any]

    def __init__(self, root_folder: str = GOOGLE_DRIVE_DEFAULT_ROOT_FOLDER,
                 sa_cred_dict: Optional[dict[str, Any]] = None, sa_cred_file: str = '.service_account_credentials.json',
                 oa_cred_file: str = '.oauth2_credentials.json', **csh_args):
        """ initialize an instance to access the Google Drive via API.

        :param root_folder:     Google Drive root folder id for this host api instance.
        :param sa_cred_dict:    service account credentials dictionary (if passed has priority over credential files).
        :param sa_cred_file:    service account credentials file path (if exists has priority over oa_cred_file).
        :param oa_cred_file:    path to the OAuth 2.0 credentials file.
        """
        super().__init__(**csh_args)
        self.root_folder_id_default = root_folder

        if sa_cred_dict:
            creds = self._service_account_authenticate(sa_cred_dict)
        elif os_path_isfile(sa_cred_file):
            creds = self._service_account_authenticate(sa_cred_file)
        else:
            assert os_path_isfile(oa_cred_file), f"missing credential json file '{sa_cred_file}' or '{oa_cred_file}'"
            creds = self._oauth2_authenticate(oa_cred_file)

        self.service = build('drive', 'v3', credentials=creds)

    def _create_folder(self, folder_name: str, parent_id: str) -> GoodriveRequestReturnType:
        """ create a single folder under the parent folder (specified by id).

        .. note::
            sometimes :meth:`.folder_file_ids` fails to see a created folder after the deployment. on subsequent
            bulk creations use :meth:`.wait_for_deployment_finish` to wait for finished/completed folder creation.

        :param folder_name:     name of the folder to create.
        :param parent_id:       id of the parent folder where to create a new folder underneath.
        :return:                dict with the id of the created folder.
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': self.FOLDER_MIMETYPE,
            'parents': [parent_id],
        }
        return self._request(self.service.files().create(body=file_metadata, fields="id, mimeType"))

    def _oauth2_authenticate(self, cred_info: Union[dict, str], cached_cred_file_path: str = '.token.json'
                             ) -> Optional[Credentials]:
        """ not used/tested """
        creds = None

        if os_path_isfile(cached_cred_file_path):   # if user authorization cache file exists then use it
            try:
                creds = Credentials.from_authorized_user_file(cached_cred_file_path, self.CRED_SCOPES)
            except (HttpError, Exception):
                creds = None

        if creds and creds.refresh_token and (creds.expired or not creds.valid):
            try:
                creds.refresh(Request())
            except (HttpError, Exception):
                creds = None

        if not creds or not creds.valid:
            try:
                if isinstance(cred_info, dict):
                    flow = InstalledAppFlow.from_client_config(cred_info, self.CRED_SCOPES)
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(cred_info, self.CRED_SCOPES)
                creds = flow.run_local_server(port=0)
            except (HttpError, Exception):
                creds = None

        if creds:
            with open(cached_cred_file_path, 'w') as token:     # save for next run
                token.write(creds.to_json())

        return creds

    def _service_account_authenticate(self, cred_info: Union[dict, str]) -> Optional[Credentials]:
        if isinstance(cred_info, dict):
            return service_account.Credentials.from_service_account_info(cred_info, scopes=self.CRED_SCOPES)
        else:
            return service_account.Credentials.from_service_account_file(cred_info, scopes=self.CRED_SCOPES)

    def _request(self, prepared_call: Any) -> GoodriveRequestReturnType:
        try:
            return prepared_call.execute()
        except (HttpError, Exception) as ex:
            self.error_message = f"HttpError {ex} executing {prepared_call}"
            return {}

    def delete_file_or_folder(self, file_path: str, empty_trash: bool = False) -> str:
        """ delete a file or folder on the cloud storage host.

        :param file_path:       path relative to the host root of the file/folder to be deleted.
                                to delete a folder a trailing slash character has to be added.
                                .. note:: deleting a folder will also delete all files/folders underneath it.
        :param empty_trash:     pass True to empty the trash (definitely removing this and other deleted files).
        :return:                error message if deletion failed else on success an empty string.
        """
        folder_id, file_id = self.folder_file_ids(file_path)
        if file_id:
            self._request(self.service.files().delete(fileId=file_id))  # returns {} on success and error
            if not self.error_message and empty_trash:
                self._request(self.service.files().emptyTrash())
        else:
            self.error_message = f"error in deleting file '{file_path}'"

        return self.error_message

    def deployed_file_content(self, file_path: str) -> Optional[bytes]:
        """ determine the file content of a file deployed to a server.

        :param file_path:       path of a deployed file relative to the host root folder.
        :return:                file content as bytes or None if error occurred (check self.error_message).
        """
        _folder_id, file_id = self.folder_file_ids(file_path)
        if not file_id:
            return None

        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        while True:
            status, done = downloader.next_chunk()
            if done:
                break
            # callback or print(f"{int(status.progress() * 100)}% in downloading the file '{folder_path}' ... ")

        fh.seek(0)
        content = fh.read()
        fh.close()
        return content

    def deploy_file(self, file_path: str, source_path: str = '') -> str:
        """ add or update a binary file to the cloud storage host.

        :param file_path:       path (relative to the host root) and name of the file to be deployed (added or updated).
        :param source_path:     source path if differs from the destination path given in
                                :paramref:`~deploy_file.file_path`.
        :return:                created/updated file id or empty string on error (check self.error_message for details).

        .. note::
            sometimes :meth:`.folder_file_ids` fails to see a deployed file directly after the deployment. on subsequent
            bulk deployments use :meth:`.wait_for_deployment_finish` to wait for finished/completed deployment.

        """
        if ':' in file_path:
            self.error_message = f"invalid character ':' in remote file name/path '{file_path}'"
            return ""

        media = MediaFileUpload(source_path or file_path)
        folder_id, file_id = self.folder_file_ids(file_path, create_folders=True)
        if file_id:
            file = self._request(self.service.files().update(fileId=file_id, media_body=media, fields="id"))
        else:
            self.error_message = ""
            file_metadata = {"name": os_path_basename(file_path), "parents": [folder_id]}
            file = self._request(self.service.files().create(body=file_metadata, media_body=media, fields="id"))
        return file.get('id', "")

    def folder_file_ids(self, file_path: str, folder_id: str = '', create_folders: bool = False) -> tuple[str, str]:
        """ convert Google Drive file path into the related folder and file ids.

        :param file_path:       path of a file or folder, relative to the folder specified in
                                :paramref:`~folder_file_ids.folder_id`.
        :param folder_id:       Google Drive folder id of the root folder where :paramref:`~folder_file_ids.folder_path`
                                is underneath of. if not passed then it defaults to the root folder (specified via
                                __init__()).

                                .. note::
                                    MyDrive GOOGLE_DRIVE_DEFAULT_ROOT_FOLDER/'root' id is working for OAuth2,
                                    but not for service accounts authentication.
        :param create_folders:  pass True to create non-existing folders in the specified file path.
        :return:                tuple of ids of the specified folder and of the basename file/folder.
                                if the second tuple item is an empty string then an error occurred, because either
                                the specified folder/file does not exist,
                                or the specified basename ends with a slash, although it is a file.

        .. note::
            if :paramref:`~folder_file_ids.folder_path` specifies a Google Drive cloud mimetype, like
            Google Doc/Sheet/.., then although the file id get returned, an error
            message get set (stating that Google Docs cannot be downloaded as files via
            :meth:`.deployed_file_content`).

        """
        if not folder_id:
            folder_id = self.root_folder_id_default

        err_msg = f"invalid path '{file_path}' "
        self.error_message = ""

        is_folder = file_path.endswith('/')
        path_parts = file_path.strip('/').split('/')
        last_idx = len(path_parts) - 1
        file_id = ''
        for idx, part in enumerate(path_parts):
            query = f"'{folder_id}' in parents and name = '{part}' and trashed = false"
            results = self._request(self.service.files().list(q=query, fields="files(id, mimeType)"))  # files(*)
            items = results.get('files', [])
            if items:
                file_item = items[0]
            else:
                if not create_folders or idx == last_idx and not is_folder:
                    self.error_message = err_msg + f"(missing '{part}' in folder '{'/'.join(path_parts[:idx])}')"
                    break       # return folder_id, ''
                file_item = self._create_folder(part, folder_id)

            if file_item['mimeType'] == self.FOLDER_MIMETYPE:
                if idx < last_idx:
                    folder_id = file_item['id']
                elif is_folder:
                    file_id = file_item['id']
                else:
                    self.error_message = err_msg + f"(expected trailing slash after last folder item '{part}')"
            elif idx == last_idx:
                file_id = file_item['id']
                if file_item['mimeType'].startswith(self.SKIPPED_FILES_MIMETYPE_PREFIX):
                    self.error_message = err_msg + "(Warning: Google Documents cannot be downloaded)"
            else:
                self.error_message = err_msg + f"(path item '{part}' is a file, not a folder)"
                break

        return folder_id, file_id if path_parts else folder_id

    def wait_for_deployment_finish(self, path: str, file_id: str = "", max_tries: int = 99, verbose: bool = False
                                   ) -> tuple[tuple[str, str], int, float]:
        """ wait until the deployment of a file or the creation of a folder is fully visible in the api.

        :param path:            path to the just created/deployed file/folder.
        :param file_id:         pass file/folder id to wait for, to restrict the item specified in :paramref:`.path`.
        :param max_tries:       number of tries/loops to check if the api can see the file/folder.
        :param verbose:         pass True to print to the console for each try.
        :return:                3-tuple consisting of the return value of :meth:`.folder_file_ids`,
                                the number of tries and the total amount of seconds waited.
        """
        start = time.time()     # waiting time normally around 5, but sometime up to 17 seconds
        tries = 0               # retrying normally around 14, but experienced up to 52 times
        while True:
            tries += 1
            ids = self.folder_file_ids(path)
            if (ids[1] == file_id if file_id else ids[1]) or tries == max_tries:
                break
            if verbose:
                print(f"**** {path} not created after {tries} tries, time waiting: {time.time() - start} seconds")
        return ids, tries, time.time() - start
