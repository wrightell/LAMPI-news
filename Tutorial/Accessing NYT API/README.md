## Step 1: Creating API accounts
This project utilizes the NYT API. You can get started by following the [directions](https://developer.nytimes.com/get-started) to create an account, and build an app to get the API license key. Once you sign up, create an app, this one is called LAMPI-News and I gave it access to the Article Search, Times Wire, and Top Stories APIs. 

## Step 2: Adding API keys to Environment
Since we don't want to hardcode our API keys in our code we can add them to our environment. Copy the key from your App in the NYT Developer portal. In the ec2 instance write
```
nano ~/.bashrc
```
add the following line to the end of the file:
```
export NYT_API_KEY="<YOUR-KEY-HERE>"
```
Save and exit the file. To make the changes, run:
```
source ~/.bashrc
```