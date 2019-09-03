from drone_nebula.functions.nebula_deploy.nebula_deployment import *
from drone_nebula.functions.envvars.envvars import *
from drone_nebula.functions.file.file import *
from parse_it import ParseIt
import os


def init():
    # read envvars
    print("reading envvars")
    parser = ParseIt(recurse=False, envvar_prefix="plugin_")
    nebula_host = parser.read_configuration_variable("nebula_host", required=True)
    nebula_username = parser.read_configuration_variable("nebula_username", default_value=None)
    nebula_password = parser.read_configuration_variable("nebula_password", default_value=None)
    nebula_token = parser.read_configuration_variable("nebula_token", default_value=None)
    nebula_port = parser.read_configuration_variable("nebula_port", default_value=80)
    nebula_protocol = parser.read_configuration_variable("nebula_protocol", default_value="http")
    nebula_job_file = parser.read_configuration_variable("nebula_job_file", default_value="nebula.json")
    nebula_job_type = parser.read_configuration_variable("nebula_job_type", default_value="app")
    nebula_job_file = os.getcwd() + "/" + nebula_job_file
    envvar_dict = read_all_envvars_to_dict()

    # get the job json
    print("reading nebula job json file")
    nebula_job_json = read_file(nebula_job_file)

    # populate the job json with the template data
    print("populating nebula job json file with the templated data")
    nebula_job_json = populate_template_string(nebula_job_json, envvar_dict)

    # create nebula connection object
    print("contacting nebula API")
    nebula_connection = NebulaDeploy(host=nebula_host, username=nebula_username, password=nebula_password,
                                     token=nebula_token, port=nebula_port, protocol=nebula_protocol)

    # update nebula
    if nebula_job_type == "app":
        nebula_connection.create_or_update_nebula_app(nebula_job_json)
    elif nebula_job_type == "cron_job":
        nebula_connection.create_or_update_nebula_cron_job(nebula_job_json)
    print("finished updating nebula")
