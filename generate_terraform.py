def generate_terraform(postgres_version, instance_type, num_replicas):
    terraform_code = f"""
    provider "aws" {{
      region = "us-east-1"
    }}

    resource "aws_instance" "postgres_primary" {{
      ami           = "ami-0c55b159cbfafe1f0"  # Example Ubuntu AMI
      instance_type = "{instance_type}"

      tags = {{
        Name = "Postgres-Primary"
      }}
    }}

    resource "aws_instance" "postgres_replica" {{
      count         = {num_replicas}
      ami           = "ami-0c55b159cbfafe1f0"
      instance_type = "{instance_type}"

      tags = {{
        Name = "Postgres-Replica-${{count.index + 1}}"
      }}
    }}
    """
    with open("main.tf", "w") as f:
        f.write(terraform_code)