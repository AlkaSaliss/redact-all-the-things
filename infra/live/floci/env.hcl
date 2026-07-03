locals {
  deployment_mode    = "floci"
  environment        = "floci"
  floci_endpoint_url = get_env("FLOCI_ENDPOINT_URL")
  state_backend      = "local"
}
