# IBM Generative AI Python SDK
This generative chatbot repository was created for Python AI Code Challenge at BrainSoft
## Access to this work:
- this work has been done and tested in linux (ubuntu) enviroment
- you can directly try this demo on my domain **vajpet.com**
- run `docker-compose up -d` to create package that can be access at you `localhost`
- or just run it my separately using **entry.sh** (packages from reuirements.txt must be installed previously) from  folders backend, frontend, etc
### Demo
- this is the easiest way to access this work
- navigate **vajpet.com** and all details will be provided on the website
- this website is running AWS EC2 instance server ()
#### Custom domain address (OPTIONAL)
- repository  is set primarily to http but the demo I run securely on https
- to run it on your own domain, you need to do following steps:
   - create your own domain 
   - get DNS A record for `<your_domain>` and `www.<your_domain> and add you endpoint to it
   - Obtain SSL certicates (I used CertBot in my linux enviroment)
   - Add SSL certificates to nginx with domains and redirect http and https to only https
   - Then you just set your domain in nginx.conf in https folder and copy-paste all files from https folder to root directory
   - Now you can follow following docker-compose option, which can be run without customing domain  
### Docker Compose
- from root directory:

1. **Download the Script**  
   Download the `install_docker_compose.sh` script from the provided location.

2. **Make the Script Executable**  
   Open a terminal, navigate to the directory containing the script, and run:  
chmod +x install_docker_compose.sh

3. **Execute the Script**  
   Run the script with:  
   ```bash
   ./install_docker_compose.sh

4. **Verification**  
The script will display the installed versions of Docker and Docker Compose upon completion.

5. **Final run** 
   You have installed docker and docker-compose to create backend, forntend, nginx and cli.
   Now just run: 
   ```bash
   sudo docker-compose up -d

## Others features
1. **CLI**
   - run after `docker-compose up` succceded 
   - to run any method from command line you can use CLI. For more details please got to cli folder and read `README.md` file 

6. **Tests**
   - tests are saved in backend/routers starting with prefix `"test_"`
      1. we an run it in root:
      ```bash
      pytest
      2. after docker-compose up is executed, the tests for backend are run automatically as prerequsities for vuilding of backend (see entry.sh in backend folder) 


   












# Docker Compose Installation Script

This README outlines the steps to run a Bash script for installing Docker Compose on Ubuntu.

## Installation Steps

1. **Download the Script**  
   Download the `install_docker_compose.sh` script from the provided location.

2. **Make the Script Executable**  
   Open a terminal, navigate to the directory containing the script, and run:  
chmod +x install_docker_compose.sh

3. **Execute the Script**  
Run the script with:  
./install_docker_compose.sh


4. **Verification**  
The script will display the installed versions of Docker and Docker Compose upon completion.

## Note
- Ensure you have sudo privileges to run the script.
- The script checks if Docker Compose is already installed and installs it if necessary.
