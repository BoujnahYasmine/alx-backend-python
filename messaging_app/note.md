# General flow of the CI/CD pipeline and DevOps process
## Summary of each step and its role in modern DevOps, CI/CD, and containerized deployments

1. Development (App Building):
This is the preliminary stage of the whole software development process. At this stage, developers - both Frontend and Backend, develop their applications respectively. This is where containerization of the application starts. During the development stage, developers may use different versions of packages and libraries, which, when merging code together, might result in conflicts and dependency issues. Dockerizing your application helps solve this issue.

Developers save their dependencies in a file, e.g., in Python, `requirements.txt`, and in JavaScript, `package.json`. Once they have this in place, they can create a configuration to build a Docker image in a file called `Dockerfile` and specify the packages to install with their versions inside that image. Once the code is pushed, other developers working on it can create an image and run a container based on the Dockerfile. This ensures that they have the same environment and the same dependencies. With Docker, you do not need to install all of these dependencies on your local machine as you can just install them on your image or container, and that's all.

### Example: Dockerizing a Python Application

1. **Create a `requirements.txt` file**:
    ```plaintext
    flask==2.0.1
    requests==2.25.1
    ```
Above file content can be achieve in python application by using this:
    ```bash
    pip freeze > requirements.txt
    ```

2. **Create a `Dockerfile`**:
    ```dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.8-slim

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Make port 80 available to the world outside this container
    EXPOSE 80

    # Define environment variable
    ENV NAME World

    # Run app.py when the container launches
    CMD ["python3", "app.py"]
    ```

3. **Build the Docker image**:
    ```bash
    docker build -t my-python-app .
    ```

4. **Run the Docker container**:
    ```bash
    docker run -p 4000:80 my-python-app
    ```
### N.B:
    In some cases, you might need to access the shell inthe command, to do so, use the command below to access as the root user:
     ```bash
    docker exec -it --user root jenkins-container bash
    ```

### Example: Dockerizing a Node.js Application

1. **Create a [package.json](http://_vscodecontentref_/0) file**:
    ```json
    {
      "name": "my-node-app",
      "version": "1.0.0",
      "description": "A simple Node.js application",
      "main": "app.js",
      "scripts": {
        "start": "node app.js"
      },
      "dependencies": {
        "express": "^4.17.1"
      }
    }
    ```

2. **Create a `Dockerfile`**:
    ```dockerfile
    # Use an official Node runtime as a parent image
    FROM node:14

    # Set the working directory in the container
    WORKDIR /usr/src/app

    # Copy package.json and package-lock.json
    COPY package*.json ./

    # Install app dependencies
    RUN npm install

    # Bundle app source
    COPY . .

    # Make port 8080 available to the world outside this container
    EXPOSE 8080

    # Define environment variable
    ENV NODE_ENV=production

    # Run app.js when the container launches
    CMD ["node", "app.js"]
    ```

3. **Build the Docker image**:
    ```bash
    docker build -t my-node-app .
    ```

4. **Run the Docker container**:
    ```bash
    docker run -p 8080:8080 my-node-app
    ```

By following these steps, developers can ensure that their applications run consistently across different environments, avoiding the "it works on my machine" problem. Docker provides a standardized unit of software that packages up code and all its dependencies, making it easier to develop, ship, and run applications.

2. # CI/CD (Continuous Integration/Continuous Deployment)

## What is CI/CD?

CI/CD stands for Continuous Integration and Continuous Deployment/Delivery. It is a method to frequently deliver apps to customers by introducing automation into the stages of app development. The main concepts attributed to CI/CD are continuous integration, continuous deployment, and continuous delivery.

### Continuous Integration (CI)

CI is a development practice where developers integrate code into a shared repository frequently, preferably several times a day. Each integration can then be verified by an automated build and automated tests. CI aims to detect and fix integration issues earlier, improve software quality, and reduce the time it takes to validate and release new software updates.

### Continuous Deployment (CD)

CD is a software release process that uses automated testing to validate whether changes to a codebase are correct and stable for immediate autonomous deployment to a production environment. CD ensures that software can be reliably released at any time.

## Uses of CI/CD

- **Automated Testing**: Ensures that code changes do not break the existing functionality.
- **Automated Deployment**: Reduces the manual effort required to deploy applications.
- **Faster Release Cycles**: Enables more frequent releases of software.
- **Improved Collaboration**: Encourages collaboration among team members by integrating changes frequently.

## Advantages of CI/CD

- **Early Bug Detection**: Bugs are detected early in the development cycle.
- **Reduced Integration Issues**: Frequent integration reduces the risk of integration issues.
- **Faster Time to Market**: Automated processes speed up the release cycle.
- **Consistent Delivery**: Ensures consistent and reliable delivery of software.
- **Improved Quality**: Automated testing and deployment improve the overall quality of the software.

## Setting Up CI/CD

### Example with Jenkins
### What is Jenkins?
Jenkins is an open-source automation server designed to help developers and teams automate tasks related to building, testing, and deploying software. It's a key tool in the DevOps ecosystem because it simplifies continuous integration (CI) and continuous delivery (CD), ensuring that code changes are automatically tested and deployed quickly and reliably.

Think of Jenkins as your software-building assistant — it automates repetitive tasks so developers can focus on writing code instead of worrying about deployment, testing, or builds.

#### Why Use Jenkins?
- Automation: Automates tasks like building your code, running tests, and deploying to servers.
- Continuous Integration (CI): Allows developers to merge their code changes into a shared repository multiple times a day, with automated testing to catch issues early.
- Continuous Delivery (CD): Streamlines the process of delivering new code to production, reducing downtime.
- Plugins: Offers over 1,800 plugins to integrate with tools like GitHub, Docker, Kubernetes, Slack, and more.
- Customizable Pipelines: Lets you create pipelines (sequences of steps) to define how your code is built, tested, and deployed.
- Containerized Workflows: Build Docker images for your application and push them to container registries like Docker Hub.

1. **Install Jenkins**: Run jenkins in a docker container by executing the following command
    ```bash
    docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
    ```
    **This command will**:
    - Pull the latest Long-Term Support (LTS) Jenkins image.
    - Expose Jenkins on port 8080.
    - Map the Jenkins home directory to the host machine to persist data.

2. **Configure Jenkins**:
    - Get your admin password by running this command:
    ```bash
       # Open interactive shell of the jenkins container
        docker -exec -it --user root <name of your jenkins container>
    ```
    ```bash
       # Run this to get the admin password
        cat /var/lib/jenkins/secrets/initialAdminPassword
    ```
    - Access Jenkins at `http://localhost:8080`
    - Input your admin password when propted
    - Follow the setup wizard to install recommended plugins and create an admin user.
    - Create your first pipeline or job.

3. **Setting up a Jenkins Pipeline**:
    - Create a New Pipeline Job:
    - Go to the Jenkins dashboard, click "New Item", and select "Pipeline".
    - Write a Jenkinsfile: A Jenkinsfile defines your CI/CD pipeline. Example below
    
    ```groovy
        pipeline {
            agent any
            stages {
                stage('Build') {
                    steps {
                        echo 'Building the application...'
                    }
                }
                stage('Test') {
                    steps {
                        echo 'Running tests...'
                    }
                }
                stage('Deploy') {
                    steps {
                        echo 'Deploying the application...'
                    }
                }
            }
        }
    ```
4. **Run the Pipeline**:
    - Save the job and click "Build Now" to see your pipeline execute step by step.

### Example with GitHub Actions

1. **Create a GitHub Actions Workflow**:
    - Create a `.github/workflows/main.yml` file in your repository.

    ```yaml
    name: CI/CD Pipeline

    on:
      push:
        branches:
          - main

    jobs:
      build:
        runs-on: ubuntu-latest

        steps:
        - name: Checkout code
          uses: actions/checkout@v2

        - name: Set up Node.js
          uses: actions/setup-node@v2
          with:
            node-version: '14'

        - name: Install dependencies
          run: npm install

        - name: Run tests
          run: npm test

        - name: Build project
          run: npm run build

        - name: Deploy
          run: npm run deploy
    ```

## Jenkins vs. GitHub Actions

### Jenkins

- **Pros**:
  - Highly customizable with a wide range of plugins.
  - Can be hosted on-premises, providing more control over the environment.
  - Supports complex workflows and pipelines.

- **Cons**:
  - Requires maintenance and management of the Jenkins server.
  - Steeper learning curve for beginners.

### GitHub Actions

- **Pros**:
  - Integrated with GitHub, making it easy to set up and use.
  - No need to manage servers or infrastructure.
  - Supports a wide range of actions and workflows.

- **Cons**:
  - Limited to GitHub repositories.
  - Less customizable compared to Jenkins.

## Differences Between CI and CD

- **Continuous Integration (CI)**:
  - Focuses on integrating code changes frequently.
  - Automated builds and tests are run to ensure code quality.
  - Aims to detect and fix integration issues early.

- **Continuous Deployment (CD)**:
  - Focuses on deploying code changes automatically to production.
  - Ensures that the code is always in a deployable state.
  - Reduces the manual effort required for deployment.

By implementing CI/CD, development teams can improve their workflow, reduce errors, and deliver high-quality software more efficiently.