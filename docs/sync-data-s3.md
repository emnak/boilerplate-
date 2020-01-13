# Synchronize your S3 data (Sicara GPU)
Before syncing your data, you need to configure your [access to Muaddib first](access_muaddib.md).
- SSH on muaddib:
   ```
   ssh muaddib
   ```
- Create your personal data folder in `/media/HDD/data`:
    ```
    mkdir /media/HDD/data/{YOUR_NAME}
    ``` 
    eg `mkdir /media/HDD/data/antoinet`

- Synchronize your s3 bucket: 
    ```
    aws s3 sync s3://{YOUR_S3_BUCKET} /data/{YOUR_NAME}
     ```
     eg `aws s3 sync s3://totem-polyaxon /media/HDD/data/antoinet --profile=leto`
- Disconnect from muaddib
    ```
    exit
    ```

Notes:

- It is important that you create your own personal folders. 
- AWS CLI is already associated with the account of Leto. If you want to use your own S3 data, 
you would have to either
    - **configure a new profile** `aws configure --profile={MY_PROFILE}`. Then sync your data with:
    ```
    aws s3 sync s3://{YOUR_S3_BUCKET} /media/HDD/data/{YOUR_NAME} --profile={MY_PROFILE}
    ```
    - **use you credentials in the command line**:
    ```
    AWS_ACCESS_KEY_ID={YOUR_AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY={YOUR_AWS_SECRET_ACCESS_KEY} aws s3 cp s3://{YOUR_S3_BUCKET} /media/HDD/data/{YOUR_NAME}
    ```
