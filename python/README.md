Google Cloud Functions
======================

The Python function is run as a "Google Cloud Function". This allows for minimal configuration,
you essentially write your function and deploy. The code for Google cloud functions is required to be in main.py by 
Google.

Setup
-----
To use Google Cloud functions, you must have a
[Google cloud services](https://cloud.google.com/functions/docs/create-deploy-gcloud#functions-deploy-command-python) 
account with billing enabled. You will also need to enable some APIs to use cloud functions, they should be outlined in 
the quickstart docs linked before. When 
[deploying the function](https://cloud.google.com/functions/docs/create-deploy-gcloud#deploying_the_function)
be sure to replace the word REGION with a valid [region name](https://cloud.google.com/functions/docs/locations).
The code which you are deploying should live in [main.py](https://github.com/JR-SRUSA/JR-SRUSA.github.io/python/main.py)
and the --entry-point=FUNCTION_NAME.

See the [main.py](https://github.com/JR-SRUSA/JR-SRUSA.github.io/python/main.py) header for how to deploy and test the function.

Alternatively you can deploy and edit code directly from the 
[cloud functions dashboard](https://console.cloud.google.com/functions/). Click on your project link and then you can 
view the source, logs, etc. for that project.