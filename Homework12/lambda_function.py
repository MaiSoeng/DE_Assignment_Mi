import base64
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    output = []

    for record in event['records']:
        try:
            # decode the base64 data 
            payload = base64.b64decode(record['data']).decode('utf-8')
            data = json.loads(payload)

            # extract the data 
            item_id = data.get('item_id')
            user_id = data.get('user_id')
            action = data.get('action')
            price = data.get('price')

            # transform the data
            category = 'Other'
            if item_id is not None:
                try:
                    item_id_int = int(item_id)
                    if 100 <= item_id_int < 250:
                        category = 'Clothing'
                    elif 250 <= item_id_int < 500:
                        category = 'Instruments'
                    elif 500 <= item_id_int < 750:
                        category = 'Electronics'
                    else:
                        category = 'Books'
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert item_id '{item_id}' to an integer. Defaulting to 'Other' category.")

            transformed_data = {
                'user_id': user_id,
                'item_id': item_id,
                'category': category,
                'price': price
            }

            encoded_data = base64.b64encode(json.dumps(transformed_data).encode('utf-8')).decode('utf-8')

            output.append({
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': encoded_data
            })
            
        except Exception as e:
            logger.error(f"Error processing record: {e}", exc_info=True)
            output.append({
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            })

    return {'records': output}