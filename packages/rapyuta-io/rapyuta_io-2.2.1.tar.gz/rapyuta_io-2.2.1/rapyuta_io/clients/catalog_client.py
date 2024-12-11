# encoding: utf-8
from __future__ import absolute_import

import os
import re

from rapyuta_io.clients.api_client import CatalogConfig
from rapyuta_io.utils import RestClient, PackageNotFound
from rapyuta_io.utils.rest_client import HttpMethod
from rapyuta_io.utils.settings import CATALOG_API_PATH
from rapyuta_io.utils.utils import response_validator


class CatalogClient(CatalogConfig):

    def __init__(self, auth_token, project, catalog_api_host):
        super(CatalogClient, self).__init__(catalog_api_host, auth_token, project)
        self._api_path = CATALOG_API_PATH

    def _get_api_path(self):
        return self._catalog_api_host + self._api_path

    def _execute(self, url, method=HttpMethod.GET, retry_count=0, payload=None, query_params=None):
        rest_client = RestClient(url).method(method).headers(self._headers).retry(retry_count).query_param(query_params)
        response = rest_client.execute(payload)
        return response

    @response_validator(True, {404: PackageNotFound})
    def _get_service(self, package_id, retry_limit=0):
        url = self._get_api_path() + "?package_uid=%s" % package_id
        return self._execute(url, HttpMethod.GET, retry_limit)

    @response_validator(True)
    def get_rosbag_job(self, guid):
        url = self._catalog_api_host + '/rosbag-jobs/job/{}'.format(guid)
        return self._execute(url, HttpMethod.GET)

    @response_validator(True)
    def create_rosbag_job(self, rosbag_job):
        url = self._catalog_api_host + '/rosbag-jobs/{}'.format(rosbag_job.deployment_id)
        return self._execute(url, HttpMethod.POST, payload=rosbag_job.serialize())

    @response_validator(True)
    def list_rosbag_jobs(self, deployment_id, guids=None, component_instance_ids=None, statuses=None):
        url = self._catalog_api_host + '/rosbag-jobs/{}'.format(deployment_id)
        query_params = {}
        if guids:
            query_params.update({'guid': guids})
        if component_instance_ids:
            query_params.update({'componentInstanceID': component_instance_ids})
        if statuses:
            query_params.update({'status': statuses})
        return self._execute(url, HttpMethod.GET, query_params=query_params)

    @response_validator(True)
    def list_rosbag_jobs_in_project(self, device_ids):
        url = self._catalog_api_host + '/rosbag-jobs'
        query_params = {'deviceID': device_ids}
        return self._execute(url, HttpMethod.GET, query_params=query_params)

    @response_validator(True)
    def stop_rosbag_jobs(self, deployment_id, guids=None, component_instance_ids=None):
        url = self._catalog_api_host + '/rosbag-jobs/{}'.format(deployment_id)
        query_params = {}
        if guids:
            query_params.update({'guid': guids})
        if component_instance_ids:
            query_params.update({'componentInstanceID': component_instance_ids})
        return self._execute(url, HttpMethod.PATCH, query_params=query_params)

    @response_validator(True)
    def list_rosbag_blobs(self, guids=None, deployment_ids=None, component_instance_ids=None,
                          job_ids=None, statuses=None, device_ids=None):
        url = self._catalog_api_host + '/rosbag-blobs'
        query_params = {}
        if guids:
            query_params.update({'guid': guids})
        if deployment_ids:
            query_params.update({'deploymentID': deployment_ids})
        if component_instance_ids:
            query_params.update({'componentInstanceID': component_instance_ids})
        if statuses:
            query_params.update({'status': statuses})
        if job_ids:
            query_params.update({'jobID': job_ids})
        if device_ids:
            query_params.update({'deviceID': device_ids})
        return self._execute(url, HttpMethod.GET, query_params=query_params)

    @response_validator(True)
    def get_blob_download_url(self, guid):
        url = self._catalog_api_host + '/rosbag-blobs/{}/file'.format(guid)
        return self._execute(url, HttpMethod.GET)

    @staticmethod
    def download_blob(signed_url, filename, download_dir):
        response = RestClient(signed_url).method(HttpMethod.GET).execute()
        if not filename:
            content_disposition = response.headers.get('Content-Disposition')
            filename = re.findall("filename=(.+)", content_disposition)[0]
        filepath = os.path.join(download_dir, filename) if download_dir else filename
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024 * 1024):
                f.write(chunk)

    @response_validator(True)
    def delete_rosbag_blob(self, guid):
        url = self._catalog_api_host + '/rosbag-blobs/{}'.format(guid)
        return self._execute(url, HttpMethod.DELETE)
