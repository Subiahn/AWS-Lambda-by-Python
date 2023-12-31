import json
import boto3

s3_client = boto3.client('s3')
translate_client = boto3.client('translate')

def translate_vtt_file(input_bucket, input_key, output_bucket, output_key, target_language):
    if not input_key.lower().endswith('.vtt'):
        # Skip if the file is not in VTT format
        return
    
    # Read the VTT file
    response = s3_client.get_object(Bucket=input_bucket, Key=input_key)
    vtt_content = response['Body'].read().decode('utf-8')
    
    # Translate the VTT content
    response = translate_client.translate_text(
        Text=vtt_content,
        SourceLanguageCode='auto',
        TargetLanguageCode=target_language
    )
    translated_text = response['TranslatedText']
    
    # Write the translated VTT content to the output bucket
    s3_client.put_object(Bucket=output_bucket, Key=output_key, Body=translated_text)
    print(f"Translated VTT file '{output_key}' has been created.")

def lambda_handler(event, context):
    record = event['Records'][0]
    input_bucket = record['s3']['bucket']['name']
    input_key = record['s3']['object']['key']
    output_bucket = 'out-translate-subi'
    target_language = 'en'  # Specify your target language code here

    output_key = f"translated_{input_key}"
    translate_vtt_file(input_bucket, input_key, output_bucket, output_key, target_language)

    return {
        'statusCode': 200,
        'body': json.dumps('Translation completed.')
    }
