import sys
import time
import smtplib
from email.mime.text import MIMEText
from kubernetes import client, config
import json
import requests
def get_services_with_label(namespace, label_selector):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    final_services=[]
    services = v1.list_service_for_all_namespaces().items
    for service in services:
        test_data=label_selector
        print(test_data)
        #test_data={'app':'nginx'}
        data=service.spec.selector
        print(data)
        try:
            for key, value in test_data.items():
                if key not in data or data[key] != value:
                    pass
                else:
                    final_services.append(service.metadata.name)
        except:
            print("exception")




    return final_services




def ping_service(service, port, endpoint, retry_count, smtp_mail_list, smtp_server, smtp_port,namespace):
    config.load_incluster_config()
    #v1=client.CoreV1Api()
    service_name = service
    namespace = namespace
    failed_services = []

    for i in range(retry_count):
        try:
            #api_client = client.ApiClient()
            #response = api_client.call_api(
             #   f"/api/v1/namespaces/{namespace}/services/{service_name}:{port}{endpoint}",
              #  "GET",
               # _preload_content=False,
                #response_type="object"
            #)
            url=f"http://{service}:{port}/{endpoint}"
            response= requests.get(url)
            if response.status_code == 200:
                print(f"Service {service_name} is healthy.")
                return
        except Exception as e:
            print(f"Error pinging service {service_name}: {str(e)}")

        if i < retry_count - 1:
            time.sleep(1)  # Wait for 1 second before retrying
        else:
            failed_services.append(service_name)

    if failed_services:
        send_notification_email(smtp_mail_list, smtp_server, smtp_port, failed_services)


def send_notification_email(mail_list, smtp_server, smtp_port, failed_services):
    sender = 'sender@example.com'
    subject = 'Service Health Check Failed'
    message = f"The following services are not responding to health checks: {' '.join(failed_services)}"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(mail_list)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.sendmail(sender, mail_list, msg.as_string())
        print("Notification email sent successfully.")
    except Exception as e:
        print(f"Error sending notification email: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: python clusterpolice.py <retry_count> <port> <endpoint> <namespace> <label_selector> <mail_list> <smtp_server> <smtp_port>")


    retry_count = int(sys.argv[1])
    port = int(sys.argv[2])
    endpoint = sys.argv[3]
    namespace = sys.argv[4]
    selector_labels = sys.argv[5]
    mail_list = sys.argv[6].split(',')
    smtp_server = sys.argv[7]
    smtp_port = int(sys.argv[8])
    # Load the in-cluster configuration
    config.load_incluster_config()

    # Create a Kubernetes client
    api = client.CoreV1Api()
    label_selector='{'+selector_labels+'}'
    print("labels")
    print(label_selector)

    # Retrieve the token from the default ServiceAccount
    token = open('/var/run/secrets/kubernetes.io/serviceaccount/token').read()

    # Configure the API client with the token
    configuration = client.Configuration()
    configuration.host = 'https://kubernetes.default.svc'  # The Kubernetes API server's Service DNS name
    configuration.verify_ssl = False  # Only set to False for testing or insecure environments
    configuration.debug = False  # Set to True for verbose output
    configuration.api_key = {
    'authorization': 'Bearer {}'.format(token)
    }

    # Set the API client configuration
    api.api_client.configuration = configuration
    services = get_services_with_label(namespace, label_selector)
    print(services)
    for service in services:
        ping_service(service, port, endpoint, retry_count, mail_list, smtp_server, smtp_port,namespace)
