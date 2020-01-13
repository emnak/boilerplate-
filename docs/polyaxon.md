# How to use Polyaxon on Sicara's clusters


This page explains how to start an experiment on a Polyaxon cluster:
1. [Prerequisistes](#prerequisites)
2. [Configure Polyaxon CLI on your local machine](#configure-polyaxon-cli-on-your-local-machine)
3. [Create a Polyaxon Project](#create-a-polyaxon-project)
4. [Polyaxon Experiments](#polyaxon-experiments)

If you need more details on Polyaxon, check the more complete [Notion doc](https://www.notion.so/m33/Polyaxon-2897e58e5e5e4f9c965e5e6f3fdc1a0b).

---


## Prerequisites
> - You need **Polyaxon-CLI** installed to interact with the cluster (it is in your dev-requirements).
> - You need **Polyaxon passwords**. Follow this
> [doc](https://www.notion.so/m33/Retrieve-Sicara-Tech-Passwords-acbb30b767bb4c1e91a3b0880ec97f3b)
> to get Sicara's technical Passwords.


---


## Configure Polyaxon CLI on your local machine

- On your machine, connect to the cluster with the Polyaxon-CLI:
    - `polyaxon config set --host=10.20.200.125 --http_port=32116` for Muaddib
- Login with the Sicara user and fill in the **Polyaxon password**:
    ```
    polyaxon login --username=sicara
    ```
- Check that you can see the cluster with `polyaxon cluster`


---


## Polyaxon Projects

Polyaxon experiments are run inside a Project. Thus, you need to create or checkout to an exisiting one.


#### Create a Polyaxon project

- To create {YOUR_PROJECT}, simply enter
    ```
    polyaxon project create --name {YOUR_PROJECT} --init
    ```
    Write `no` when asked to override the .polyaxonignore file



#### Switch to an existing Polyaxon project

- To checkout on an already created project {YOUR_PROJECT}, simply enter
    ```
    polyaxon init {YOUR_PROJECT}
    ```
    Write `no` when asked to override the .polyaxonignore file
> The keyword `init` is not really explicit but it is the counterpart of the git `checkout`


---


## Polyaxon Experiments

Training your Networks can be achieved with Polyaxon by running "Experiments". They are run inside a project
and are described by a simple yaml.


#### Run a Polyaxon experiment

First, you need to create a Yaml file in the `experiments` folder. To do so, you can look at the experiment files that are in the
[experiment folder](experiments). For instance,
[a simple CNN experiment](../experiments/fashion-mnist-simple-cnn-experiment.yaml)
which downloads the [fashion mnist](https://github.com/zalandoresearch/fashion-mnist) dataset and launches a training with a simple cnn.

In your experiment YAML, you will need to fill paths for - if existing - `data` on the Polyaxon cluster.
To put data on Muaddib, check this [page](docs/sync-data-s3.md).

To run the experiment on Polyaxon:
```
polyaxon run -u -f experiments/{YOUR_EXPERIMENT}.yaml --name {EXPERIMENT_NAME}
```
where `{YOUR_EXPERIMENT}.yaml` is the name of your Polyyaxon experiment file, and `{EXPERIMENT_NAME}` is
an optional given name which can help you retrieve your experiment in the Polyaxon Dashboard.

Results of your experiment will be found in the directory you provided in the .yaml file.
By default, you will find them in `/output/sicara/{YOUR_PROJECT}/experiments/{POLYAXON_EXPERIMENT_ID}`

**Notes** :
- In the `polyaxon run` command:
  - `-u` allows to upload the code on the cluster
  - `-f` allows to provide the file `experiments/my_experiment.yaml` through the Polyaxon CLI.


#### Stop a polyaxon experiment
Stopping using the UI interface does not work properly. You should use the following polyaxon-cli command line to stop
an experiment:
```bash
polyaxon experiment -xp <Experiment Id> stop
```


##### Download a polyaxon experiment results
Run `./scripts/download_experiment_result.sh -p <Project Name> -e <Experiment Id>` with the id of the experiment.

For instance, for the boilerplate project on Polyaxon:
`scripts/download_experiment_result.sh -p boilerplate -e 21672`

The results will be downloaded in the `polyaxon-results` folder.



## Monitor your experiment


#### Polyaxon Dashboard

The Polyaxon Dashboard allows to retrieve, monitor your experiments, and download their outputs  within your Web Browser.
It can access at:
- http://10.20.200.125:32116 for Muaddib


#### Tensorboard


- Launch Tensorboard for your project:
    ```
    polyaxon tensorboard -p {YOUR_PROJECT} start
    ```
- Launch Tensorboard for an experiment:
    ```
    polyaxon tensorboard -xp {POLYAXON_EXPERIMENT_ID} start
    ```

You then can access it within the Polyaxon Dashboard.

Notes:
- Don't forget to stop tensorboard if you have finished to you use it. Otherwise it will consume some RAM on Muaddib
and might lead to crash and slowdowns.
```
polyaxon tensorboard -p {YOUR_PROJECT} stop
```


## Troubleshooting
If your Tensorboard failed to start, it might be because you forgot to shut it down the last time you used it.
Try:
```
polyaxon tensorboard -p {YOUR_PROJECT} stop
polyaxon tensorboard -p {YOUR_PROJECT} start
```
