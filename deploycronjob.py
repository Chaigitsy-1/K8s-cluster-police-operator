
import kopf
#import kubernetes.config as k8s_config
#import kubernetes.client as k8s_client
import logging

import zlib
import hashlib
from kubernetes import client, config
import requests
@kopf.on.update('operators.chaigitsy-1.github.com', 'v1', 'clusterpolices')
@kopf.on.create('operators.chaigitsy-1.github.com', 'v1', 'clusterpolices')
def on_create(body, **kwargs):
    print(f"An ClusterPolice CRD IS CREATED WITH THIS BODY: {body}")
    crd_name = body['metadata']['name']
    crd_namespace = body['metadata']['namespace']
    healthcheckport= spec['port']
	labels= spec['labels']
	healthcheckendpoint=spec['healthcheckendpoint']
	interval=spec['interval']
	timeout=spec['timeout']
	retries=spec['retries']
	maillist=spec['maillist']
	smtpdetails=spec['smtpdetails']
	smtpport=spec['smtpport']
	
    #config.load_kube_config()
    #api = client.BatchV1beta1Api()

                  
    body = {
    "apiVersion": "batch/v1",
    "kind": "CronJob",
    "metadata": {


        "name": "{}".format(crd_name),
        "namespace": "{}".format(crd_namespace),

    },
    "spec": {
        "concurrencyPolicy": "Allow",
        "failedJobsHistoryLimit": 1,
        "jobTemplate": {

            "spec": {
                "template": {

                    "spec": {
                        "containers": [
                            {

                                "image": "chaigistyoperator:latest",
                                "imagePullPolicy": "IfNotPresent",
                                "name": "{}".format(crd_name),
                                "args": [retries,healthcheckport, healthcheckendpoint, crd_namespace,labels, maillist, smtpdetails, smtpport ,interval, timeout]
                                
                            }
                        ]
                    }
                }
            }
        },
        "schedule": "* * * * *",
        "successfulJobsHistoryLimit": 3,
        "suspend": false
                  }

            }
            
            
    try:
        logging.info("Trying load kube config")
        config.load_kube_config()
        logging.info("Done!")
    except config.ConfigException:
        config.load_incluster_config()
    )
    
    try:
        logging.info("Trying Cronjob Creation")
        v1 = client.BatchV1Api(
        ret = v1.create_namespaced_cron_job(namespace=crd_namespace, body=body, pretty=True,
                                            _preload_content=False, async_req=False)
        ret_dict = json.loads(ret.data)
        print(f'create succeed\n{json.dumps(ret_dict)}')
        logging.info("CronJob Created")
    except client.rest.ApiException as e:
        if e.status == 409:
            logging.info("Cronjob already exists")
        else:
            raise e    





if __name__ == '__main__':
    kopf.run()

	