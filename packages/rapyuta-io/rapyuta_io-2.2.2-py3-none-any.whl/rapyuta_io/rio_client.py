# encoding: utf-8
from __future__ import absolute_import

import json
import os

import six

from rapyuta_io.clients import DeviceManagerClient, _ParamserverClient
from rapyuta_io.clients.catalog_client import CatalogClient
from rapyuta_io.clients.core_api_client import CoreAPIClient
from rapyuta_io.clients.device import Device
from rapyuta_io.clients.metrics import ListMetricsRequest, ListTagKeysRequest, ListTagValuesRequest, Metric, \
    MetricFunction, MetricOperation, QueryMetricsRequest, QueryMetricsResponse, Tags
from rapyuta_io.clients.rip_client import AuthTokenLevel, RIPClient
from rapyuta_io.clients.rosbag import ROSBagBlob, ROSBagBlobStatus, ROSBagJob, ROSBagJobStatus
from rapyuta_io.clients.user_group import UserGroup
from rapyuta_io.utils import InvalidAuthTokenException, \
    InvalidParameterException
from rapyuta_io.utils.settings import default_host_config
from rapyuta_io.utils.utils import valid_list_elements


class Client(object):
    """
    Client class provides access to device, package, volume and deployment classes.

    """

    def __init__(self, auth_token, project=None):
        """
        Get new client object

        :param auth_token: Authentication token
        :type auth_token: string

        :param project: project_guid of the user
        :type project: string
        """

        super(Client, self).__init__()
        self._validate_auth_token(auth_token)
        self._catalog_client = CatalogClient(auth_token, project,
                                             catalog_api_host=self._get_api_endpoints('catalog_host'))
        self._core_api_client = CoreAPIClient(auth_token, project,
                                              core_api_host=self._get_api_endpoints('core_api_host'))
        self._dmClient = DeviceManagerClient(auth_token, project,
                                             device_api_host=self._get_api_endpoints('core_api_host'))
        self._paramserver_client = _ParamserverClient(auth_token, project, self._get_api_endpoints('core_api_host'))

    @staticmethod
    def _validate_auth_token(auth_token):
        if not auth_token:
            raise InvalidAuthTokenException("Authentication token is missing")

    @staticmethod
    def _get_api_endpoints(host_type):
        try:
            config_file = os.environ["RIO_CONFIG"]
            with open(config_file, 'r') as f:
                configuration = json.load(f)
            return configuration[host_type]
        except Exception:
            return default_host_config[host_type]

    def _add_auth_token(self, obj):
        setattr(obj, '_host', self._catalog_client._catalog_api_host)
        setattr(obj, '_auth_token', self._catalog_client._auth_token)
        setattr(obj, '_project', self._catalog_client._project)

    @staticmethod
    def get_auth_token(email, password, token_level=AuthTokenLevel.LOW):
        """
        Generate and fetch a new API Authentication Token.

        :param email: Email of the user account.
        :type email: str
        :param password: User password for the account.
        :type password: str
        :param token_level: Level of the token. This corresponds to token validity
        :type token_level: AuthTokenLevel
        :return: str

        Following example demonstrates how to get auth token

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.clients.rip_client import AuthTokenLevel
            >>> auth_token = Client.get_auth_token('email@example.com', 'password', AuthTokenLevel.MED)
            >>> client = Client(auth_token, 'project-id')
        """
        rip_client = RIPClient(rip_host=Client._get_api_endpoints('rip_host'))
        return rip_client.get_auth_token(email, password, token_level)

    def set_project(self, project_guid):
        """
        Sets the current Project for the Client.

        :param project_guid: GUID of the Project

        """
        self._catalog_client.set_project(project_guid)
        self._core_api_client.set_project(project_guid)
        self._dmClient.set_project(project_guid)
        self._paramserver_client.set_project(project_guid)

    def get_authenticated_user(self):
        """
        Get details for authenticated User.

        :rtype: :py:class:`~rapyuta_io.clients.project.User`

        Following example demonstrates how to get authenticated user details.

        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='auth_token', project='project_guid')
        >>> user = client.get_authenticated_user()

        """
        return self._core_api_client.get_user()

    def get_user_organizations(self):
        """
        Get list of organizations that a user is part of.

        :rtype: list(:py:class:`~rapyuta_io.clients.organization.Organization`)

        Following example demonstrates how to get the list of organizations that a user is part of.

        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='auth_token', project='project_guid')
        >>> organizations = client.get_user_organizations()

        """
        return self._core_api_client.get_user_organizations()

    def get_all_devices(self, online_device=False, arch_list=None, retry_limit=0, device_name=None):
        """
        Get all the devices

        :param online_device: The value True returns only those devices that are online,
            while the value False returns all devices
        :type online_device: bool
        :param arch_list: If set, another call is made to filter devices by architecture.
            Valid architectures can be found in :py:class:`~.DeviceArch` class. Note: Only online devices
            can be filtered by architecture. Therefore if `arch_list` is set, non-online
            devices are not included in the result irrespective of the value of `online_device`.
        :type arch_list: list
        :param retry_limit: No of retry attempts to be carried out if any failures occurs\
                during the API call.
        :type retry_limit: int
        :param device_name: Optional parameter to filter the devices based on the device name.
        :type device_name: str
        :return: List of instances of :py:class:`~Device` class
        :raises: :py:class:`APIError`: If the API returns an error, a status code
            of anything other than 200/201 is returned

        Following example demonstrates how to get the device list

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.clients import DeviceArch
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> devices = client.get_all_devices()
            >>> filtered_by_arch_devices = client.get_all_devices(arch_list=[
            >>>     DeviceArch.ARM32V7, DeviceArch.ARM64V8, DeviceArch.AMD64])

        """
        return self._dmClient.device_list(online_device, arch_list, retry_limit, device_name=device_name)

    def get_device(self, device_id, retry_limit=0):
        """
        Get information of a device.

        :param device_id: Device Id
        :type device_id: string
        :param retry_limit: No of retry attempts to be carried out if any failures occurs\
         during the API call.
        :type retry_limit: int
        :return: Instances of :py:class:`~Device` class.
        :raises: :py:class:`~utils.error.ResourceNotFoundError`: If the device with given device id is not present.
        :raises: :py:class:`APIError`: If the API returns an error, a status code of
            anything other than 200/201 is returned.

        Following example demonstrates how to select a device information.

            >>> from rapyuta_io import Client
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> device = client.get_device(device_id="device_id")

        """
        return self._dmClient.get_device(device_id, retry_limit)

    def create_device(self, device):
        """
        Create a device on rapyuta.io platform.

        :param device: device object
        :type device: :py:class:`~rapyuta_io.clients.device.Device`
        :rtype: :py:class:`~rapyuta_io.clients.device.Device`

        Following example demonstrates how to create a device.

            >>> from rapyuta_io import Client, ROSDistro
            >>> from rapyuta_io.clients.device import Device, DeviceRuntime, DevicePythonVersion
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> device = Device(name='test-device', runtime=DeviceRuntime.DOCKER, ros_distro=ROSDistro.MELODIC,
            ...                 rosbag_mount_path='/opt/rapyuta/volumes/rosbag', python_version=DevicePythonVersion.PYTHON3)
            >>> device = client.create_device(device)
        """
        if not isinstance(device, Device):
            raise InvalidParameterException("device must be non-empty and of type "
                                            "rapyuta_io.clients.device.Device")

        device_response = self._dmClient.create_device(device)
        device_id = device_response['response']['device_id']
        return self.get_device(device_id)

    def delete_device(self, device_id):
        """
        Delete a device based on its device id.

        :param device_id: Device Id
        :type device_id: str

        Following example demonstrates how to delete a device.

        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='auth_token', project='project_guid')
        >>> client.delete_device('device-id')
        """
        if not device_id or not isinstance(device_id, six.string_types):
            raise InvalidParameterException('device_id needs to be a non empty string')
        return self._dmClient.delete_device(device_id)

    def toggle_features(self, device_id, features, config=None):
        """
        Patch a device on rapyuta.io platform.

        :param device_id: Device ID
        :type device_id: str
        :param features: A tuple of featues and their states
        :type features: list<tuple>
        :param config: A dict of additional feature configuration
        :type config: dict

        Following example demonstrates how to toggle features a device.

            >>> from rapyuta_io import Client
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> client.toggle_features('device-id', [('vpn', True), ('tracing', False)], config={'vpn': {'advertise_routes': True}})
        """
        if not device_id or not isinstance(device_id, six.string_types):
            raise InvalidParameterException('device_id needs to be a non empty string')
        if not features or not (isinstance(features, list) or isinstance(features, tuple)):
            raise InvalidParameterException('features needs to be a list or tuple')

        data = {}
        for entry in features:
            feature, state = entry
            data[feature] = state

        if config is not None:
            data['config'] = config

        return self._dmClient.patch_daemons(device_id, data)

    def upload_configurations(self, rootdir, tree_names=None, delete_existing_trees=False, as_folder=False):
        """
        Traverses rootdir and uploads configurations following the same directory structure.

        :param rootdir: Path to directory containing configurations
        :type rootdir: str
        :param tree_names: List of specific configuration trees to upload. If None, all trees under rootdir are uploaded
        :type tree_names: list[str], optional
        :param delete_existing_trees: For each tree to upload, delete existing tree at the server. Defaults to False
        :type delete_existing_trees: bool, optional
        :param as_folder: For each tree to upload, upload as an folder hierarchy
        :as_folder: bool, optional

        Following example demonstrates how to use upload_configurations and handle errors.

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.utils.error import BadRequestError, InternalServerError
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> try:
            ...     client.upload_configurations('path/to/configs/source_dir',
            ...                                  tree_names=['config_tree1', 'config_tree2'],
            ...                                  delete_existing_trees=True)
            ... except (BadRequestError, InternalServerError) as e:
            ...     print 'failed API request', e.tree_path, e
            ... except (IOError, OSError) as e:
            ...     print 'failed file/directory read', e

        """
        return self._paramserver_client.upload_configurations(rootdir, tree_names, delete_existing_trees, as_folder)

    def download_configurations(self, rootdir, tree_names=None, delete_existing_trees=False):
        """
        Download all configurations to rootdir following the same directory structure. If rootdir does not exist, it is
        created.

        :param rootdir: Path to directory to store downloaded configurations
        :type rootdir: str
        :param tree_names: List of specific configuration trees to download. If None, all trees are downloaded
        :type tree_names: list[str], optional
        :param delete_existing_trees: For each tree to download, delete existing tree on the filesystem. Defaults to
            False
        :type delete_existing_trees: bool, optional

        Following example demonstrates how to use download_configurations and handle errors.

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.utils.error import APIError, InternalServerError, ConfigNotFoundException
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> try:
            ...     client.download_configurations('path/to/destination_dir',
            ...                                    tree_names=['config_tree1', 'config_tree2'],
            ...                                    delete_existing_trees=True)
            ... except (APIError, InternalServerError) as e:
            ...     print('failed API request', e.tree_path, e)
                except ConfigNotFoundException as e:
                    print ('config not found')
            ... except (IOError, OSError) as e:
            ...     print('failed file/directory creation', e)

        """
        return self._paramserver_client.download_configurations(rootdir, tree_names, delete_existing_trees)

    def apply_parameters(self, device_list, tree_names=None, retry_limit=0):
        """
        Applies configuration parameters for the given device_list. If tree_names is given, only these trees are
        applied.

        :param device_list: List of device IDs
        :type device_list: list[str]
        :param tree_names: List of configuration tree names
        :type tree_names: list[str]
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: List of dictionaries - each with device_id, bool success status, and an error message if the success
            status is False for that device_id
        :rtype: list[dict]

        Following example demonstrates how to use apply_parameters and handle errors.

            >>> from rapyuta_io import Client
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> devices = client.get_all_devices()
            >>> response = client.apply_parameters([device.deviceId for device in devices])
            >>> for device in response:
            ...     if not device['success']:
            ...         print device['device_id'], device['error']

        """
        return self._dmClient.apply_parameters(device_list, tree_names, retry_limit)

    def get_rosbag_job(self, guid):
        """
        Get ROSBag Job

        :param guid: ROSBag Job GUID
        :type guid: str

        Following example demonstrates how to fetch a ROSBag Job.

            >>> from rapyuta_io import Client
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> rosbag_job = client.get_rosbag_job('job-guid')

        """
        if not guid or not isinstance(guid, six.string_types):
            raise InvalidParameterException('guid needs to be a non-empty string')
        rosbag_job = self._catalog_client.get_rosbag_job(guid)
        rosbag_job = ROSBagJob.deserialize(rosbag_job)
        self._add_auth_token(rosbag_job)
        return rosbag_job

    def create_rosbag_job(self, rosbag_job):
        """
        Create a ROSBag Job

        :param rosbag_job: ROSBag object
        :type rosbag_job: :py:class:`~rapyuta_io.clients.rosbag.ROSBagJob`
        :raises: :py:class:`~utils.error.BadRequestError`: Rosbag Upload Options are required in case of Device jobs
        :return: Instance of :py:class:`~rapyuta_io.clients.rosbag.ROSBagJob` class

        Following example demonstrates how to create a ROSBag Job.

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.clients.rosbag import ROSBagJob, ROSBagOptions
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> rosbag_options = ROSBagOptions(all_topics=True)
            >>> rosbag_job = ROSBagJob(deployment_id="deployment-id",
            ...              component_instance_id=component_instance_id,
            ...              rosbag_options=rosbag_options, name='name')
            >>> rosbag_job = client.create_rosbag_job(rosbag_job)

        """
        if not isinstance(rosbag_job, ROSBagJob):
            raise InvalidParameterException("rosbag job must be non-empty and of type "
                                            "rapyuta_io.clients.rosbag.ROSBagJob")
        if not rosbag_job.deployment_id or not isinstance(rosbag_job.deployment_id, six.string_types):
            raise InvalidParameterException('deployment id must be non empty string')
        if not rosbag_job.component_instance_id or not isinstance(rosbag_job.component_instance_id, six.string_types):
            raise InvalidParameterException('component instance id must be non empty string')

        response = self._catalog_client.create_rosbag_job(rosbag_job)
        rosbag_job = ROSBagJob.deserialize(response)
        self._add_auth_token(rosbag_job)
        return rosbag_job

    def list_rosbag_jobs(self, deployment_id, component_instance_ids=None, guids=None, statuses=None):
        """
        Get rosbag jobs based on the passed query params

        :param deployment_id: deployment guid
        :type  deployment_id: str
        :param component_instance_ids: list of component instance id
        :type  component_instance_ids: list(str)
        :param guids: list of job guid
        :type  guids: list(str)
        :param statuses: list of rosbag status
        :type  statuses: list(:py:class:`~rapyuta_io.clients.rosbag.ROSBagJobStatus`)
        :return: list(:py:class:`~rapyuta_io.clients.rosbag.ROSBagJob`)

        Following example demonstrates how to get ROSBag Jobs
            1. List all ROSBagJobs of a deployment
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_jobs = client.list_rosbag_jobs(deployment_id)

            2. List ROSBagJobs of a deployment’s component instance
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_jobs = client.list_rosbag_jobs(deployment_id,
                ...                                       component_instance_ids=['comp-inst-id'])

            3. List specific ROSBagJobs of a deployment
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_jobs = client.list_rosbag_jobs(deployment_id, guids=['job-id'])

            4. List ROSBagJobs with statuses of a deployment
                >>> from rapyuta_io import Client
                >>> from rapyuta_io.clients.rosbag import ROSBagJobStatus
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_jobs = client.list_rosbag_jobs(deployment_id,
                ...                                       statuses=[ROSBagJobStatus.RUNNING])

        """
        if not deployment_id or not isinstance(deployment_id, six.string_types):
            raise InvalidParameterException('deployment id be non empty string')

        if component_instance_ids is not None and not valid_list_elements(component_instance_ids, six.string_types):
            raise InvalidParameterException('component_instance_ids needs to be a list of string')
        if guids is not None and not valid_list_elements(guids, six.string_types):
            raise InvalidParameterException('guids needs to be a list of string')
        if statuses is not None and not valid_list_elements(statuses, ROSBagJobStatus):
            raise InvalidParameterException('status needs to be a list of ROSBagJobStatus')
        if guids is not None and component_instance_ids:
            raise InvalidParameterException('only guid or component_instance_id should be present')

        response = self._catalog_client.list_rosbag_jobs(deployment_id, component_instance_ids=component_instance_ids,
                                                         guids=guids, statuses=statuses)
        rosbag_jobs = [ROSBagJob.deserialize(resp) for resp in response]
        for rosbag_job in rosbag_jobs:
            self._add_auth_token(rosbag_job)
        return rosbag_jobs

    def list_rosbag_jobs_in_project(self, device_ids):
        """
        Lists rosbag jobs based on device ids

        :param device_ids: list of device id
        :type  device_ids: list(str)

        Following example demonstrates how to list rosbag jobs in a project based on device ids:
            1. List all ROSBagJobs based on device ids
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_jobs = client.list_rosbag_jobs_in_project(['device-id'])
        """
        if device_ids is None or (not valid_list_elements(device_ids, six.string_types)) or len(device_ids) == 0:
            raise InvalidParameterException('device_ids need to be a non-empty list of string')

        response = self._catalog_client.list_rosbag_jobs_in_project(device_ids=device_ids)
        rosbag_jobs = [ROSBagJob.deserialize(resp) for resp in response]
        for rosbag_job in rosbag_jobs:
            self._add_auth_token(rosbag_job)
        return rosbag_jobs

    def stop_rosbag_jobs(self, deployment_id, component_instance_ids=None, guids=None):
        """
        Stop ROSBag Job based on the passed query params

        :param deployment_id: deployment guid
        :type deployment_id: str
        :param component_instance_ids: list of component instance id
        :type component_instance_ids: list(str)
        :param guids: list of job guid
        :type  guids: list(str)

        Following example demonstrates how to stop ROSBag Jobs
            1. Stop all ROSBagJobs of a deployment
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> client.stop_rosbag_jobs(deployment_id)

            2. Stop ROSBagJobs of a deployment’s component instance
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> client.stop_rosbag_jobs(deployment_id, component_instance_ids=['comp-inst-id'])

            3. Stop specific ROSBagJobs of a deployment
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> client.stop_rosbag_jobs(deployment_id, guids=['job-id'])

        """
        if component_instance_ids is not None and not valid_list_elements(component_instance_ids, six.string_types):
            raise InvalidParameterException('component_instance_ids needs to be a list of string')
        if guids is not None and not valid_list_elements(guids, six.string_types):
            raise InvalidParameterException('guids needs to list of string')
        if guids and component_instance_ids:
            raise InvalidParameterException('only guid or component_instance_id should be present')

        self._catalog_client.stop_rosbag_jobs(deployment_id, component_instance_ids=component_instance_ids, guids=guids)

    def list_rosbag_blobs(self, guids=None, deployment_ids=None, component_instance_ids=None,
                          job_ids=None, statuses=None, device_ids=None):
        """
        Get rosbag blobs based on the passed query params


        :param guids: list of blob guid
        :type guids: list(str)
        :param deployment_ids: list of deployment id
        :type deployment_ids: list(str)
        :param component_instance_ids: list of component instance id
        :type component_instance_ids: list(str)
        :param job_ids: list of job guid
        :type job_ids: list(str)
        :param statuses: list of
        :type statuses: list(:py:class:`~rapyuta_io.clients.rosbag.ROSBagBlobStatus`)
        :param device_ids: list of device id
        :type  device_ids: list(str)
        :return: list(:py:class:`~rapyuta_io.clients.rosbag.ROSBagBlob`)

        Following example demonstrates how to stop ROSBag Blobs
            1. List specific ROSBagBlobs
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_blobs = client.list_rosbag_blobs(guids=['blob-id'])

            2. List all ROSBagBlobs of a deployment
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_blobs = client.list_rosbag_blobs(deployment_ids=['dep-id'])

            3. List ROSBagBlobs of a deployment’s component instance
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_blobs = client.list_rosbag_blobs(component_instance_ids=['dep-id'])

            4. List all ROSBagBlobs of a job
                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_blobs = client.list_rosbag_blobs(job_ids=['job-id'])

            5. List ROSBagBlobs with statuses
                >>> from rapyuta_io import Client
                >>> from rapyuta_io.clients.rosbag import ROSBagBlobStatus
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_blobs = client.list_rosbag_blobs(statuses=[ROSBagBlobStatus.UPLOADED])

            6. List ROSBagBlobs of a device
                >>> from rapyuta_io import Client
                >>> from rapyuta_io.clients.rosbag import ROSBagBlobStatus
                >>> client = Client(auth_token='auth_token', project='project_guid')
                >>> rosbag_blobs = client.list_rosbag_blobs(device_ids=['device-id'])

        """
        if component_instance_ids is not None and not valid_list_elements(component_instance_ids, six.string_types):
            raise InvalidParameterException('component_instance_ids needs to be a list of string')
        if guids is not None and not valid_list_elements(guids, six.string_types):
            raise InvalidParameterException('guids needs to be a list of string')
        if deployment_ids is not None and not valid_list_elements(deployment_ids, six.string_types):
            raise InvalidParameterException('deployment_ids needs to be a list of string')
        if job_ids is not None and not valid_list_elements(job_ids, six.string_types):
            raise InvalidParameterException('job_ids needs to be a list of string')
        if statuses is not None and not valid_list_elements(statuses, ROSBagBlobStatus):
            raise InvalidParameterException('status needs to be a list of ROSBagBlobStatus')
        if device_ids is not None and not valid_list_elements(device_ids, six.string_types):
            raise InvalidParameterException('device_ids need to be a list of string')

        query_param_count = 0
        if deployment_ids:
            query_param_count += 1
        if component_instance_ids:
            query_param_count += 1
        if guids:
            query_param_count += 1
        if job_ids:
            query_param_count += 1

        if query_param_count > 1:
            raise InvalidParameterException('only one of deployment_ids, component_instance_ids, '
                                            'guids or job_ids should be present')

        response = self._catalog_client.list_rosbag_blobs(guids=guids, deployment_ids=deployment_ids,
                                                          component_instance_ids=component_instance_ids,
                                                          job_ids=job_ids, statuses=statuses, device_ids=device_ids)

        rosbag_blobs = [ROSBagBlob.deserialize(resp) for resp in response]
        for rosbag_blob in rosbag_blobs:
            self._add_auth_token(rosbag_blob)
        return rosbag_blobs

    def download_rosbag_blob(self, guid, filename=None, download_dir=None):
        """
        Download rosbag bag file

        :param guid: blob guid
        :type guid: str
        :param download_dir: filename
        :type download_dir: str

        :param filename: filename
        :type filename: str

        Following example demonstrates how to download ROSBag Blob

        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='auth_token', project='project_guid')
        >>> client.download_rosbag_blob('blob-id', 'filename.bag')

        """
        if not guid or not isinstance(guid, six.string_types):
            raise InvalidParameterException('guid needs to non empty string')
        response = self._catalog_client.get_blob_download_url(guid)
        signed_url = response['url']
        self._catalog_client.download_blob(signed_url, filename, download_dir)

    def delete_rosbag_blob(self, guid):
        """
        Delete the rosbag bag file

        :param guid: blob guid
        :type guid: str

        Following example demonstrates how to delete ROSBag Blob

        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='auth_token', project='project_guid')
        >>> client.delete_rosbag_blob('blob-id')

        """
        if not guid or not isinstance(guid, six.string_types):
            raise InvalidParameterException('guid needs to non empty string')
        self._catalog_client.delete_rosbag_blob(guid)

    def query_metrics(self, query_metrics_request):
        """
        Query and fetch metrics

        :param query_metrics_request: QueryMetricsRequest instance
        :type query_metrics_request: :py:class:`~rapyuta_io.clients.metrics.QueryMetricsRequest`
        :rtype: :py:class:`~rapyuta_io.clients.metrics.QueryMetricsResponse`

        Following example demonstrates how to query metrics

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.clients.metrics import QueryMetricsRequest, StepInterval, SortOrder,
            >>> MetricOperation, MetricFunction
            >>> from datetime import datetime, timedelta
            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> now = datetime.utcnow()
            >>> metrics = [MetricOperation(MetricFunction.AVG, 'mem.total'),
            >>>            MetricOperation(MetricFunction.AVG, 'mem.used')]
            >>> request = QueryMetricsRequest(from_datetime=now-timedelta(days=10), to_datetime=now,
            >>>                               step_interval=StepInterval.FIFTEEN_MINUTES, metrics=metrics)
            >>> response = client.query_metrics(request)
            >>> print([str(col) for col in response.columns])
            >>>
            >>> import pandas as pd  # pip install pandas
            >>> rows, columns = response.to_row_column_format()
            >>> df = pd.DataFrame(data=rows, columns=columns)
            >>> df['timestamp'] = pd.to_datetime(df['timestamp'])
            >>> print(df.head())

        """
        if not isinstance(query_metrics_request, QueryMetricsRequest):
            raise InvalidParameterException('metrics_query_request must be '
                                            'of type rapyuta_io.clients.metrics.MetricsQueryRequest')

        default_tags = {}
        if not query_metrics_request.tags.get(query_metrics_request.TENANT_ID_TAG):
            project = self._core_api_client._project
            if not project:
                raise InvalidParameterException('Either set project on client using client.set_project(), or '
                                                'set {} in tags'.format(query_metrics_request.TENANT_ID_TAG))
            default_tags[query_metrics_request.TENANT_ID_TAG] = {
                "operator": "eq",
                "value": project
            }

        if not query_metrics_request.tags.get(query_metrics_request.ORGANIZATION_ID_TAG):
            user = self._core_api_client.get_user()
            organization_guid = user.organization.guid
            default_tags[query_metrics_request.ORGANIZATION_ID_TAG] = {
                "operator": "eq",
                "value": organization_guid
            }

        query_metrics_request.tags.update(default_tags)

        response = self._core_api_client.query_metrics(query_metrics_request)
        return QueryMetricsResponse.deserialize(response)

    def list_metrics(self, list_metrics_request):
        """
        List metrics for a particular entity

        :param list_metrics_request: ListMetricsRequest instance
        :type list_metrics_request: :py:class:`~rapyuta_io.clients.metrics.ListMetricsRequest`
        :rtype: list(:py:class:`~rapyuta_io.clients.metrics.Metric`)

        Following example demonstrates how to list metrics

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.clients.metrics import ListMetricsRequest, Entity
            >>> from datetime import datetime, timedelta
            >>> project_guid = 'project_guid'
            >>> client = Client(auth_token='auth_token', project=project_guid)
            >>> now = datetime.utcnow()
            >>> request = ListMetricsRequest(Entity.PROJECT, project_guid,
            ...                              start_date=now-timedelta(days=30), end_date=now)
            >>> for metric in client.list_metrics(request):
            ...    print(metric.metric_group, metric.metric_names)

        """
        if not isinstance(list_metrics_request, ListMetricsRequest):
            raise InvalidParameterException('metrics_query_request must be of type '
                                            'rapyuta_io.clients.metrics.ListMetricsRequest')

        response = self._core_api_client.list_metrics(list_metrics_request)
        return [Metric.deserialize(resp) for resp in response.get('metrics', [])]

    def list_tag_keys(self, list_tag_keys_request):
        """
        List Tag Keys for a particular entity

        :param list_tag_keys_request: ListTagKeysRequest
        :type list_tag_keys_request: :py:class:`~rapyuta_io.clients.metrics.ListTagKeysRequest`
        :rtype: list(:py:class:`~rapyuta_io.clients.metrics.Tags`)

        Following example demonstrates how to list tag keys

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.clients.metrics import ListTagKeysRequest, Entity
            >>> from datetime import datetime, timedelta
            >>> project_guid = 'project_guid'
            >>> client = Client(auth_token='auth_token', project=project_guid)
            >>> now = datetime.utcnow()
            >>> request = ListTagKeysRequest(Entity.PROJECT, project_guid,
            ...                              start_date=now-timedelta(days=30), end_date=now)
            >>> for tag in client.list_tag_keys(request):
            ...     print(tag.metric_group, tag.tags)

        """
        if not isinstance(list_tag_keys_request, ListTagKeysRequest):
            raise InvalidParameterException('metrics_query_request must be of '
                                            'type rapyuta_io.clients.metrics.ListTagKeysRequest')

        response = self._core_api_client.list_tag_keys(list_tag_keys_request)
        return [Tags.deserialize(resp) for resp in response.get('tag_keys', [])]

    def list_tag_values(self, list_tag_values_request):
        """
        List Tag Values for a particular entity

        :param list_tag_values_request: ListTagValuesRequest
        :type list_tag_values_request: :py:class:`~rapyuta_io.clients.metrics.ListTagValuesRequest`
        :rtype: list(str)

        Following example demonstrates how to list tag values

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.clients.metrics import ListTagValuesRequest, Entity
            >>> from datetime import datetime, timedelta
            >>> project_guid = 'project_guid'
            >>> client = Client(auth_token='auth_token', project=project_guid)
            >>> now = datetime.utcnow()
            >>> request = ListTagValuesRequest(Entity.PROJECT, project_guid, 'cpu',
            ...                                start_date=now-timedelta(days=30), end_date=now)
            >>> for tag_value in client.list_tag_values(request):
            ...     print(tag_value)

        """
        if not isinstance(list_tag_values_request, ListTagValuesRequest):
            raise InvalidParameterException('metrics_query_request must be of '
                                            'type rapyuta_io.clients.metrics.ListTagValuesRequest')

        response = self._core_api_client.list_tag_values(list_tag_values_request)
        return response.get('tags_values', [])

    def list_usergroups(self, org_guid):
        """
        List usergroups in an organization

        :param org_guid: Organization GUID
        :type org_guid: str
        :return: A list of all Usergroups in the organization
        :rtype: list(:py:class:`~rapyuta_io.clients.user_group.UserGroup`)

        Following example demonstrates how to list usergroups

            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> user = self._core_api_client.get_user()
            >>> organization_guid = user.organization.guid
            >>> client.list_usergroups(organization_guid)

        """
        return self._core_api_client.list_usergroups(org_guid)

    def get_usergroup(self, org_guid, group_guid):
        """
        Get usergroup using its GUID

        :param org_guid: Organization GUID
        :type org_guid: str
        :param group_guid: Usergroup GUID
        :type group_guid: str
        :return: A usergroup
        :rtype: :py:class:`~rapyuta_io.clients.user_group.UserGroup`

        Following example demonstrates how to fetch a usergroup using its GUID

            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> user = self._core_api_client.get_user()
            >>> organization_guid = user.organization.guid
            >>> client.get_usergroup(organization_guid, 'group-guid')

        """
        return self._core_api_client.get_usergroup(org_guid, group_guid)

    def delete_usergroup(self, org_guid, group_guid):
        """
        Delete usergroup using its GUID

        :param org_guid: Organization GUID
        :type org_guid: str
        :param group_guid: Usergroup GUID
        :type group_guid: str

        Following example demonstrates how to delete a usergroup using its GUID

            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> user = self._core_api_client.get_user()
            >>> organization_guid = user.organization.guid
            >>> client.delete_usergroup(organization_guid, 'group-guid')

        """
        return self._core_api_client.delete_usergroup(org_guid, group_guid)

    def create_usergroup(self, org_guid, usergroup):
        """
        Create usergroup in organization

        :param org_guid: Organization GUID
        :type org_guid: str
        :param usergroup: usergroup object
        :type usergroup: py:class:`~rapyuta_io.clients.user_group.UserGroup`
        :return: Usergroup object
        :rtype: :py:class:`~rapyuta_io.clients.user_group.UserGroup`

        Following example demonstrates how to create usergroup in an organization

            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> user = self._core_api_client.get_user()
            >>> organization_guid = user.organization.guid
            >>> usergroup = UserGroup(name='test-usergroup', description='test-description', creator=user.guid)
            >>> usergroup = client.create_usergroup(organization_guid, usergroup)

        """
        return self._core_api_client.create_usergroup(org_guid, usergroup)

    def update_usergroup(self, org_guid, group_guid, usergroup):
        """
        Update usergroup in organization

        :param org_guid: Organization GUID
        :type org_guid: str
        :param group_guid: Usergroup GUID
        :type group_guid: str
        :param usergroup: Usergroup object
        :type usergroup: py:class:`~rapyuta_io.clients.user_group.UserGroup`
        :return: Usergroup object
        :rtype: :py:class:`~rapyuta_io.clients.user_group.UserGroup`

        Following example demonstrates how to update usergroup

            >>> client = Client(auth_token='auth_token', project='project_guid')
            >>> user = self._core_api_client.get_user()
            >>> organization_guid = user.organization.guid
            >>> usergroup = UserGroup(name='test-usergroup-updated', description='test-description-updated', creator=user.guid)
            >>> usergroup = client.update_usergroup(organization_guid, 'group-guid', usergroup)

        """
        return self._core_api_client.update_usergroup(org_guid, group_guid, usergroup)
