# Terraform Multi-Cloud Modules

Reusable, production-minded Terraform modules for the most common services on **AWS**, **Azure** and **Google Cloud**, built with the **same layout and the same naming** on every cloud. Learn one module and you can use its equivalent on the other two.

[![terraform](https://github.com/chalampaladugu/terraform-multicloud-modules/actions/workflows/terraform.yml/badge.svg)](https://github.com/chalampaladugu/terraform-multicloud-modules/actions/workflows/terraform.yml)
![Terraform](https://img.shields.io/badge/terraform-%3E%3D1.5-7B42BC)
![License](https://img.shields.io/badge/license-MIT-green)

## Service map

| Capability | AWS | Azure | GCP |
|---|---|---|---|
| Network | [`aws/vpc`](modules/aws/vpc) | [`azure/vnet`](modules/azure/vnet) | [`gcp/vpc`](modules/gcp/vpc) |
| Virtual machine | [`aws/ec2`](modules/aws/ec2) | [`azure/vm`](modules/azure/vm) | [`gcp/compute`](modules/gcp/compute) |
| Kubernetes | [`aws/eks`](modules/aws/eks) | [`azure/aks`](modules/azure/aks) | [`gcp/gke`](modules/gcp/gke) |
| Object storage | [`aws/s3`](modules/aws/s3) | [`azure/storage`](modules/azure/storage) | [`gcp/gcs`](modules/gcp/gcs) |
| PostgreSQL | [`aws/rds`](modules/aws/rds) | [`azure/postgresql`](modules/azure/postgresql) | [`gcp/cloudsql`](modules/gcp/cloudsql) |

Each module folder has its own README with every input and output.

## Secure by default

- **Private first:** databases have no public endpoint; VMs get no public IP unless you ask; Kubernetes nodes run in private subnets.
- **Encryption everywhere:** encrypted disks, buckets and databases; TLS enforced.
- **No public buckets:** public access is blocked on S3, Blob and GCS.
- **No hard-coded secrets:** database passwords are generated (RDS stores its password in Secrets Manager) and outputs are marked `sensitive`.
- **Least-privilege identities:** dedicated IAM roles, managed identities and service accounts per workload.
- **Workload identity** is turned on for EKS (OIDC), AKS and GKE.

## Repository layout

```
.
├── modules/
│   ├── aws/      vpc · ec2 · eks · s3 · rds
│   ├── azure/    vnet · vm · aks · storage · postgresql
│   └── gcp/      vpc · compute · gke · gcs · cloudsql
├── examples/
│   ├── aws/      full stack wiring all AWS modules together
│   ├── azure/    full stack wiring all Azure modules together
│   └── gcp/      full stack wiring all GCP modules together
└── .github/workflows/terraform.yml   fmt + validate + tflint on every push/PR
```

## Quick start

```bash
git clone https://github.com/chalampaladugu/terraform-multicloud-modules.git
cd terraform-multicloud-modules/examples/aws      # or azure / gcp

cp terraform.tfvars.example terraform.tfvars      # fill in your values
terraform init
terraform plan
terraform apply
```

Log in to the cloud first: `aws configure` / `az login` / `gcloud auth application-default login`.

## Using a module from another repo

Pin to a release tag so upgrades are deliberate:

```hcl
module "network" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/aws/vpc?ref=v1.0.0"

  name                 = "prod"
  azs                  = ["us-east-1a", "us-east-1b"]
  public_subnet_cidrs  = ["10.0.0.0/20", "10.0.16.0/20"]
  private_subnet_cidrs = ["10.0.32.0/19", "10.0.64.0/19"]
}
```

## Cost notes

The examples are sized for **dev/test**. Before production, review:

- **NAT:** `single_nat_gateway = true` (AWS) saves money; use one per AZ for high availability.
- **Kubernetes control plane:** EKS charges per cluster-hour; the AKS `Free` tier and the GKE free-tier credit cover one small cluster.
- **Databases:** turn on `multi_az` / `high_availability` for production. The examples disable deletion protection so you can tear them down easily, so turn it back on for production.
- **Storage lifecycle:** buckets move to infrequent-access tiers after 30 days and delete old versions after 90 by default.

## Requirements

| Tool | Version |
|---|---|
| Terraform | >= 1.5 |
| AWS provider | >= 5.40, < 7.0 |
| AzureRM provider | >= 4.9, < 5.0 |
| Google provider | >= 6.0, < 8.0 |

## Contributing

1. Install [pre-commit](https://pre-commit.com) and run `pre-commit install`.
2. Run `terraform fmt -recursive` before committing.
3. Open a pull request; CI runs `fmt`, `validate` and `tflint` on every module and example.

## License

[MIT](LICENSE)
