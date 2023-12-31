import json
import boto3

s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')

def create_transcription_job(job_name, job_uri, output_bucket):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        OutputBucketName=output_bucket,
        MediaFormat='mp4',
        # LanguageCode='auto',
        IdentifyLanguage=True,
        LanguageOptions=[ "ko-KR", "en-US", "ja-JP", "zh-CN"],
        Subtitles={'Formats': ['vtt', 'srt'], 'OutputStartIndex': 1}
    )
    
    return response

def lambda_handler(event, context):
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']

    job_name = f'transcription-job-{object_key}'
    job_uri = f's3://{bucket_name}/{object_key}'
    output_bucket = 'out-transcribe-subi'

    response = create_transcription_job(job_name, job_uri, output_bucket)
    print(f"Transcription job {job_name} has been started.")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Transcription job has been started.')
    }
