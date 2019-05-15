# Project

API that does voice transcription.

## Technologies used

#### AWS API Gateway: for building the api
Scalability up and down automatically based on requests

Integrated with AWS Services such Lambda 

Pyload modeling and Transformation

#### AWS Lambda: for the operational tasks
Designed for short tasks.

Serverless : No resource management needed, we can focus only on the tasks needed.

Scalability.

Integration with AWS Services such as API Gateway, S3 and Transcribe.

#### AWS S3: for storing files(input and output) 
Scalability

No management needed

Integration with AWS services such as Lambda and Transcribe.

#### AWS Transcribe

###### These technologies are very cost effective, we're charged only based on the usage.


### Overview

A post request containing the audio file is send to API Gateway, where it's encoded to base64(to be able to upload the file without corrupting it), API Gateway passes the payload through to Lambda where the body(containing the base64 encoded file) is decoded and then stored in an s3 bucket. 

After that, Lambda configures and starts the AWS transcribe job and returns the Transcribe output url(made public on s3) as response to API Gateway, which sends it as a response the the request. 


the API works in an asynchronous way:

Send request with the input file, and receive response containing the result url.

The reason for the asynchronous choice is that AWS Transcribe can take time, sending the result url while the processing is taking place in the background allows the request sender to focus resources on something else(other than waiting).

The uploaded file and the result file are both available on s3.

### Architecture

![alt text](Architecture.jpg)

## Running the tests

from a terminal 
```
curl -X POST -F "data=@test_file.mp3" https://cybu70ogsc.execute-api.us-east-2.amazonaws.com/Dep1 -H "Content-Type: application/json"
```
Expected output:
```
{
 "statusCode": 200, 
 "transcript_url": "result_url", 
 "Message": "Information about the status"
}
```

AWS Transcribe takes some time to process the uploaded file, so it is advised to wait a minute or two(or more depending on the size of the uploaded file) to get the results from the URL.

I have chosen to return a url with the entire Transcription Job output:

```
{
"jobName":"job_name_2019_05_14_22_24_23",
"accountId":"213727552267",
"results":
{
"transcripts":[{"transcript":"MP three Track two, eh? Three. See? D f g age I Jay. Okay. L m end. Oh, P Q oh, s t you v w eggs. Why, zed?"}],
"items":[{"start_time":"0.04","end_time":"0.48","alternatives":[{"confidence":"0.9976","content":"MP"}],"type":"pronunciation"},{"start_time":"0.48","end_time":"0.94","alternatives":[{"confidence":"1.0000","content":"three"}],"type":"pronunciation"},{"start_time":"0.94","end_time":"1.36","alternatives":[{"confidence":"0.9944","content":"Track"}],"type":"pronunciation"},{"start_time":"1.36","end_time":"1.95","alternatives":[{"confidence":"0.5919","content":"two"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":","}],"type":"punctuation"},{"start_time":"3.94","end_time":"4.45","alternatives":[{"confidence":"0.3676","content":"eh"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"?"}],"type":"punctuation"},{"start_time":"6.44","end_time":"6.85","alternatives":[{"confidence":"0.7749","content":"Three"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"."}],"type":"punctuation"},{"start_time":"8.78","end_time":"9.35","alternatives":[{"confidence":"0.8869","content":"See"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"?"}],"type":"punctuation"},{"start_time":"11.34","end_time":"11.75","alternatives":[{"confidence":"0.6026","content":"D"}],"type":"pronunciation"},{"start_time":"16.14","end_time":"16.65","alternatives":[{"confidence":"0.8998","content":"f"}],"type":"pronunciation"},{"start_time":"18.58","end_time":"19.15","alternatives":[{"confidence":"0.7295","content":"g"}],"type":"pronunciation"},{"start_time":"21.04","end_time":"21.65","alternatives":[{"confidence":"0.9997","content":"age"}],"type":"pronunciation"},{"start_time":"23.54","end_time":"24.15","alternatives":[{"confidence":"0.8907","content":"I"}],"type":"pronunciation"},{"start_time":"26.04","end_time":"26.65","alternatives":[{"confidence":"0.5380","content":"Jay"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"."}],"type":"punctuation"},{"start_time":"28.54","end_time":"29.05","alternatives":[{"confidence":"0.7501","content":"Okay"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"."}],"type":"punctuation"},{"start_time":"31.04","end_time":"31.55","alternatives":[{"confidence":"0.8761","content":"L"}],"type":"pronunciation"},{"start_time":"33.44","end_time":"33.95","alternatives":[{"confidence":"0.3752","content":"m"}],"type":"pronunciation"},{"start_time":"35.87","end_time":"36.35","alternatives":[{"confidence":"0.6399","content":"end"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"."}],"type":"punctuation"},{"start_time":"38.34","end_time":"38.85","alternatives":[{"confidence":"0.9014","content":"Oh"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":","}],"type":"punctuation"},{"start_time":"40.74","end_time":"41.36","alternatives":[{"confidence":"0.8961","content":"P"}],"type":"pronunciation"},{"start_time":"43.34","end_time":"43.95","alternatives":[{"confidence":"0.8035","content":"Q"}],"type":"pronunciation"},{"start_time":"45.84","end_time":"46.35","alternatives":[{"confidence":"0.9052","content":"oh"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":","}],"type":"punctuation"},{"start_time":"48.34","end_time":"48.85","alternatives":[{"confidence":"0.8489","content":"s"}],"type":"pronunciation"},{"start_time":"50.84","end_time":"51.35","alternatives":[{"confidence":"0.5171","content":"t"}],"type":"pronunciation"},{"start_time":"53.34","end_time":"53.95","alternatives":[{"confidence":"0.6907","content":"you"}],"type":"pronunciation"},{"start_time":"55.84","end_time":"56.45","alternatives":[{"confidence":"0.6307","content":"v"}],"type":"pronunciation"},{"start_time":"58.4","end_time":"59.05","alternatives":[{"confidence":"0.9995","content":"w"}],"type":"pronunciation"},{"start_time":"60.94","end_time":"61.55","alternatives":[{"confidence":"0.9864","content":"eggs"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"."}],"type":"punctuation"},{"start_time":"63.49","end_time":"64.05","alternatives":[{"confidence":"1.0000","content":"Why"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":","}],"type":"punctuation"},{"start_time":"66.0","end_time":"66.55","alternatives":[{"confidence":"0.7173","content":"zed"}],"type":"pronunciation"},{"alternatives":[{"confidence":null,"content":"?"}],"type":"punctuation"}]
},
"status":"COMPLETED"
}
```

or a simply a post request with the audio file from an API development environment(such as POSTMAN) to the address https://cybu70ogsc.execute-api.us-east-2.amazonaws.com/Dep1

Needless to say, this can also be integrated in other applications.

## Code
The main code is for the Lambda function.

Because Python library base64 which is external (not available in AWS SDK) was used, the code has been packaged as a Python Deployment package and uploaded to Lambda.

(In a nutshell, the python deployment package contains the lambda code in addition to the site packages of a virtual environment where are the needed libraries are installed) 

Some configurations were done for API Gateway(Payload Transformation) and S3 buckets permissions, but no major code.

Screen_shorts directory contains screen shorts of the different services used.

## Improvements:
Many improvements can be added here:
- Improvements or changes should be made with the intended production use in mind.
- Lambda is very convenient for fault tolerence, but proper Error handling can be added to deliver meaningful information.
- The result can be tailored as needed as opposed to deliver it as it is.
- More strict security policies can be applied to the output file access on s3(depending on the use case)
- Add Logging and Monitoring Features.

