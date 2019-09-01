# drone-nebula

CI/CD build status: [![Build Status](https://cloud.drone.io/api/badges/nebula-orchestrator/drone-nebula/status.svg)](https://cloud.drone.io/naorlivne/drone-nebula)

Code coverage: [![codecov](https://codecov.io/gh/nebula-orchestrator/drone-nebula/branch/master/graph/badge.svg)](https://codecov.io/gh/naorlivne/drone-nebula)

Drone plugin for deploying to [nebula](https://dcos.github.io/nebula/).

Drone plugin to build and publish Docker images to a container registry. For the usage information and a listing of the available options please take a look at [the docs](http://plugins.drone.io/drone-plugins/drone-docker/).

## Usage

This plugin can be used to deploy applications to a nebula server, it will create\update the given nebula tasks as needed.

The below pipeline configuration demonstrates simple usage:

> In addition to the `.drone.yml` file you will need to create a `nebula.json` file that contains the nebula configuration as well as the "app_name" field. Please see [here](test/test_files/nebula.json) for an example. 

```yaml
pipeline:
name: default

steps:
- name: nebula_deploy
  image: nebulaorchestrator/drone-nebula
  settings:
    nebula_host: http://127.0.01
    nebula_job_file: nebula.json
```

### Value substitution

Example configuration with values substitution:
```yaml
pipeline:
name: default

steps:
- name: nebula_deploy
  image: nebulaorchestrator/drone-nebula
  settings:
    nebula_host: http://127.0.01
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

The nebula server URL (no trailing slash should be used)

#### nebula_job_file

The nebula configuration file location relative to the root folder of the repo, defaults to `nebula.json`
