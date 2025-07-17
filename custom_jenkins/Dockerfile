# ✅ Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# 🔧 Switch to root user to install system dependencies and Docker
USER root

# 📦 Install prerequisites and Docker CLI inside Jenkins container
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean

# 👥 Add Jenkins user to the 'docker' group so Jenkins can run Docker commands
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# 📁 Create Docker directory and mount it as a volume for Docker-in-Docker (optional)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# 🔄 Switch back to Jenkins user for normal Jenkins operations
USER jenkins
