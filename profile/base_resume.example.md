# Jane Doe

Austin, TX | (555) 867-5309 | jane.doe@example.com
linkedin.com/in/jane-doe | github.com/janedoe

## Skills

**Cloud:** AWS (IAM, S3, VPC, Lambda, EC2, RDS, CloudWatch, SNS)
**Infrastructure as Code:** Terraform, Ansible, CloudFormation
**Containers & CI/CD:** Docker, Kubernetes, GitHub Actions, Jenkins, Git
**Monitoring & Observability:** Prometheus, Grafana, CloudWatch
**Programming:** Python, Bash, SQL
**Networking:** DNS/DHCP, firewalls, load balancing, VPC design
**Security:** IAM policy design, vulnerability scanning, Active Directory
**Virtualization:** VMware
**Practices:** SDLC, Agile, change management, incident response, documentation

## Projects

### Log Aggregation Pipeline — Centralized logging for a multi-service app
*Terraform, AWS Lambda (Python 3.12), S3, CloudWatch, SNS*

- Designed and deployed a serverless pipeline collecting application logs from three services into a queryable S3 store on a scheduled cadence
- Provisioned the entire stack as Terraform infrastructure-as-code, including IAM policies, retention rules, and event schedules — no console-created resources
- Cut mean time to locate a production error from roughly 15 minutes of manual searching to a single query
- Routed malformed log records to a dead-letter path instead of failing the batch, so one bad record can't drop an entire run

### Deployment Pipeline — Automated build and release to Kubernetes
*GitHub Actions, Docker, Docker Hub, Kubernetes, pytest, ruff*

- Built a four-stage pipeline (lint → test → build → deploy) with each stage gated on the previous, taking releases from manual SSH to push-triggered deploys in under 8 minutes
- Enforced quality gates with ruff linting and a pytest coverage floor that fails the build below threshold
- Published tagged Docker images to a registry, versioned by semantic version and CI run number
- Restricted the deploy stage to the main branch, with all registry credentials stored in Actions Secrets

### Containerized Web Application on Kubernetes
*Docker, Kubernetes, Flask, kubectl*

- Containerized a two-service application and deployed it to a Kubernetes cluster in a dedicated namespace with Deployments, Services, and ConfigMaps
- Authored all manifests as version-controlled YAML and validated them with server-side dry-run before applying
- Documented the build with an architecture diagram, a security decisions table, and a teardown procedure

### Multi-AZ Network with Terraform
*Terraform, AWS VPC, EC2, S3*

- Built a reusable Terraform VPC module provisioning public and private subnets across two availability zones with internet and NAT gateways
- Implemented tiered security groups where the database tier references the web tier rather than opening CIDR ranges
- Hardened EC2 instances with IMDSv2 and deployed a versioned, encrypted S3 bucket with public access blocked
- Configured remote state in an S3 backend so the module is safe for more than one person to run

## Work Experience

### Systems Analyst, Infrastructure — Example Corp, Austin, TX
*Mar 2021 – Present*

- Automate configuration and deployment of test environments using Ansible playbooks, replacing manual setup steps with repeatable, version-controlled runs
- Manage change control for application releases through Git, maintaining an auditable history of what changed, when, and why
- Partner with network engineers to design and roll out infrastructure spanning 200+ endpoints
- Author technical runbooks for platform migrations, standardizing rollout procedures and reducing incident resolution time
- Built reporting on incident trends and resolution metrics, improving tracking by 30%
- Drive change management across system rollouts, consolidating stakeholder input into controlled release plans

### IT Support Specialist — Sample Industries, Dallas, TX
*Jun 2018 – Mar 2021*

- Managed Windows and Linux systems in a secure enterprise environment; enforced access controls through Active Directory
- Led an email platform migration for 150+ users with zero business disruption
- Coordinated end-user support across Windows and macOS environments, resolving escalated technical incidents

## Certifications

- AWS Certified Solutions Architect – Associate
- CompTIA Security+

## Education

**State University** — B.S., Computer Science