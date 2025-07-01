import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # get the parameters from the event object to calculate the sum of two numbers
    a = event['a']
    b = event['b']

    result = calculate_sum(a, b)
    print(f'The sum result is {result}')

    logger.info(f"CloudWatch logs group: {context.log_group_name}")

    # return the sum as a json string
    data = {"sum": result}
    return json.dumps(data)


def calculate_sum(a, b):
    return a + b
