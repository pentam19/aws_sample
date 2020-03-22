import json
import boto3
from datetime import datetime, timedelta, timezone

dynamodb = boto3.client('dynamodb', region_name='us-west-2')
table_name = 'my_test_table'
    

def change_capacity(read_capa):
    print("Change ReadCapacityUnits: "+str(read_capa))
    # DynamoDB change capacity
    # necessary DynamoDB Policy
    dynamodb.update_table(
        TableName=table_name,
        ProvisionedThroughput={
            'ReadCapacityUnits': read_capa,
            'WriteCapacityUnits': 1
        }
    )
    
# Cron 式 10 */1 ? * * *
def lambda_handler(event, context):
    # TODO implement 
    response = dynamodb.describe_table(
        TableName=table_name
    )
    print("now ReadCapacityUnits: "+str(response['Table']['ProvisionedThroughput']['ReadCapacityUnits']))
    print("now WriteCapacityUnits: "+str(response['Table']['ProvisionedThroughput']['WriteCapacityUnits']))

    # タイムゾーンの生成
    JST = timezone(timedelta(hours=+9), 'JST')
    timenow = datetime.now(JST)
    print("Hour: "+str(timenow.hour))
    print(type(timenow.hour))
    print("Minute: "+str(timenow.minute))
    print("WeekDay: "+str(timenow.weekday()))
    print(type(timenow.weekday()))
    yobi = ["月","火","水","木","金","土","日"]
    print("{}曜日".format(yobi[timenow.weekday()]))
    """
    Hour: 11
    <class 'int'>
    WeekDay: 6
    <class 'int'>
    日曜日
    """
    
    capacity_list = [
        {'weekday': 6, 'hour_jst': 12, 'read_capa': 2},
        {'weekday': 6, 'hour_jst': 13, 'read_capa': 3},
        {'weekday': 99, 'hour_jst': 14, 'read_capa': 1},
        {'weekday': 0, 'hour_jst': 15, 'read_capa': 2},
    ]
    for capa_setting in capacity_list:
        if timenow.weekday() == capa_setting['weekday'] or capa_setting['weekday'] == 99:
            if timenow.hour == capa_setting['hour_jst']:
                change_capacity(capa_setting['read_capa'])
                break
               
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
