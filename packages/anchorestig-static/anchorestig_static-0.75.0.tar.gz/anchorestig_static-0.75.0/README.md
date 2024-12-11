# Anchore STIG

Anchore STIG is a complete STIG solution that can be used to run STIG profile against static images.

## Description

Use Anchore STIG to perform STIG checks against running containers in Kubernetes environments or static Docker images from a registry or stored locally. The tool executes automated scans against specific STIG Security Guide (SSG) policies. The program will output either a JSON report with a summary of STIG check results for runtime checks or XCCDF XML and OpenSCAP XML and HTML for static checks. 

The static functionality includes the following profiles:

* CentOS 7
* CentOS 8
* Debian 10
* Debian 11
* Fedora
* Oracle Linux 7
* Oracle Linux 8
* Oracle Linux 9
* OpenSUSE
* SUSE Linux Enterprise Server 15
* Red Hat Enterprise Linux 7
* Red Hat Enterprise Linux 8
* Red Hat Enterprise Linux 9
* Ubuntu 16.04
* Ubuntu 18.04
* Ubuntu 20.04
* Ubuntu 22.04

## Getting Started

### Dependencies

#### Overall
* `python3 >= 3.8 with pip3 installed`
* `make`

#### Static
* `docker`

#### Runtime
* `kubectl exec` privileges
* Pods running one of the above listed software / OS types


### Install

* clone the repo
* run `make` to install 

### Running the Program

#### Static

* Run the tool using `anchorestig static IMAGE`. 
    * Ex: `anchorestig static docker.io/ubi8:latest`

```
CLI Input Parameters:

Username:             --username (-u)     Username for private registry
Password:             --password (-p)     Password for private registry
Url:                  --url (-r)          URL for private registry
Insecure:             --insecure (-s)     Allow insecure registries or registries with custom certs
Local Image:          --local-image (-l)  Run against an image stored in your local docker instance
AWS S3 Bucket         --aws (-a)          Upload results to S3
Anchore Account       --account (-c)      Anchore STIG UI account to store the stig result in
```

##### Viewing Results

Navigate to the `./stig-results` directory. The output directory containing output files will be named according to the image scanned.

## Help

Use the `--help` flag to see more information on how to run the program:

`anchorestig --help`

## Authors

* Sean Fazenbaker 
[@bakenfazer](https://github.com/bakenfazer)
* Michael Simmons 
[@MSimmons7](https://github.com/MSimmons7)

<!-- ## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Anchore License - see the LICENSE.md file for details -->