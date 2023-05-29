# K8s-cluster-police-operator
Writing an operator which tests all the services and their healthcheck endpoints every few minutes and also will trigger mails if it sees one of the endpoint is not responding by a 200

I have used v1.26 k8s cluster and also python client for kubernetes to write this operator

So wt are few considerations here

1. the smtp is password less , If its a password based mechanism i would suggest u to modify the code here to add smtp with ssl and password enabled https://github.com/Chaigitsy-1/K8s-cluster-police-operator/blob/f6eb84462bc3df9604e3c27bbac9830f4a04034d/clusterpolice/cronimage/clusterpolice.py#L81
2. The password above mentioned could be passed as party of crd and modified at cronimage and deploycronjob.py too

You guys are open to change and modify code or add functionalities in the way you want consider this is a basic one and i would like to develop this firther more

How to deploy and test:

Step1: clone this repo
Step2: cd clusterpolice/operator
Step3: kubectl apply -f clusterpolice/operator/rbac-op.yaml
(remember that https://github.com/Chaigitsy-1/K8s-cluster-police-operator/blob/ec8916ef95e0b7778686f7129f431337df8c189e/clusterpolice/operator/rbac-op.yaml#LL68C1-L69C35 this shld be replaced with namespace of serviceaccount)

Step4: kubectl apply -f deployment.yaml
Step5: cd clusterpolice/crds
Step6: kubectl apply -f crd.yaml
Step7: kubectl apply -f crd-deploy.yaml (with necessary changes you want to create in deploy.yaml)
