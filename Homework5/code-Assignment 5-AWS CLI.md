### Assignment 5

aws configure

aws s3 presign s3://assignment-git/sample2.jpg

% the link：<https://assignment-git.s3.us-east-1.amazonaws.com/sample2.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA5S3BCOZLD65F7A4D%2F20250423%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250423T202650Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=e3c992af4f2cb954bb9bd05604dbcae08daa3987fae45bd0b3150f4cb9d405c2>

% the screenshot:&#x20;

![](<code-Assignment 5_md_files/bdee5ab0-2081-11f0-9312-9bfb4c8d073e.jpeg?v=1&type=image>)

aws s3 cp "H:/DE/DE Lecture/Homework5/sample3.jpg" s3://assignment-git/
upload: H:\DE\DE Lecture\Homework5\sample3.jpg to s3://assignment-git/sample3.jpg
