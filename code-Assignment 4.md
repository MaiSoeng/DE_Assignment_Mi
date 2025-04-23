### **Assignment 4 Code**

% user management automation with AWS CLI

aws configure

aws iam create-user --user-name UserA

aws iam create-user --user-name UserB

aws iam create-user --user-name UserC

aws iam create-user --user-name UserD

aws iam create-user --user-name UserE

aws iam create-group --group-name Developers

aws iam create-group --group-name Testers

aws iam add-user-to-group --user-name UserA --group-name Developers

for user in UserC UserD UserE; do

aws iam add-user-to-group --user-name \$user --group-name Testers

done

aws iam create-login-profile \\

--user-name UserA \\

--password "TempPass123!" \\

--password-reset-required

for user in UserB UserC UserD UserE; do

aws iam create-login-profile \\

--user-name \$user \\

--password "TempPass123!" \\

--password-reset-required

Done

% restricting S3 bucket access using IAM policies and AWS CLI

pwd

ls

vim s3-readonly-policy.json

{

"Version": "2012-10-17",

"Statement": \[

{

"Effect": "Allow",

"Action": \[

"s3:Get\*",

"s3:List\*"

],

"Resource": \[

"arn:aws:s3:::techfusion-data",

"arn:aws:s3:::techfusion-data/\*"

]

}

]

}

aws iam create-policy \\

--policy-name TechFusionS3ReadOnly \\

--policy-document <file://s3-readonly-policy.json>

%% bucket policy created in the console

aws s3 ls s3://techfusion-data --profile UserA

aws s3 ls s3://techfusion-data --profile UserC

% manage and rotate access keys

aws iam create-access-key --user-name keyRotateUser

aws iam update-access-key \\

&#x20;\--user-name keyRotateUser \\

\--access-key-id AKIA5S3BCOZLCXGAMX27 \\

\--status Inactive

aws iam delete-access-key \\

\--user-name keyRotateUser \\

\--access-key-id AKIA5S3BCOZLCXGAMX27

% implementing and utilizing AWS CLI Profiles

aws configure
aws iam create-user --user-name prodUser
aws iam create-user --user-name devUser
aws configure --profile prodProfile for prodUser
aws iam create-access-key --user-name prodUser
aws iam create-access-key --user\=-name devUser
aws iam create-access-key --user-name devUser
aws configure --profile prodProfile
aws configure --profile devProfile
aws s3 ls
aws s3 ls --profile prodProfile
aws s3 ls --profile devUser
aws s3 ls --profile devProfile
pwd
ls
vim EC2-fullaccess.md
vim EC2-fullaccess.md

pwd
ls
vim EC2-full.md
aws iam put-user-policy --user-name devUser --policy-name EC2-full --policy-document file://EC2-full.json
ls
aws iam put-user-policy --user-name devUser --policy-name EC2-full --policy-document file://EC2-full.md
aws ec2 ls --profile devUser
aws ec2 ls --profile devProfile
aws ec2 describe-instances --profile devProfile

vim prod-policy.json
aws iam put-user-policy --user-name prodUser --policy-name prod-EC2 --policy-document file://prod-policy.json
aws ec2 describe-instances --profile prodProfile
aws ec2 describe-key-pairs --profile devProfile
aws ec2 describe-key-pairs --profile devProfile
aws ec2 describe-key-pairs --profile prodProfile
