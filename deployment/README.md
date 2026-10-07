# In-cluster GitHub Actions runner

The repository workflows use the ARC runner scale set named `arc-mlops`. The
runner only executes Python and Jupyter commands; it does not build images, use
Docker-in-Docker, mount the Docker socket, or require a Kubernetes service
account.

## Install

1. Apply [`namespace.yaml`](namespace.yaml) and install the Actions Runner
   Controller components in the cluster following
   the ARC documentation.
2. Create a namespace for the runner and a GitHub App or personal access token
   secret named `arc-github-secret`. Keep the secret outside this repository.
3. Install the runner scale set chart using
   [`arc-runner-values.yaml`](arc-runner-values.yaml), replacing the GitHub
   URL and namespace as needed.
4. Verify that the scale set advertises the `arc-mlops` runner label before
   enabling the workflows on the `development` branch.

The values intentionally set `minRunners: 0`, `runAsNonRoot`,
`allowPrivilegeEscalation: false`, and dropped Linux capabilities. The runner
also has service-account token automounting disabled because the workflow does
not call the Kubernetes API.

## KFP endpoint

ARC jobs set:

```text
http://ml-pipeline.kubeflow.svc.cluster.local:8888
```

Local development keeps the default `http://localhost:8080`. Start a port
forward before running the script or notebook locally:

```sh
kubectl port-forward svc/ml-pipeline-ui -n kubeflow 8080:80
```

To override either environment, set `KFP_ENDPOINT`. The endpoint is read by
`src/submit_run.py` and the notebook when they create the KFP client.