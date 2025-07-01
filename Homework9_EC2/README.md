### Task 1

To implement Task 1, the following steps are shown below.

1.  Create a template.yaml file indicating that a lambda function will be applied to start or stop an EC2 instance.

2.  Write a handler function to recognize and check the event, and starts or stops the EC2 instance accordingly.

3.  Use powershell to execute the code to deploy the lambda function using AWS SAM.

    ![](README_md_files/977baf20-53a5-11f0-b17d-bb242a9eb7f2.jpeg?v=1&type=image)![](README_md_files/99d4ba50-53a5-11f0-b17d-bb242a9eb7f2.jpeg?v=1&type=image)![](README_md_files/9915d720-53a5-11f0-b17d-bb242a9eb7f2.jpeg?v=1&type=image)

4.  Create an EC2 instance using AWS console as a testing example

5.  Create two event files, EC2-start.json and EC2-stop.json, and implement the two events separately using AWS CLI.

6.  &#x20;Test EC2-start function and a log has been generated showing the start event successfully triggered.

    ![](README_md_files/3a2be180-53ac-11f0-95f4-1f6eab69fdc8.jpeg?v=1&type=image)

7.  Test EC2-stop function and a log has been generated showing the start event successfully triggered.

    ![](README_md_files/2415e3a0-53ac-11f0-95f4-1f6eab69fdc8.jpeg?v=1&type=image)![](README_md_files/2649daa0-53ac-11f0-95f4-1f6eab69fdc8.jpeg?v=1&type=image)

8.  Delete all the resources

### Task 2

To implement Task 2, the following steps are shown below.

1.  Create a template.yaml file to build an RDS instance and a lambda function.

2.  Write a handler function to recognize and check the event, and to perform basic database operations.&#x20;

3.  Use powershell to execute the code to deploy the lambda function using AWS SAM.

    ![](README_md_files/73cb0bf0-5604-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)

4.  Create a table in the RDS database. The table has three keys: name, age, user_id.

5.  Create four event files, RDS_Insert.json and RDS_Read.json, RDS_Update.json, RDS_Delete.json and implement these four events separately using AWS CLI.

6.  Test RDS_Insert function and a log has been generated showing the insert event successfully triggered.

    ![](README_md_files/9136d6b0-5609-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)

7.  Test RDS_Read function and a log has been generated showing the read event successfully triggered.

    ![](README_md_files/85f234b0-560a-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)

8.  Test RDS_Update function and a log has been generated showing the update event successfully triggered.

    ![](README_md_files/b9451a90-560e-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)

    ![](README_md_files/e7525970-560e-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)

9.  Test RDS_Delete function and a log has been generated showing the delete event successfully triggered.

![](README_md_files/3a238570-560f-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)

![](README_md_files/bc2a1ca0-560f-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)

1.  Delete all the resources

    ![](README_md_files/0d74f9f0-5614-11f0-845b-b31adf08ebfa.jpeg?v=1&type=image)
