# Polyaxon Platform and Kubernetes cluster

[Polyaxon](https://docs.polyaxon.com) is a platform for reproducing and managing ML experiments.
It is installed on a Kubernetes cluster that runs either on-premise or in the Cloud (AWS, Google Cloud, Azure).

- If you are starting a new project, you need to install Polyaxon and create a Kubernetes cluster.
- If you want to quickly test an experiment, you can use Polyaxon on Muaddib.

## Installing Polyaxon for a new project

In order to launch ML pipelines (trainings, inferences), you will need an account on [Polyaxon](https://docs.polyaxon.com).

To install Polyaxon and to setup a Kubernetes cluster, have a look at the [Leto's documentation](https://github.com/sicara/leto-documentation).

## Using Polyaxon on Muaddib for testing purpose

Muaddib is the GPU Sicara server on-premise that is physically at Sicara.
It has two RTX2080 GPUs.

Kubernetes ([microk8](https://microk8s.io/)) and Polyaxon are installed on Muaddib.
You can access [the Polyaxon web UI here](http://10.20.200.125:32116/app/sicara). Ask the Leto Team for credentials.
