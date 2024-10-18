Here is a detailed **README.md** to document your project, covering the setup, usage, error handling, assumptions, and future use cases.

---

## **README.md**  

# PostgreSQL Primary-Replica Setup Automation API  

## **Overview**  
This project provides a RESTful API built with **FastAPI** that automates the setup of a PostgreSQL **primary-read-replica architecture**. The API generates Terraform configurations to provision infrastructure (EC2 instances, security groups) and Ansible playbooks to install and configure PostgreSQL, including replication between the primary and replicas.  

---

## **Features**  
- **Automated Infrastructure Provisioning:** Dynamically generates Terraform templates to create EC2 instances and security groups.  
- **PostgreSQL Installation & Configuration:** Uses Ansible to configure the PostgreSQL server and set up replication.  
- **Configurable Parameters:** Accepts PostgreSQL version, instance type, number of replicas, and settings like `max_connections` and `shared_buffers`.  
- **API Workflow:** Provides endpoints to generate code, plan and apply infrastructure, and execute Ansible playbooks.  
- **Modularity and Maintainability:** Separation of logic between Terraform, Ansible, and Python code for better maintainability.

---

## **Folder Structure**

```bash
postgresql-api/
├── app.py               # FastAPI app with API routes
├── generate_terraform.py # Generates Terraform configurations dynamically
├── generate_ansible.py   # Generates Ansible playbooks for PostgreSQL setup
├── main.tf               # Base Terraform configuration
├── requirements.txt      # Python dependencies
├── README.md             # Documentation (this file)
├── configure_postgres.yml # Generated Ansible playbook (after API call)
└── inventory.ini         # Ansible inventory file
```

---

## **Pre-requisites**  

1. **Python 3.x** and pip installed  
2. **Ansible installed** on the local machine or VM  
   ```bash
   sudo apt update
   sudo apt install ansible -y
   ```  
3. **Terraform installed**  
   Download and install Terraform: https://www.terraform.io/downloads  
4. **AWS or Cloud Provider Configuration:** Ensure your VM has access to AWS (or the relevant cloud provider) credentials.  
5. **Open Required Ports:** Ensure the security group allows **inbound access on port 8000** to expose the API.

---

## **Setup Instructions**  

### 1. Clone the Repository  

```bash
git clone <repository-url>
cd postgresql-api
```

### 2. Create a Virtual Environment  

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies  

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI Server  

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## **API Endpoints**  

### **1. Generate Code (Terraform & Ansible)**
- **Endpoint:** `GET /generate-code/`  
- **Description:** This endpoint generates Terraform and Ansible code based on the parameters provided.

**Request Example:**
```bash
curl -X GET http://<your-server-ip>:8000/generate-code/
```

**Response:**
```json
{
  "message": "Code generated successfully."
}
```

---

### **2. Apply Terraform Plan**
- **Endpoint:** `POST /apply-terraform/`  
- **Description:** Runs `terraform plan` and `terraform apply` to provision infrastructure.

**Request Example:**
```bash
curl -X POST http://<your-server-ip>:8000/apply-terraform/
```

**Response:**
```json
{
  "message": "Terraform apply executed successfully."
}
```

---

### **3. Configure PostgreSQL with Ansible**
- **Endpoint:** `POST /configure-postgres/`  
- **Description:** Runs the Ansible playbook to install and configure PostgreSQL on the provisioned instances.

**Request Example:**
```bash
curl -X POST http://<your-server-ip>:8000/configure-postgres/
```

**Response:**
```json
{
  "message": "PostgreSQL configured successfully."
}
```

---

## **Handling Errors and Edge Cases**  

1. **Terraform Apply Failures:**  
   - If infrastructure provisioning fails, the API will return an appropriate error message.
   - Example response:  
     ```json
     { "detail": "Terraform apply failed with exit status 1." }
     ```

2. **Ansible Playbook Errors:**  
   - If the Ansible playbook execution fails, the error will be logged, and the response will indicate failure.
   - Example response:  
     ```json
     { "detail": "Configuration failed: Ansible playbook returned non-zero exit status." }
     ```

3. **Invalid Parameters:**  
   - If the API receives invalid input (e.g., non-integer `max_connections`), it will return a **400 Bad Request** response.

4. **Network Issues:**  
   - If the API server or PostgreSQL instances are not reachable, the appropriate timeout or network error will be logged and returned to the user.

---

## **How to Modify the API**  

1. **Update Terraform Configuration:**
   Modify the `main.tf` template or **`generate_terraform.py`** to adjust the EC2 instance types, security groups, or other infrastructure settings.

2. **Modify Ansible Playbooks:**
   Adjust the **`generate_ansible.py`** script to change PostgreSQL configurations (e.g., replication, logging).

3. **Add New Endpoints:**
   Add new endpoints in **`app.py`** if you want to introduce more functionality (e.g., checking infrastructure status).

---

## **Assumptions**  
1. PostgreSQL version 12 is used by default unless specified.  
2. The target infrastructure is assumed to be running on AWS EC2.  
3. The primary-read-replica setup assumes synchronous replication, but can be modified to asynchronous.  
4. Terraform and Ansible are installed and accessible from the machine running the API.  
5. Inventory (`inventory.ini`) correctly points to the provisioned EC2 instances.

---

## **Future Use Cases**  
1. **Multi-Cloud Support:** Extend the API to support other cloud providers (e.g., Azure, GCP).  
2. **Advanced PostgreSQL Configurations:** Add support for more PostgreSQL parameters like replication lag detection or automated failover.  
3. **Monitoring and Alerts:** Integrate Prometheus/Grafana or CloudWatch to monitor PostgreSQL health.  
4. **Database Backups:** Include automation for regular database backups and restores.

---

## **Common Issues and Troubleshooting**  

1. **ETIMEDOUT Error:**
   - Ensure the API server is running and listening on **0.0.0.0:8000**.
   - Check security groups/firewall rules to allow access to **port 8000**.

2. **Ansible Fails to Connect:**
   - Ensure the target EC2 instances are reachable via SSH.
   - Verify that the SSH key is correctly configured in the `inventory.ini`.

3. **Terraform Apply Hangs:**
   - Ensure AWS credentials are properly configured.
   - Check for network connectivity issues between the API server and AWS.

---

## **Conclusion**  
This project provides a flexible and automated way to set up a PostgreSQL primary-read-replica architecture using Terraform and Ansible. With configurable parameters and modular code, it is easy to extend and maintain for future use cases.

---

Let me know if you need further customization or clarification!
