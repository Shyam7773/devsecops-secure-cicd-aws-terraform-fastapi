variable "project" {
  description = "Project name prefix"
  type        = string
  default     = "devsecops-demo"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "container_image" {
  description = "Container image to run on the EC2 host (e.g., ghcr.io/owner/secure-ci-cd-demo:latest)"
  type        = string
  default     = "nginxdemos/hello"
}
