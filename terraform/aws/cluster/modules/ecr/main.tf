data "aws_ecr_repository" "api" {
  name = "${var.project_name}-api"
}
