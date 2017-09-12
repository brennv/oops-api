# oops-api

Curated search for issues related to Docker, Kubernetes and OpenShift

See: [oops.vonapp.co](http://oops.vonapp.co)

## Endpoints

### search

GET **/api/search/{issue}**  Generic search

### openshift

GET **/api/search/openshift/{issue}** Search openshift docs and bugs

GET **/api/search/openshift/bugs/{issue}** Search openshift bugs

GET **/api/search/openshift/docs/{issue}** Search openshift docs

#### Example response

```
[
  {
    title: "GlusterFS pods don't start · Issue #4452 · openshift ...",
    url: "https://github.com/openshift/openshift-ansible/issues/4452",
    snippet: "openshift -ansible - OpenShift ... I'm trying to deploy openshift with hyper-converged glusterfs pos on nodes but glusterfs pods don't start. ... Error syncing pod ..."
  },
  {
    title: "Bug 1395183 - Unable to create pods",
    url: "https://bugzilla.redhat.com/show_bug.cgi?id=1395183",
    snippet: "Description of problem: Unable to start simple hello-openshift pods. Version-Release number of selected component (if applicable): $ oc version oc v3.4.0.23+24b1a58 ..."
  },
  ..

]
```

### status

GET **/api/health** API health check
