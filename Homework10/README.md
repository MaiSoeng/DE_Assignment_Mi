### Task 1

1.  Create a simple lambda function (stored in src file, named app.py) to perform calculation between two numbers.

    ![](README_md_files/a0bce690-5642-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

2.  Track the lambda function metrics by looking at the monitor of the lambda function.

    ![](README_md_files/f4aabb40-5644-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

3.  Build a CloudWatch dashboard with invocations, duration, error count as Lambda metrics.

    ![](README_md_files/e65fe8b0-5646-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

4.  Set up a CloudWatch Alarm that triggers when the error rate (error / invocations) of the lambda function exceeds 1%.

    ![](README_md_files/14dbb5f0-5649-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

5.  a. View Lambda logs

    ![](README_md_files/62255320-5649-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

&#x20; b. Use CloudWatch logs insights to run queries and analyze logs. In this task, we are trying to find the sum results.

![](README_md_files/84996760-564a-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

1.  Create a CloudFormation template (template.yaml) including Lambda function, IAM Role, CloudWatch Log Group, Dashboard with 3 widgets, CloudWatch Alarm for error rate and deploy the template in CloudFormation to see if it matches previous results.&#x20;

    Once deployed, go to:

    Lambda Console to test the function

    CloudWatch Dashboard to view the created metrics

    Logs to check outputs

    Alarms to monitor threshold violations

    ![](README_md_files/6bed9ca0-56bc-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

    ![](README_md_files/3e4ff300-56bd-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

    ![](README_md_files/7a21d290-56bd-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

    ![](README_md_files/6b9582d0-56c2-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

    ![](README_md_files/7f66c0d0-56c2-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

    ![](README_md_files/ae076610-56c2-11f0-b7a9-7dc9d425238d.jpeg?v=1&type=image)

2.  Upload to GitHub and delete all the resources
