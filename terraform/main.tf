terraform {
    cloud {
        organization = "disinformation-verifier"
        workspaces {
            name = "disinformation-verifier"
        }
    }
}

provider "aws" {
    region = "eu-west-2"
}
