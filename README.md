# MetaML

Easily train and serve ML models on Kubernetes, directly from your python code.

> MetaML only supports TensorFlow currently

## Overview

MetaML allows you to express how you want your model to be trained and served using native python decorators.  

```python
@Train(
    package={'name': 'some_image_name', 'repository': 'some_docker_repo', 'publish': True},
    options={
      'hyper_parameters': {'learning_rate': random.normalvariate(0.5, 0.5)},
    },
    tensorboard={
      'log_dir': '/some/path',
    }
)
def my_training_function(learning_rate):
  # some training logic
  ...
```

### Backends

Currently, MetaML supports two backends:
* `Native`: This is the default backend. Your trainings will be deployed using only Kubernete's `Job` object. This works with any Kubernetes cluster, but this backend only support 'embarassingly parallel' trainings.
* `Kubeflow`: This requires having [Kubeflow](https://github.com/kubeflow/kubeflow) pre-installed in your Kubernetes cluster. Trainings will be deployed using the `TfJob` custom object instead, allowing for distributed training.

### `@Train` decorator

The `Train` decorator takes 4 arguments:

* `package`: Defines the repository (this could be your DockerHub username, or something like `somerepo.acr.io` on Azure for example) and name that should be used to build the image. You can control wether you want to publish the image by setting `publish` to `True`.

* `options`: These are the options specific to the training itself
  * `parallelism`: How many trainings should run in parallel? Default to `1`.
  * `completion`: [Only for `Native` backend] How many trainings should run in total. If omitted, this will be set to the value of `parallelism`.
  * `hyper_parameters`: What hyperparameters should be used for each training. You can either pass an object (in which case every instance will receive the same values) or a function (the function will be called separatly in every instance, allowing you to explore the HP space).

* `tensorboard`: [Optional] If specified, will spawn an instance of TensorBoard to monitor your trainings
  * `log_dir`: Directory where the summaries are saved.
  * `pvc_name`: Name of an existing `PermanentVolumeClaim` that should be mounted.
  * `public`: If set to `True` then a public IP will be created for TensorBoard (provided your Kubernetes cluster supports this). Otherwise only a private IP will be created.

* `backend`: Which backend to use.

### `@Serve` decorator

This decorator is not yet implemented

## Installing

**This projects requires python 3**

#### `metaparticle-ast`

This project uses a fork of `metaparticle-ast` for now, that need to be installed from source as well:

```bash
go get github.com/metaparticle-io/metaparticle-ast
cd $GOPATH/src/github.com/metaparticle-io/metaparticle-ast
git remote add wbuchwalter https://github.com/wbuchwalter/metaparticle-ast
git pull wbuchwalter master

go get -d ./cmd/compiler/
rm -rf $GOPATH/src/github.com/kubeflow/tf-operator/vendor
go install ./cmd/compiler/mp-compiler.go
```

#### MetaML

```bash
git clone https://github.com/wbuchwalter/metaml
cd metaml
python setup.py install
```
