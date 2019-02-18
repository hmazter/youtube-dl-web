provider "heroku" {
  version = "~> 1.7"
}

provider "aws" {
  version = "~> 1.59"
  region  = "eu-west-1"
}

# App
resource "heroku_app" "production" {
  name   = "${var.heroku_app_name}"
  region = "eu"

  config_vars = {
    FLASK_APP             = "app"
    FLASK_ENV             = "development"
    AWS_ACCESS_KEY_ID     = "${aws_iam_access_key.app-user.id}"
    AWS_SECRET_ACCESS_KEY = "${aws_iam_access_key.app-user.secret}"
  }
}

# Bucket
resource "aws_s3_bucket" "storage" {
  bucket = "youtube-dl-storage"
  acl    = "private"

  lifecycle_rule {
    enabled = false

    expiration {
      days = 1
    }
  }
}

resource "aws_iam_user" "app-user" {
  name = "youtube-dl-app"
}

resource "aws_iam_access_key" "app-user" {
  user = "${aws_iam_user.app-user.name}"
}

resource "aws_s3_bucket_policy" "storage-policy" {
  bucket = "${aws_s3_bucket.storage.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Sid": "Allow app full access to bucket",
          "Effect": "Allow",
          "Principal": {
              "AWS": "${aws_iam_user.app-user.arn}"
          },
          "Action": "s3:*",
          "Resource": [
              "${aws_s3_bucket.storage.arn}",
              "${aws_s3_bucket.storage.arn}/*"
          ]
      }
  ]
}
POLICY
}
