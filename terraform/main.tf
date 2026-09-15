terraform {
    cloud {
        organization = "disinformation-verifier"
        workspaces {
            name = "disinformation-verifier"
        }
    }
}

provider "aws" {
    region = var.aws_region
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
}
