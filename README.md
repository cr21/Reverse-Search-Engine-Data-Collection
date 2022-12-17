# Embedding based Image Search Engine DataCollection
This Repository contains code for data collection which is required to train Embedding Based Image Search Engine.

# Architecture
![Imgur](https://i.imgur.com/wia4HB0.png)
![Imgur](https://i.imgur.com/iZOr5Eh.png)

## Actions Workflow 
1. On push checkout the code and create docker container on git-hub server.
2. Push the image to Ecr with production tag 
3. Once action push is completed pull and run the image on Ec2 instance.
![Imgur](https://i.imgur.com/UK6OKBy.png)
   
## Git-hub Configurations
```text
1. Go to setting -> actions -> runner
2. Add runner/ec2 instance by using X86_64 arc
3. Add pages for github
4. Go to secrets tab -> Repository secrets and add secrets 
```
## Route Details 
![Imgur](https://i.imgur.com/Zatc0p8.png)
1. **/fetch**  : To get labels currently present in the database. Important to call as it updates in memory database.
2. **/Single_upload** : This Api Should be used to upload single image to s3 bucket
3. **/add_label** :  This api should be ued to add new label in s3 bucket.

## Infrastructure Details
- S3 Bucket 
- Mongo Database
- Elastic Container Registry
- Elastic Compute Cloud

## Steps
1. Create data folder 
2. Put archive.zip in data folder 
3. run s3 setup and mongo setup
4. Done

## To Replicate [ Requirements ]
```yaml
aws_cli:
  download: True
  configure: True
  
S3_Configurations:
  create_bucket: <bucket-name>
  region: <bucket-region>
  access: public-access [ To all the images ]

Mongo_configuration:
  mongo_url: <url-with-id-pass>

```
## Env variable

```bash

export ATLAS_CLUSTER_USERNAME=<username>
export ATLAS_CLUSTER_PASSWORD=<password>

export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_REGION=<region>

export AWS_BUCKET_NAME=<AWS_BUCKET_NAME>
export AWS_ECR_LOGIN_URI=<AWS_ECR_LOGIN_URI>
export ECR_REPOSITORY_NAME=<name>
export ECR_REPOSITORY_URI=<name>
export DATABASE_NAME=<name>
```

## Cost Involved
- For s3 bucket    :  Since we are using S3 Standard `$0.023 per GB`
- For Ec2 Instance :  Since we are using t2.small with 20Gb storage 1vCpu and 2Gb ram `$0.0248 USD per hour`
- For Mysql : Since we are using `$db.t3.micro` Free tier.
- For ECR : Storage is $0.10 per GB / month for data stored in private or public repositories.
