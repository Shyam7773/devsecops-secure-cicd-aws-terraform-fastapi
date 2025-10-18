# Secure CI/CD Demo (DevSecOps)

A compact DevSecOps showcase aligned to Salesforce's Associate DevSecOps Engineer role.

**Highlights**
- FastAPI service with `/health`, `/predict`, and Prometheus `/metrics`
- Dockerized app with non-root user
- GitHub Actions CI: Black, Flake8, Pytest (coverage), Bandit (code security), Trivy (image CVEs)
- Terraform IaC for AWS: VPC, public subnet, SG, IAM role, Ubuntu EC2 with user data that runs a container
- Sample Prometheus scrape config for metrics

## Repo Structure
```
app/                # FastAPI app and runtime requirements
tests/              # pytest tests
infra/              # Terraform (VPC, EC2, SG, IAM, user_data)
.github/workflows/  # CI pipeline
Dockerfile
README.md
prometheus.yml
```

## Quickstart (Local)

```bash
# 1) Build & run
docker build -t devsecops-demo:local .
docker run -p 8080:80 devsecops-demo:local

# 2) Try endpoints
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict -H 'Content-Type: application/json' -d '{"text":"great product"}'
curl http://localhost:8080/metrics
```

## CI Pipeline

On every push/PR to `main`:
- **Black**: formatting check
- **Flake8**: linting
- **Pytest**: unit tests + coverage
- **Bandit**: Python security scan
- **Trivy**: container image vulnerability scan
- **Terraform**: fmt, init (no backend), validate
- **tfsec**: IaC static analysis (soft-fail by default)

> Make `tfsec` blocking by setting `soft_fail: false` in `.github/workflows/ci.yml`.

## Terraform (AWS)

Prereqs: AWS account and credentials. Default region `eu-west-1` (Ireland).

```bash
cd infra
terraform init        # use -backend=false for demo
terraform plan -var="container_image=devsecops-demo:local"
terraform apply -auto-approve -var="container_image=nginxdemos/hello"
```

Outputs include the EC2 public IP/DNS. Visit `http://<public_ip>/health`.
To run your own app image, push it to a registry (e.g. Docker Hub/ECR) and set `-var="container_image=<your_image>"`.

## Monitoring

- App exposes Prometheus metrics at `/metrics`.
- Use `prometheus.yml` as a starter and point targets to the EC2 public IP: `['<EC2_IP>:80']`.
- Optional: import into Grafana for quick visualization.

## Security Notes

- Use GitHub Secrets for any credentials (never commit secrets).
- IAM is least-privilege for demo (CloudWatch + ECR pulls). Tighten further as needed.
- Container runs as a **non-root** user in Docker.
- All scans run in CI to prevent deploying insecure builds.

## Why This Fits DevSecOps

This repo demonstrates: CI/CD automation, security gates (SAST + image scan), reproducible IaC, observability, and secure defaults—exactly what a DevSecOps team needs for reliable, secure delivery.
