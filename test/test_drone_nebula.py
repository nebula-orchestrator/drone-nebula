from unittest import TestCase, mock
from drone_nebula.drone_nebula_runner import *
import os
import requests_mock


test_files_location = os.getenv("TEST_FILES_LOCATION", "test_files")

app_creation_response_json_failure = "{\"app_exists\": true}"
app_creation_response_json_success = """
{
    \"app_id\": 1,
    \"app_name\": \"test12345\",
    \"starting_ports\": [
        80
    ],
    \"containers_per\": {
        \"cpu\": 5
    },
    \"env_vars\": {
        \"test\": \"test123\"
    },
    \"docker_image\": \"registry/nginx\",
    \"running\": true,
    \"networks\": [
        \"nebula\",
        \"bridge\"
    ],
    \"volumes\": [],
    \"devices\": [],
    \"privileged\": false,
    \"rolling_restart\": false
}
"""


class BaseTests(TestCase):

    def test_file_reader_read_file(self):
        reply = read_file(test_files_location + "/test_read_file")
        self.assertDictEqual(reply, {"check_this_out": "it_reads!"})

    def test_file_reader_read_file_raise_error_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file(test_files_location + "/non_existing_file")

    def test_read_all_envvars_to_dict_force_uppercase_false(self):
        test_envvars = {"TEST_ENV": "123", "test_env_lowercase": "456"}
        with mock.patch.dict(os.environ, test_envvars):
            reply = read_all_envvars_to_dict()
            self.assertEqual(type(reply), dict)
            self.assertEqual(reply["TEST_ENV"], "123")
            self.assertEqual(reply["test_env_lowercase"], "456")

    def test_populate_template_string_works_simple(self):
        test_template_values_dict = {"test": "test that works"}
        expected_reply = {"test": "this is a test that works"}
        reply = populate_template_string({"test": "this is a $test"}, test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_works_complex(self):
        test_template_values_dict = {"test1": "test that", "test2": "works"}
        expected_reply = {"test": "this is a $Complex$123 test that works"}
        reply = populate_template_string({"test": "this is a $Complex$123 $test1 $test2"}, test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_populate_template_string_no_template_values(self):
        test_template_values_dict = None
        expected_reply = {"test": "this is a $test"}
        reply = populate_template_string({"test": "this is a $test"}, test_template_values_dict)
        self.assertDictEqual(reply, expected_reply)

    def test_populate_template_string_no_template_values_no_template_placement(self):
        test_template_values_dict = None
        expected_reply = {"test": "this is a test"}
        reply = populate_template_string({"test": "this is a test"}, test_template_values_dict)
        self.assertEqual(reply, expected_reply)

    def test_nebula_init(self):
        test_nebula_connection = NebulaDeploy()
        self.assertEqual(test_nebula_connection.nebula_connection.API_VERSION, "v2")
        self.assertEqual(test_nebula_connection.nebula_connection.host, "http://127.0.0.1:80")
        self.assertEqual(test_nebula_connection.nebula_connection.password, None)
        self.assertEqual(test_nebula_connection.nebula_connection.port, 80)
        self.assertEqual(test_nebula_connection.nebula_connection.protocol, "http")
        self.assertEqual(test_nebula_connection.nebula_connection.request_timeout, 60)
        self.assertEqual(test_nebula_connection.nebula_connection.token, None)

    def test_nebula_check_nebula_app_exists_true(self):
        test_nebula_connection = NebulaDeploy()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.get('http://127.0.0.1:80/api/v2/apps/test_job', status_code=200,
                               text=app_creation_response_json_success)
            reply = test_nebula_connection.check_nebula_app_exists("test_job")
            self.assertTrue(reply)

    def test_nebula_check_nebula_app_exists_false(self):
        test_nebula_connection = NebulaDeploy()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.get('http://127.0.0.1:80/api/v2/apps/test_job', status_code=403,
                               text=app_creation_response_json_failure)
            reply = test_nebula_connection.check_nebula_app_exists("test_job")
            self.assertFalse(reply)

    def test_nebula_check_nebula_app_exists_connection_or_permission_issue(self):
        test_nebula_connection = NebulaDeploy(nebula_host="http://127.0.0.1")
        with requests_mock.Mocker() as request_mocker:
            request_mocker.get('http://127.0.0.1:80/api/v2/apps/test_job', status_code=500,
                               text=app_creation_response_json_failure)
            with self.assertRaises(Exception):
                test_nebula_connection.check_nebula_app_exists("test_job")

    def test_nebula_create_nebula_job(self):
        test_nebula_connection = NebulaDeploy()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.post('http://127.0.0.1:80/api/v2/apps/test', status_code=200,
                                text='{"test_json_key": "test_json_value"}')
            reply = test_nebula_connection.create_nebula_app({"app_name": "test"})
            self.assertDictEqual(reply, {'reply': {'test_json_key': 'test_json_value'}, 'status_code': 200})

    def test_nebula_create_nebula_job_failure(self):
        test_nebula_connection = NebulaDeploy(nebula_host="http://127.0.0.1")
        with requests_mock.Mocker() as request_mocker:
            request_mocker.post('http://127.0.0.1:80/api/v2/apps/test', status_code=401,
                                text='{"test_json_key": "test_json_value"}')
            with self.assertRaises(Exception):
                test_nebula_connection.create_nebula_app({"app_name": "test"})

    def test_nebula_update_nebula_app(self):
        test_nebula_connection = NebulaDeploy()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.post('http://127.0.0.1:80/api/v2/apps/test/update', status_code=200,
                               text='{"test_json_key": "test_json_value"}')
            reply = test_nebula_connection.update_nebula_app({"app_name": "test"})
            self.assertDictEqual(reply, {'status_code': 200, 'reply': {'test_json_key': 'test_json_value'}})

    def test_nebula_update_nebula_app_failure(self):
        test_nebula_connection = NebulaDeploy(nebula_host="http://127.0.0.1")
        with requests_mock.Mocker() as request_mocker:
            request_mocker.post('http://127.0.0.1:80/api/v2/apps/test/update', status_code=401,
                               text='{"test_json_key": "test_json_value"}')
            with self.assertRaises(Exception):
                test_nebula_connection.update_nebula_app({"app_name": "test"})

    def test_nebula_create_or_update_nebula_app_create(self):
        test_nebula_connection = NebulaDeploy()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.get('http://127.0.0.1:80/api/v2/apps/test', status_code=403,
                               text=app_creation_response_json_success)
            request_mocker.post('http://127.0.0.1:80/api/v2/apps/test', status_code=200,
                                text=app_creation_response_json_success)
            reply = test_nebula_connection.create_or_update_nebula_app({"app_name": "test"})
            self.assertDictEqual(reply["reply"]["env_vars"], {'test': 'test123'})
            self.assertEqual(reply["status_code"], 200)

    def test_nebula_create_or_update_nebula_app_update(self):
        test_nebula_connection = NebulaDeploy()
        with requests_mock.Mocker() as request_mocker:
            request_mocker.get('http://127.0.0.1:80/api/v2/apps/test', status_code=200,
                               text=app_creation_response_json_success)
            request_mocker.post('http://127.0.0.1:80/api/v2/apps/test/update', status_code=200,
                               text=app_creation_response_json_success)
            reply = test_nebula_connection.create_or_update_nebula_app({"app_name": "test"})
            self.assertDictEqual(reply["reply"]["env_vars"], {'test': 'test123'})
            self.assertEqual(reply["status_code"], 200)

    def test_main_init(self):
        test_envvars = {"PLUGIN_NEBULA_JOB_FILE": test_files_location + "/nebula.json"}
        with mock.patch.dict(os.environ, test_envvars):
            with requests_mock.Mocker() as request_mocker:
                request_mocker.get('http://127.0.0.1:80/api/v2/apps/example_app', status_code=200,
                                   text=app_creation_response_json_success)
                request_mocker.post('http://127.0.0.1:80/api/v2/apps/example_app/update', status_code=200,
                                    text=app_creation_response_json_success)
                init()
