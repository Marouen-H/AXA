import json
import time
import boto3
import base64

def lambda_handler(event, context):
    # TODO implement
    

    data = base64.b64decode(base64.b64decode(event["data"].encode()))

    AWS_INPUT_BUCKET_NAME = 'hm-s3bucket'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(AWS_INPUT_BUCKET_NAME)

    
    EXT = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())
    
    #Upload file to s3
    PATH = 'file_'+EXT+'.mp3'
    bucket.put_object(
         ACL='public-read',
         ContentType='audio/mpeg',
         Key=PATH,
         Body=data,
    )



    JOB_NAME = 'job_name_'+EXT
    JOB_URI = 'https://s3.us-east-2.amazonaws.com/hm-s3bucket/'+PATH
    AWS_OUTPUT_BUCKET_NAME = "hm-s3bucket-transcript-results"

    #Start the Transcription
    transcribe = boto3.client('transcribe')
    transcribe.start_transcription_job(
         TranscriptionJobName=JOB_NAME,
         Media={'MediaFileUri': JOB_URI},
         OutputBucketName = AWS_OUTPUT_BUCKET_NAME,
         MediaFormat='mp3',
         LanguageCode='en-US'
     )

    #Wait for the transcription JOb to finish and retreive result
    #while True:
    #status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    #    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
    #        break
    #    time.sleep(5)
        
    #Retreive the transcription text
    #data = s3.get_object(Bucket= AWS_OUTPUT_BUCKET_NAME, Key=job_name+'.json')
    #contents = data['Body'].read()
    #contents = json.loads(contents)

    outputfile = 'https://s3.us-east-2.amazonaws.com/'+AWS_OUTPUT_BUCKET_NAME+'/'+job_name+'.json'
    
    return {
        'statusCode': 200,
        'transcript_url' : outputfile,
        'Message' : 'Processing in progress, it could take some time depending on the size of the input file'
    }
    