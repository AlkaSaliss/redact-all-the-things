# Version constraints for the entire project
# This file ensures consistent versions across all modules



terraform {
  required_version = ">= 1.13.0, < 1.14.0"

  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.7"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
