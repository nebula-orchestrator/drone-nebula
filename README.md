# drone-nebula

CI/CD build status: [![Build Status](https://cloud.drone.io/api/badges/nebula-orchestrator/drone-nebula/status.svg)](https://cloud.drone.io/nebula-orchestrator/drone-nebula)

Code coverage: [![codecov](https://codecov.io/gh/nebula-orchestrator/drone-nebula/branch/master/graph/badge.svg)](https://codecov.io/gh/naorlivne/drone-nebula)

Drone plugin for deploying to [nebula](http://nebula-orchestrator.github.io/).

## Usage

This plugin can be used to deploy applications to a nebula server, it will create\update the given nebula tasks as needed.

The below pipeline configuration demonstrates simple usage:

> In addition to the `.drone.yml` file you will need to create a `nebula.json` file that contains the nebula configuration as well as the "app_name" field. Please see [here](test/test_files/nebula.json) for an example. 

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: nebula_deploy
  image: nebulaorchestrator/drone-nebula
  settings:
    nebula_host: my-nebula-host.com
    nebula_job_file: nebula.json
```

### Value substitution

Example configuration with values substitution:
```yaml
kind: pipeline
type: docker
name: default

steps:
- name: nebula_deploy
  image: nebulaorchestrator/drone-nebula
  settings:
    nebula_host: my-nebula-host.com
    nebula_job_file: nebula.json
    my_image_tag: my_dynamic_image
```

In the nebula.json file (please note the $ before the PLUGIN_MY_IMAGE_TAG key):

```json
{
  ...
  "image": "myrepo/myimage:$PLUGIN_MY_IMAGE_TAG",
  ...
}
```

will result in:

```json
{
  ...
  "image": "myrepo/myimage:my_dynamic_image",
  ...
}
```

## Parameter Reference

#### nebula_host

The nebula server FQDN\IP, defaults to "127.0.0.1"

#### nebula_job_file

The nebula configuration file location relative to the root folder of the repo, defaults to `nebula.json`

#### nebula_username

The nebula basic_auth username to use, defaults to None (no basic auth is used)

#### nebula_password

The nebula basic_auth password to use, defaults to None (no basic auth is used)

#### nebula_token

The nebula token_auth token to use, defaults to None (no token auth is used)


#### nebula_port

The nebula server port, defaults to 80

#### nebula_protocol

The nebula server protocol, defaults to "http"
