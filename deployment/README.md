# In-cluster GitHub Actions runner

The repository workflows use the ARC runner scale set named `arc-mlops`. The
runner only executes Python and Jupyter commands; it does not build images, use
Docker-in-Docker, mount the Docker socket, or require a Kubernetes service
account.

## Install

1. Install the ARC controller chart in an `arc-system` namespace following the
   [ARC documentation](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller).
2. Apply [`namespace.yaml`](namespace.yaml).
3. Create a GitHub App or personal access token secret named
   `arc-github-secret` in the `arc-runners` namespace. Keep the secret outside
   this repository. For a pre-created secret, the supported keys are
   `github_token`, or `github_app_id`, `github_app_installation_id`, and
   `github_app_private_key`.
4. Install the runner scale set chart:

   ```sh
   helm install arc-mlops \
     --namespace arc-runners \
     -f deployment/arc-runner-values.yaml \
     oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
   ```

5. Verify that the scale set is ready and advertises the `arc-mlops` runner
   label before enabling the workflows on the `development` branch:

   ```sh
   kubectl get autoscalingrunnerset -n arc-runners
   kubectl get pods -n arc-runners
   ```

The cluster must also provide network access from the runner pod to both
`github.com`/GitHub Container Registry and the Kubeflow service in the
`kubeflow` namespace. The runner image is pulled from
`ghcr.io/actions/actions-runner:latest`; pin it to a tested digest for
production use.

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