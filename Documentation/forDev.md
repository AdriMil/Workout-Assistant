# More infos for developers
## SonarQube analysis process
SonarQube server is running with docker on my local computer.

### SonarQube Server
Create volumes to keep your analysis in case of SonarQube container reboot : 
```console
docker volume create sonarqube_data
docker volume create sonarqube_extensions
```

Run sonarqube:community container :
```console
docker run -d --rm --name sonarqube  -p 9000:9000  -v sonarqube_data:/opt/sonarqube/data -v sonarqube_extensions:/opt/sonarqube/extensions  sonarqube:community
```

### Link your project
Within SonarQube server UI, link your local repositry where .git file from this project is.
Keep information like Token, PROJECT_KEY for next step.

### Run Alanysis
Run following command to analyse your project
```console
docker run --rm -e SONAR_HOST_URL="http://host.docker.internal:9000"  -e SONAR_SCANNER_OPTS="-Dsonar.projectKey=**PROJECT_KEY** -Dsonar.sources=." -e SONAR_TOKEN="**YOUR_TOKEN**" -v "**PROJECT_LOCAL_FOLDER**:/usr/src" sonarsource/sonar-scanner-cli
```
### Results  
All results will be displayed in SonarQube web UI. 
