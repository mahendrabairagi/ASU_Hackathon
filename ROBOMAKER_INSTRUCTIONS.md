ASU Hackathon Setup Instructions
================

AWS Robomaker is a service that makes it easy to create robotics applications at scale by extending the Robot Operating System (ROS) framework with cloud services.  Robomaker provides a robotics application development environment and simulation service, both of which speed up application development and testing.  The service also provides a fleet managerment service so you can deploy and manage applications remotely.

You'll be using Robomaker to build, bundle, and deploy your robot application to your robot.

Let's get started!

-----

### Create Infrastructure
1. Sign in to the AWS Management Console, type **S3** in the **Find Services** search bar and click to navigate to the service.

1. Choose the **Create Bucket** button to begin creating an S3 bucket

    - Bucket name: **\<Team-Name\>**-jetbot-detect
    - Region: **US East**

    ![S3 create bucket view](instructions/s3_create_bucket.png)

1. Click **Next** until reaching the **Review** step and click **Create Bucket**


### Creating a Development Environment
You'll be using the AWS RoboMaker IDE to develop your Robot Application.  This IDE is a cloud based development environment making used of a EC2 (Elastic Compute Cloud) instance.

1. Sign in to the AWS Management Console, type in **AWS RoboMaker** in the **Find Services** search bar and click to navigate to the service.

1. In the left navigation pane, choose **Development environments** and choose **Create Environment**.

1. Create a development environment with the following values:
    - General
        - Name: *Any name you choose*
        - Pre-installed Software suite: **ROS Melodic**
        - Instance type: **m4.xlarge**
    - Networking
        - VPC: **(Default)**
        - Subnets: **(us-east-1a)**

1. This opens the environment’s detail page, click Open environment, which will open a new browser tab with the Cloud9 IDE.

This may take a few minutes to complete, but when the creation process has completed, you will see something similar to this:

![Cloud9 development environment welcome view](https://robomakerworkshops.com/images/1_cloud9.png)

The Welcome page provides helpful information to get started, but for now we are not going to use it, so click the X on the tab to close.The IDE is broken down into four sections:j

![Cloud9 IDE layout](https://robomakerworkshops.com/images/1_c9_layout.png)


## Building a Robot Application with RoboMaker
### Clone software

1. Open the RoboMaker IDE and navigate to the terminal and clone this Git repo to the development machine:
    ```
    # change to the environment directory
    cd ~/environment

    git clone https://github.com/abest0/aws-nvidia-sample-robomaker-dino-detect.git jetbot-detect
    ```

1. Execute the `generate_greengrass_certs` script as follows:
    ```
    cd jetbot-detect

    # Generate greengrass certificates into the local repository
    ./scripts/generate_greengrass_certs.sh
    ```

### Setup build resources
1. Open the RoboMaker IDE and navigate to the console

1. Install Ubuntu dependencies:

    ```
    sudo apt install -y qemu-user-static
    ```

1. Change to the `jetbot-detect` directory &  Build the ARM64 docker container
    ```
    cd ~/environment/jetbot-detect/create-build-container

    docker build -t jetbot-detect .

    ```

    The name entered after `-t` is the name of your Docker image.  You'll need this to use this name
    to build and bundle in later stages

1. Verify you can start up a container and run a basic ROS command:

    ```
    # Change to the jetbot-detect
    $ docker run --rm -v $(pwd):/environment/jetbot-detect jetbot-detect rosversion -d

    # We should see the following result
    > melodic
    ```

### Build and Bundle
1. Open the RoboMaker IDE and navigate to the terminal

1. Change to the **jetbot-detect** directory and execute the `./scripts/build.sh` script
    ```
    # Build, bundle, and deploy the robot application to S3
    
    ./scripts/build.sh <DOCKER-IMAGE-NAME> <S3-BUCKET-NAME>
    ```


## Deploying with RoboMaker
When a robot application is deployed to a physical robot, AWS RoboMaker does the following:

- AWS RoboMaker creates or updates a custom Lambda in your account. The Lambda contains the logic needed for deployment. This includes robot application bundle download, ROS launch, pre- and post-checks, and other logic.

- AWS RoboMaker begins deployment to the fleet using the parallelization specified in the deployment configuration.

- AWS RoboMaker notifies AWS IoT Greengrass to run the custom Lambda on the target robot. The daemon running on the robot receives the command and runs the Lambda. If a Lambda is running when the command is received, it and all ROS process on the robot are terminated.

- The Lambda downloads and uncompresses the robot application bundle from Amazon S3. If a pre-launch script was specified, it is run. Then the Lambda starts ROS using the launch file and package specified. If a post-launch script was specified, it is run after ROS is started. Finally, the status of the deployment is updated.


### Create a Robot Application
1. Open the AWS RoboMaker console at https://console.aws.amazon.com/robomaker/

1. In the left pane, choose Development, and then choose Robot applications.

1. Select Create robot application.

1. In the Create robot application page, type a Name for the robot application. Choose a name that helps you identify the robot.

1. Select the Robot software suite used by your robot application. For more information about the Robot Operating System (ROS), see www.ros.org

1. Select the Software suite version used by your robot application.

1. Provide the Amazon S3 path to your bundled robot application file. If this robot application is used only in simulations, specify a bundle built for the X86_64 platform. If you use this robot application in a fleet deployment, specify one or more bundles that represent the architectures of the robots in your fleet.

1. Choose Create.

![Create Robot Application](instructions/create-robot-application.png)

#### Create a Robot Application Version
1. Open the AWS RoboMaker console at https://console.aws.amazon.com/robomaker/

1. In the left navigation pane, choose Development, and then choose Robot applications.

1. Choose the robot application name.

1. In the Robot applications details page, choose Create new version, and then choose Create.

### Create a Robot

To create a robot:

1. Sign in to the AWS RoboMaker console at https://console.aws.amazon.com/robomaker/

1. In the left navigation pane, choose Fleet Management, and then choose Robots.

1. Choose Create robot.

1. In the Create robot page, type a name for the robot.

1. Select the Architecture of the robot.
  1. Select the ARM64 architecture for the Sparkfun Robot

1. Under AWS IoT Greengrass group defaults, select a Create new to create a new AWS IoT Greengrass group for the robot. Optionally, you can select an existing AWS IoT Greengrass group. Each robot must have its own AWS IoT Greengrass group.

1. If you use an existing AWS IoT Greengrass group, it must have an IAM role associated with it. To create the role, see Create deployment role.

1. Optionally, modify the Greengrass prefix. This string is prepended to AWS IoT Greengrass objects created on your behalf.

1. Select a IAM role to assign to the AWS IoT Greengrass group created for the robot. It grants permissions for AWS IoT Greengrass to access your robot application in Amazon S3 and read update status from AWS RoboMaker.

1. Choose Create.
![Create Robot](instructions/create-robot.png)

1. In the Download your Core device page, choose Download to download and store your robot's security resources.

1. Download AWS IoT Greengrass core software matching the architecture of your physical robot. To configure and run the AWS IoT Greengrass core software, follow the steps in Module 1: Environment Setup for Greengrass. Then follow the steps in Start AWS Greengrass on the Core Device.

![Download robot certificates](instructions/download-robot-certs.png)


### Configure Robot with Certificates
1. Use the following command to unzip your security resources:

    ```
    $ sudo unzip RobotName-setup.zip -d /greengrass
    ```

### Create a Fleet
1. Sign in to the AWS RoboMaker console at https://console.aws.amazon.com/robomaker/

1. In the left navigation pane, choose Fleet Management, and then choose fleets.

1. Select Create fleet.

    - In the Create fleet page, type a name for the fleet.


1. Click Create to create the deployment job.

![Create a robot fleet to customize deployments](instructions/create-fleet-2.png)

#### Register a Robot

1. In the left navigation pane, choose Fleet Management, and then choose Fleets.

1. Select the Name of the fleet you want to modify.

1. In the Fleet details page, select Register.

1. In the Register robots page, select the robot you want to register, then select Register robots.

![Register a robot to a fleet](instructions/register-robot.png)


### Create a Deployment
1. Sign in to the AWS RoboMaker console at https://console.aws.amazon.com/robomaker/

1. In the left navigation pane, choose Fleet Management, and then choose Deployments.

1. Click Create deployment.

1. In the Create deployment page, under Configuration, select a Fleet.

1. Select a Robot application.

1. Select the Robot application version to deploy. The robot application must have a numbered `applicationVersion` for consistency reasons. If there are no versions listed, or to create a new version, see Creating a Robot Application Version.

1. Under Deployment launch config, specify the Package name.

1. Specify the Launch file.
  

1. Environment variables, type in an environment Name and Value. Environment variable names must start with A-Z or underscore and consist of A-Z, 0-9 and underscore. Names beginning with “AWS” are reserved.

    - Add the following environment variables:
        - **variable** = `MOTOR_CONTROLLER` **value** = `qwiic`

1. Specify a Robot deployment timeout. Deployment to an individual robot will stop if it does not complete before the amount of time specified.

1. Click Create to create the deployment job.

![Create a deployment of a robot application to a robot](instructions/create-deployment.png)


------

**Congratulations, you've just completed your very first deployment.**