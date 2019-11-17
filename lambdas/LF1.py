import json
import boto3
from botocore.vendored import requests
import time


def lambda_handler(event, context):
    # TODO implement
    #print(json.dumps(event, indent=4, sort_keys=True))
    #bucket_name = 'photoboy'
    #key_name = 'download.jpg'
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    #print(bucket_name)
    client = boto3.client('rekognition')
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    resp = client.detect_labels(Image=pass_object)
    #print('<---------Now response object---------->')
    #print(json.dumps(resp, indent=4, sort_keys=True))
    timestamp =time.time()
    #timestamp = event['Records'][0]['eventTime']
    #timestamp = timestamp[:-5]
    labels = []
    #temp = resp['Labels'][0]['Name']
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    print('<------------Now label list----------------->')
    print(labels)
    #print('<------------Now required json-------------->')
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    #required_json = json.dumps(format)
    #print(required_json)
    url = "https://vpc-photos-b4al4b3cnk5jcfbvlrgxxu3vhu.us-east-1.es.amazonaws.com/photos/0"
    headers = {"Content-Type": "application/json"}
    #url2 = "https://vpc-photos-b4al4b3cnk5jcfbvlrgxxu3vhu.us-east-1.es.amazonaws.com/photos/_search?pretty=true&q=*:*"
    r = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers)
    #resp_elastic = requests.get(url2,headers={"Content-Type": "application/json"}).json()
    #print('<------------------GET-------------------->')
    print(r.text)
    #print(json.dumps(resp_elastic, indent=4, sort_keys=True))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
