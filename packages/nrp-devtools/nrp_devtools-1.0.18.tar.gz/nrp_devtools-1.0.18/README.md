# NRP repository development tools

This tool is used to setup and run an Invenio based NRP instance. 

## Prerequisites

- Python 3.10
- node version 16 or greater, npm version 7, 8 or 10
- imagemagick and development packages for imagemagick
- standard build tools (gcc, make, ...), on ubuntu build-essential
- Docker 20.10.10+ and docker-compose 1.17.0+ (or OrbStack on Mac)

## Creating a new repository

1. Download the installer

```bash
curl -sSL https://raw.githubusercontent.com/oarepo/nrp-devtools/main/nrp-installer.sh
```

2. Run the installer with a directory where the repository will be created

```bash 
bash nrp-installer.sh my-repo
```

After asking a couple of questions, the installer will create the
repository in the `my-repo` directory.

It will also initialize git version control system and commit the initial
sources.

3. Go to the my-repo directory and see the README.md file there for further instructions
   (or have a peek at [README.md](https://github.com/oarepo/nrp-devtools/blob/main/src/nrp_devtools/templates/repository/%7B%7Bcookiecutter.repository_name%7D%7D/README.md) )