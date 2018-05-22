provider "heroku" {
  email   = "${var.heroku_email}"
  api_key = "${var.heroku_api_key}"
}

# App
resource "heroku_app" "production" {
  name = "${var.heroku_app_name}"
  region = "us"

  config_vars = {
    FLASK_APP = "app"
    FLASK_ENV = "development"
  }
}