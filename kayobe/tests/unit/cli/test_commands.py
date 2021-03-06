# Copyright (c) 2017 StackHPC Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

import cliff.app
import cliff.commandmanager
import mock

from kayobe.cli import commands
from kayobe import utils


class TestApp(cliff.app.App):

    def __init__(self):
        super(TestApp, self).__init__(
            description='Test app',
            version='0.1',
            command_manager=cliff.commandmanager.CommandManager('kayobe.cli'))


class TestCase(unittest.TestCase):

    @mock.patch.object(utils, "galaxy_install", spec=True)
    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_control_host_bootstrap(self, mock_run, mock_install):
        command = commands.ControlHostBootstrap(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        mock_install.assert_called_once_with("requirements.yml",
                                             "ansible/roles")
        expected_calls = [
            mock.call(mock.ANY, ["ansible/bootstrap.yml"]),
            mock.call(mock.ANY, ["ansible/kolla-ansible.yml"],
                      tags="install"),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(utils, "galaxy_install", spec=True)
    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_control_host_upgrade(self, mock_run, mock_install):
        command = commands.ControlHostUpgrade(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        mock_install.assert_called_once_with("requirements.yml",
                                             "ansible/roles", force=True)
        expected_calls = [
            mock.call(mock.ANY, ["ansible/bootstrap.yml"]),
            mock.call(mock.ANY, ["ansible/kolla-ansible.yml"],
                      tags="install"),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_network_connectivity_check(self, mock_run):
        command = commands.NetworkConnectivityCheck(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(mock.ANY, ["ansible/network-connectivity.yml"]),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_seed_container_image_build(self, mock_run):
        command = commands.SeedContainerImageBuild(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(
                mock.ANY,
                [
                    "ansible/container-image-builders-check.yml",
                    "ansible/kolla-build.yml",
                    "ansible/container-image-build.yml"
                ],
                extra_vars={
                    "container_image_sets": (
                        "{{ seed_container_image_sets }}"),
                    "push_images": False,
                }
            ),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_seed_container_image_build_with_regex(self, mock_run):
        command = commands.SeedContainerImageBuild(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args(["--push", "^regex1$", "^regex2$"])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(
                mock.ANY,
                [
                    "ansible/container-image-builders-check.yml",
                    "ansible/kolla-build.yml",
                    "ansible/container-image-build.yml"
                ],
                extra_vars={
                    "container_image_regexes": "'^regex1$ ^regex2$'",
                    "push_images": True,
                }
            ),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_overcloud_container_image_build(self, mock_run):
        command = commands.OvercloudContainerImageBuild(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(
                mock.ANY,
                [
                    "ansible/container-image-builders-check.yml",
                    "ansible/kolla-build.yml",
                    "ansible/container-image-build.yml"
                ],
                extra_vars={
                    "container_image_sets": (
                        "{{ overcloud_container_image_sets }}"),
                    "push_images": False,
                }
            ),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_overcloud_container_image_build_with_regex(self, mock_run):
        command = commands.OvercloudContainerImageBuild(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args(["--push", "^regex1$", "^regex2$"])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(
                mock.ANY,
                [
                    "ansible/container-image-builders-check.yml",
                    "ansible/kolla-build.yml",
                    "ansible/container-image-build.yml"
                ],
                extra_vars={
                    "container_image_regexes": "'^regex1$ ^regex2$'",
                    "push_images": True,
                }
            ),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_baremetal_compute_inspect(self, mock_run):
        command = commands.BaremetalComputeInspect(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(
                mock.ANY,
                [
                    "ansible/baremetal-compute-inspect.yml",
                ],
            ),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_baremetal_compute_manage(self, mock_run):
        command = commands.BaremetalComputeManage(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(
                mock.ANY,
                [
                    "ansible/baremetal-compute-manage.yml",
                ],
            ),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)

    @mock.patch.object(commands.KayobeAnsibleMixin,
                       "run_kayobe_playbooks")
    def test_baremetal_compute_provide(self, mock_run):
        command = commands.BaremetalComputeProvide(TestApp(), [])
        parser = command.get_parser("test")
        parsed_args = parser.parse_args([])
        result = command.run(parsed_args)
        self.assertEqual(0, result)
        expected_calls = [
            mock.call(
                mock.ANY,
                [
                    "ansible/baremetal-compute-provide.yml",
                ],
            ),
        ]
        self.assertEqual(expected_calls, mock_run.call_args_list)
