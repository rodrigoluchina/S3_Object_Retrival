# S3 File Search and Download Project

## Description
This project allows you to search for and download files from an S3 bucket based on phone numbers stored in JSON files.A structured folder tree is created recursively on your local machine.

![demonstrative_png](https://github.com/rodrigoluchina/S3_Object_Retrival/blob/main/assets/main.png)

## Setup

### Prerequisites
- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/repository-name.git
   cd repository-name

2. python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. pip install -r requirements.txt

4. pyinstaller --onefile --windowed s3_object_retrival_script.py to build the project


### AWS CLI Configuration

**You need CLI configured in order to the program execute correcly**

**Configuring using AWS CLI commands**

    For general use, the aws configure or aws configure sso commands in your preferred terminal are the fastest way to set up your AWS CLI installation. Based on the credential method you prefer, the AWS CLI prompts you for the relevant information. By default, the information in this profile is used when you run an AWS CLI command that doesn't explicitly specify a profile to use.

        This example is for the short-term credentials from AWS Identity and Access Management. The aws configure wizard is used to set initial values and then the aws configure set command assigns the last value needed.


        $ aws configure
        AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
        AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
        Default region name [None]: us-west-2
        Default output format [None]: json
        $ aws configure set aws_session_token fcZib3JpZ2luX2IQoJb3JpZ2luX2IQoJb3JpZ2luX2IQoJb3JpZ2luX2IQoJb3JpZVERYLONGSTRINGEXAMPLE

