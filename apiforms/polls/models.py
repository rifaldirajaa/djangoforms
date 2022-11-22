from django.db import models
from django_jsonform.models.fields import JSONField


class EmailJson(models.Model):
    ITEMS_SCHEMA = {
  "type": "array",
  "items": {
    "type": "object",
    "title": "email",
    "keys": {
        "type": {
                "type": "string",
                "title": "request type",
                "required": True,
                "helpText": "Choose Request Type",
                "choices": [
                    "email_basic",
                    "email_data",
                    "dataset",
                    "connect"
                ]
            },
             "sender": {
            "type": "array",
            "title": "email sender",
            "required": False,
            "items": {
                "type": "string",
                "format": "email"
            }
        },
          "receiver": {
            "type": "array",
            "title": "receiver email",
            "required": False,
            "items": {
                "type": "string",
                "format": "email"
            }
        },
        "cc": {
            "type": "array",
            "title": "receiver cc",
            "required": False,
            "items": {
                "type": "string",
                "format": "email"
            }
        },
        "bcc": {
            "type": "array",
            "title": "receiver bcc",
            "required": False,
            "items": {
                "type": "string",
                "format": "email"
            }
        },
           "receiver_table": {
            "type": "array",
            "title": "receiver table",
            "required": False,
            "items": {
                "type": "string",
                "placeholder": "BQ table for recepient list",
                "helpText": "e.g: `project.dataset.table`"
            }
        },
          "subject": {
            "type": "string",
            "required": True
            },
        "body": {
            "type": "string",
            "required": False
            }
    }
  }
}

    items = JSONField(schema=ITEMS_SCHEMA)
    date_created = models.DateTimeField(auto_now_add=True)

# Create your models here.
