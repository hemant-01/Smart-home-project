Please make use of the README file while executing the script
1) Code has been written in Python. All the necessary technical details are provided as comments.
2) The high level architechture of communication is provided in the report. The same has been followed in the implementation.
3) The main points of code implementation and design choice is explained in Part 1 of the video. Part 2_1 and 2_2 contains the demo of the execution. It would be really helpful to understand our implementation if both the videos are watched.
4) The Lambda.py file should be present of the AWS
5) The alexa.py file must be on the local host. Except the Gateway Link, nothing needs to be changed in the script.
6) credentials.db and all_device_db.db will be automatically created when we execute the alexa.py.
7) terminal_log file has the log observed as we carry on the particular user actions.
8) The secret_key is a pre-shared value between the AWS and the particular registered user of AWS. This is similar to how Microsoft provides it's OS with a pre-shared unique key for each device which installs legitimate Windows. The _**secret_key**_ is sent by the _**local_system**_ to the AWS while sending the parameters. The _**secret_key**_ is verified to be correct by the AWS to _**authenticate the user**_. All of this happens over a secure HTTPS channel, thus providing guarantees when sending data over the channel(Internet).
