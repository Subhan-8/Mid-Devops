# Comprehensive DevOps Implementation Report

**Project Name:** Web-based Student Information System (SSIS) Modernization
**Date:** December 2025
**Author:** Subhan

---

## 1. Project Overview
This project involved migrating a monolithic Flask-based application to a cloud-native, microservices-ready architecture using modern DevOps practices. The transformation covered the entire lifecycle from local containerization to automated cloud deployment with monitoring.

## 2. Technology Stack & Tools Used
*   **Version Control:** Git, GitHub
*   **Containerization:** Docker, Docker Compose
*   **Infrastructure as Code (IaC):** Terraform (AWS Provider)
*   **Configuration Management:** Ansible
*   **Orchestration:** Kubernetes (K3s)
*   **CI/CD:** GitHub Actions
*   **Monitoring:** Prometheus, Grafana, Node Exporter
*   **Cloud Provider:** AWS (EC2, VPC, S3, Security Groups)

---

## 3. Step-by-Step Implementation Log

### Step 1: Containerization (Docker)
**Objective:** Isolate the application dependencies and create a consistent build artifact.

*   **Actions:**
    1.  Refactored `Dockerfile` to use **Multi-Stage Builds** (reduced image size).
    2.  Integration of **Redis** for caching.
    3.  Implemented `docker-compose.yml` for local orchestration.

*   **Key Commands Executed:**
    ```bash
    # Build the image locally
    docker build -t ssis-web .

    # Run the stack (App + DB + Redis)
    docker-compose up --build -d

    # verify containers
    docker ps
    ```

### Step 2: Infrastructure Provisioning (Terraform)
**Objective:** Provision reproducible infrastructure on AWS.

*   **Actions:**
    1.  Authored `infra/vpc.tf` to create a new VPC, Internet Gateway, and Subnets.
    2.  Authored `infra/ec2.tf` to provision a `t3.small` Ubuntu instance.
    3.  Authored `infra/security_groups.tf` to define strict firewall rules.

*   **Key Commands Executed:**
    ```bash
    cd infra
    # Initialize Terraform
    terraform init

    # Preview changes
    terraform plan

    # Apply changes (Create execution plan)
    terraform apply -auto-approve
    ```
    *Result:* Obtained EC2 Public IP: `3.221.149.190`.

### Step 3: Configuration Management (Ansible)
**Objective:** Automate the setup of the EC2 server (installing Docker & K3s).

*   **Actions:**
    1.  Created `ansible/inventory.ini` mapping the EC2 IP.
    2.  Created `ansible/playbook.yaml` to automated installation steps.
    3.  **Workaround Used:** Ran Ansible via a Docker container to bypass Windows SSH permission issues.

*   **Key Commands Executed:**
    ```powershell
    # Run playbook via Docker container
    docker run --rm -v ${PWD}:/work -w /work/ansible willhallonline/ansible:2.14-ubuntu-22.04 /bin/sh -c "cp ../ssis-key.pem /tmp/key && chmod 600 /tmp/key && ansible-playbook -i inventory.ini playbook.yaml --private-key /tmp/key"
    ```

### Step 4: Kubernetes Deployment
**Objective:** Deploy the application to the K3s cluster.

*   **Actions:**
    1.  Defined Namespaces (`dev`, `prod`).
    2.  Created `k8s/secret.yaml` base64 encoded credentials.
    3.  Created Deployments for MySQL, Redis, and Flask App (`ssis-web`).
    4.  Exposed app via **NodePort 30080**.

*   **Key Commands Executed:**
    ```bash
    # Apply manifests
    kubectl apply -f k8s/namespace.yaml
    kubectl apply -f k8s/
    
    # Check status
    kubectl get pods -n dev
    kubectl get svc -n dev
    ```

### Step 5: CI/CD Pipeline (GitHub Actions)
**Objective:** Automate the entire delivery pipeline.

*   **Actions:**
    1.  Created `.github/workflows/ci-cd.yml`.
    2.  Configured 6 stages:
        *   **Build & Test**: `pytest`, `flake8`.
        *   **Push**: Push Docker Image to Docker Hub.
        *   **Infra**: Run `terraform plan` to validate IaC.
        *   **Deploy**: SSH into EC2 and run `kubectl apply`.
        *   **Smoke Test**: `curl` the application endpoint.

*   **Key Workflow Snippet:**
    ```yaml
    - name: Deploy to K3s
      run: |
        kubectl apply -f k8s/namespace.yaml
        kubectl apply -f k8s/monitoring/
        kubectl rollout restart deployment/ssis-web -n dev
    ```

### Step 6: Monitoring (Prometheus & Grafana)
**Objective:** Gain observability into the cluster health.

*   **Actions:**
    1.  Deployed **Prometheus** (Port 30090).
    2.  Deployed **Grafana** (Port 30091).
    3.  Deployed **Node Exporter**.
    4.  Updated Security Groups to allow traffic on these ports.

*   **Key Commands Executed:**
    ```bash
    kubectl apply -f k8s/monitoring/
    ```

---

## 4. Troubleshooting Log & Challenges

### Issue 1: Git Push Blocked by Large Files
*   **Problem:** Terraform provider binaries (`.terraform/`) were too large for GitHub.
*   **Solution:** Updated `.gitignore` and ran:
    ```bash
    git rm -r --cached infra/.terraform
    git commit -m "Remove ignored files"
    ```

### Issue 2: AWS VPC Limit Exceeded
*   **Problem:** CI/CD pipeline tried to create a *new* VPC on every run because it lacked access to the local Terraform state.
*   **Solution:** Modified the CI/CD pipeline to use `terraform plan` instead of `apply` to validate code without duplicating infrastructure.

### Issue 3: Smoke Test Connection Timeout
*   **Problem:** The application was deployed, but the GitHub Action "Smoke Test" failed.
*   **Root Cause:** AWS Security Group blocked port 30080.
*   **Solution:** Created a custom GitHub Workflow `fix_sg.yml` to force-open port 30080 using AWS CLI.
    ```yaml
    aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 30080 --cidr 0.0.0.0/0
    ```

---

## 5. Final Deliverables Status
*   [x] **Source Code**: Fully pushed to GitHub.
*   [x] **Docker Image**: Available at `subhan45/ssis-web`.
*   [x] **Infrastructure**: Live on AWS (IP: 3.221.149.190).
*   [x] **Pipeline**: Passing (Green).
*   [x] **Monitoring**: Accessible via Browser.
