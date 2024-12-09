[![pipeline  status](https://gitlab.com/octomy/common/badges/production/pipeline.svg)](https://gitlab.com/octomy/common/-/commits/production)

<!---
                                                         
                                                         
     ## ## ## ## ## ## ## ## ## ## ##                    
        ## ## ## ## ## ## ## ## ##                       
           ## ## ## ## ## ## ##                          
              ## ## ## ## ##                             
                 ## ## ##                                
                    ##                                   
                                                         
                                                         
WARNING: This file is AUTO GENERATED from "resources/templates/README.md".
         Any changes you make will be OVERWRITTEN at the 
         next invocation of `make readme`                
                                                         
                                                         
                    ##                                   
                 ## ## ##                                
              ## ## ## ## ##                             
           ## ## ## ## ## ## ##                          
        ## ## ## ## ## ## ## ## ##                       
     ## ## ## ## ## ## ## ## ## ## ##                    
                                                         
                                                         
-->

#  Practical details
<img  src="https://gitlab.com/octomy/common/-/raw/production/resources/iamges/logos/1024.svg"  width="20%"/>

This is the common project version 1.0.47

- common is [available  on  gitlab](https://gitlab.com/octomy/common).
- common is [available as private Docker image](https://gitlab.com/octomy/common/container_registry).


```shell
#  Clone  git  repository
git  clone  git@gitlab.com:octomy/common.git
```

```shell
# Pull image from Docker registry
docker pull registry.gitlab.com/octomy/common

```


# What is common?

common is a pypi package that contains common  files  for  OctoMY™ Python projects.


```shell

#  Clone  git  repository

git  clone  git@gitlab.com:octomy/common.git
```

```shell
#  Install  package  into  your  current  Python  environment
pip  install  octomy-common
```

# Versioning

In this section the versioning scheme used for all octomy codebases will be explained.

First of, we strive to follow [semver](https://semver.org/) as far as possible, so any details pertaining to the actual version numbers themselves is better explained in the semver spec. This documentation refers to how we store, change and update the version number in the project itself, and how that version number is propagated from source to build artifacts such as PyPi packages, Docker images and more.

## Source of version number

The source of the version number shall be a one line, plain-text file in the root of the project simply called [VERSION](VERSION)

This should contain the full version number on semver format and nothing else. Example versions are:

* 0.0.1
* 0.1.3
* 1.0.0
* 2.2.12
> NOTE: There should not be any prefixes or postfixes in this version. No "rc", "beta" as this is handled by the logic as described below.

## git branches

We will operate with 3 protected git branches. The rules that govern them are as follows:

| Branch | Description |
| --------------- |--------------------------|
| production      | This corresponds to what is in production right now. Using CI/CD, anything merged to this branch will immediately be built and deployed in production, replacing whatever was in production before |
| beta      | This corresponds to what is in the beta environment right now. Using CI/CD, anything merged to this branch will immediately be built and deployed into the beta environment, replacing whatever was in that environment before. Beta means an almost ready "next version" that is ready to preview for a selection of customers. |
| stage-_XXX_      | This corresponds to what is in the stage environment labelled _XXX_ right now. Using CI/CD, anything merged to this branch will immediately be built and deployed into the  stage-_XXX_ environment, replacing whatever was in that environment before. Please note that the _XXX_ could be any string, you may have several stage environments labelled as you see fit. Typically you will have a stage set up for a private presentation to a select client, or for internal testing. |
| *      | Any other branch is considered unprotected and may be built and tested using CI/CD, but will not be considered for any automatic deployment. When built and deployed manually, these branches will have `test-`prepended to them for easy identification. |


## PyPi packages

PyPi package names are on the form `project_name`-`version` The branch name is omitted entirely and it is expected that PyPi packages are deployed only for the production branch.

## Docker images

Docker images are named `project_name` and tagged with `branch_name`-`version`. The branch name is omitted for "production" giving simply `version` in that case. Further, any branch name starting with `stage-` will have the `stage-` part removed. And finally, any branch that is not production, beta or stage-X will have `test-`prepended to the branch name itself, so it becomes  `version`-test-`branch_name`.

## Examples

* Example project name: __my_project__
* Example version: __1.2.3__
* Example stage name: __my_presentation__

| git branch name         | Docker image                               | PyPi package             |
| ----------------------- |--------------------------------------------| -------------------------|
| `production`            | my_project:_1.2.3_                         | my_project-_1.2.3_       |
| `beta`                  | my_project:_1.2.3_-`beta`                  | N/A                      |
| `stage-my_presentation` | my_project:_1.2.3_-`my_presentation`       | N/A                      |
| `silly_branch`          | my_project:_1.2.3_-__test__-`silly_branch` | N/A                      |

## Implementation

To maintain this versioning, we depend on a few tools for the logic:

1. bash
2. make
3. setup.py (Python)

Each octomy project will have a [Makefile](Makefile) in the root of the project that has targets for building and pushing pypi and/or Docker images. It [specifies bash as the shell](https://www.gnu.org/software/make/manual/html_node/Choosing-the-Shell.html) to use, and use [bash string manipulation and conditions](https://www.gnu.org/software/bash/manual/bash.html) to generate the correct version string following the rules above for Docker tags. Further, the rules are implemented as a function in setup.py to satisfy the rules when building pypi package.

The Makefile targets are named as follows:

| make target     | Description                                                    |
| --------------- |----------------------------------------------------------------|
| docker-build    | Build the docker image with correct version tags               |
| docker-push     | Push the docker image with correct version tags to registry    |
| pypi-build      | Build the pypi package with correct version                    |
| pypi-push       | Push the pypi package with correct version to PyPi repository. NOTE: Should only be called for production branch  |

## Example implementation

This octomy-common project will follow the rules above and will contain the Makefile targets that can be used as a reference for other projects.


