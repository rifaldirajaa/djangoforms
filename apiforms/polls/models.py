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
            "type": "string",
            "title": "email sender",
            "required": False,
            "format": "email"
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
class TypeEmail(models.Model):
    ITEMS_SCHEMA = {
        "type": "object",
        "keys":{
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
            }
        }}
    items = JSONField(schema=ITEMS_SCHEMA)

class BasicEmail(models.Model):
    ITEMS_SCHEMA = {
        "type": "array",
        "items": {
            "type": "object",
            "title": "email",
            "keys": {
                    "sender": {
                        "type": "string",
                        "title": "email sender",
                        "required": False,
                        "format": "email"
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

class DataEmail(models.Model):
    ITEMS_SCHEMA = {
            "type": "object",
            "title": "emaildata",
            "keys": {
                "dataset": {
                "$ref": "#/$defs/dataset"
                },
                "subject": {
                "type": "string",
                "required": True
                },
                "sender": {
                    "type": "string",
                    "title": "email sender",
                    "required": False,
                    "format": "email"
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
                "bodyhtml": {
                "type": "string",
                "widget": "textarea",
                "required": True
                },
              "attachment":{
                  "$ref": "#/$defs/attachment"
                }
        },
            "$defs": {
                "dataset":{
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                        "dataset_name": {
                        "type": "string",
                        "title": "Dataset Name",
                        "required": True
                        },
                    "query": {
                        "type": "string",
                        "widget": "textarea",
                        "title": "SQL Query",
                        "required": True,
                        "placeholder": "select * from `project.dataset.table` where col_ref ><= date",
                        "helpText": "query must have where clause for time"
                        },
                   "col_ref": {
                        "type": "string",
                        "title": "Date Column (opt)",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as date reference on table"
                        },
                  "fromdate": {
                        "type": "string",
                        "title": "From Date (opt)",
                        "required": False,
                        "placeholder": "yyyy-mm-dd",
                        "helpText": "if null use datetimenow()"
                        },
                  "todate": {
                        "type": "string",
                        "title": "To Date (opt)",
                        "required": False,
                        "placeholder": "yyyy-mm-dd",
                        "helpText": "if null use datetimenow()"
                        }
                }
                }
            },
              "attachment":{
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                        "dataset_name": {
                        "type": "string",
                        "title": "Dataset Name",
                        "required": True
                        },
                    "attachment_name": {
                        "type": "string",
                        "title": "Attachment Name",
                        "required": True,
                        "placeholder": "filename.csv",
                        "helpText": "(.xlsx,.xls,.csv)"  
                        },
                   "zipname": {
                        "type": "string",
                        "title": "zip name (opt)",
                        "required": False,
                        "placeholder": "filename.zip",
                        "helpText": "enter if want to zip files, zip multiple files by declare same name"
                        },
                  "zippassword": {
                        "type": "string",
                        "title": "zip password (opt)",
                        "required": False,
                        "placeholder": "password",
                        "helpText": "enter if want to add password to zipfiles, ignore if dont want password on zipfiles"
                        }
                }
                }
            }
            }
            }
            
    items = JSONField(schema=ITEMS_SCHEMA)