terraform {
  required_version = ">= 1.10, < 2.0"
}

resource "terraform_data" "lesson" {
  input = "Infrastructure changes deserve review too."
}

output "message" {
  value = terraform_data.lesson.output
}
