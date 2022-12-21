from django.db import models
from django_jsonform.models.fields import JSONField
from django.contrib.auth.models import User
import json
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.title + ' | ' + str(self.author)


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
                "preprocess_data":{
                "type":"object",
                "title":"Preprocess_data",
                "keys":{
     "Table":
	{
		"type":"array",
		"items":{
		"type":"object",
		"keys":{
                    "table_name": {
                        "type": "string",
                        "title": "Table Name",
                        "required": True
                        },
                    "dataset_name": {
                        "type": "string",
                        "title": "Dataset Name",
                        "required": True
                        },
                    "show_column": {
                        "type": "string",
                        "widget": "textarea",
                        "title": "Show Column",
                        "required": False,
                        "placeholder": "select column from dataset"
                        }
		}
		}
	},
      "Bar/Line Chart":
        {
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                    "type": {
                "type": "string",
                "title": "Bar/Line Chart",
                "required": True,
                "helpText": "Choose Request Chart",
                "choices": [
                    "Line Chart",
                    "Bar Chart",
                    "stacked bar",
                    "clustered bar",
                    "horizontal stacked bar",
                    "horizontal clustered bar"
                ]
            },
                    "chart_name": {
                        "type": "string",
                        "title": "Chart Name",
                        "required": True
                        },
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
                        "placeholder": "query to dataset",
                        "helpText": "query must have where clause for time"
                        },
                    "plot_title": {
                        "type": "string",
                        "title": "plot_title",
                        "required": False,
                        "placeholder": "Title",
                        "helpText": "Title for the Plot"
                        },
                   "x_axis": {
                        "type": "string",
                        "title": "x_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        },
                  "y_axis": {
                        "type": "string",
                        "title": "y_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        },
                    "legend":{
                        "type": "string",
                        "title": "Legend Position",
                        "required": False,
                        "helpText": "Choose Legend Position",
                        "choices": [
                            "upper left",
                            "center left",
                            "bottom left"
                ]
                    }
                }
                }
            },
      "Scatter_Plot":
        {
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                    "chart_name": {
                        "type": "string",
                        "title": "Chart Name",
                        "required": True
                        },
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
                        "placeholder": "query to dataset",
                        "helpText": "query must have where clause for time"
                        },
                   "x_axis": {
                        "type": "string",
                        "title": "x_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        },
                  "y_axis": {
                        "type": "string",
                        "title": "y_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        }
                }
                }
            },
      "Pie_chart":
        {
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                    "chart_name": {
                        "type": "string",
                        "title": "Chart Name",
                        "required": True
                        },
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
                        "placeholder": "query to dataset",
                        "helpText": "query must have where clause for time"
                        },
                   "label": {
                        "type": "string",
                        "title": "label",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as label reference on table"
                        },
                  "slices": {
                        "type": "string",
                        "title": "slices",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as slices reference on table"
                        }
                }
                }
            }
                }
                },
                "subject": {
                "type": "string",
                "required": True,
                "placeholder": "email subject",
                "helpText": "e.g: Finance data {recepient} on {tanggal(datasetname,colname,day/month/year)}"
                },
                "sender": {
                    "type": "string",
                    "title": "email sender",
                    "required": False,
                    "format": "email",
                    "placeholder": "optional email@email.com",

                },
                "receiver": {
                    "type": "array",
                    "title": "receiver email",
                    "required": False,
                    "items": {
                        "type": "string",
                        "format": "email",
                        "placeholder": "optional email@email.com",
                    }
                },
                "cc": {
                    "type": "array",
                    "title": "receiver cc",
                    "required": False,
                    "items": {
                        "type": "string",
                        "format": "email",
                        "placeholder": "optional email@email.com",
                    }
                },
                "bcc": {
                    "type": "array",
                    "title": "receiver bcc",
                    "required": False,
                    "items": {
                        "type": "string",
                        "format": "email",
                        "placeholder": "optional email@email.com",
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
                "required": True,
                "placeholder": "body on email",
                "helpText": "use {recepient} to include partner name, {tanggal(datasetname,colname,day/month/year)} to include date, {table(tablename,tabel title)} for table,  {image(chartname,chart title)} for plot "
                },
              "attachment":{
                  "$ref": "#/$defs/attachment"
                },
                "schjobid":{
                    "type": "string",
                    "title": "scheduler job id",
                    "required": False,
                    "helpText": "unique id for job",
                    "placeholder": "(opt) fill if want to make this a schedule"
                },
                "Daily": {
                "$ref": "#/$defs/Daily"
                },
                "Weekly": {
                "$ref": "#/$defs/Weekly"
                },
                "Monthly": {
                "$ref": "#/$defs/Monthly"
                },
                "Yearly": {
                "$ref": "#/$defs/Yearly"
                },
                "Custom": {
                "$ref": "#/$defs/Custom"
                },
                "schtimezone":{
                        "type": "string",
                        "title": "timezone",
                        "required": False,
                        "placeholder": "(opt) Asia/Jakarta",
                        "helpText": "timezone for scheduler"
                },
                "schdescription":{
                        "type": "string",
                        "widget": "textarea",
                        "title": "description",
                        "required": False,
                        "placeholder": "(opt) desc",
                        "helpText": "description for scheduler"
                }
        },
            "$defs": {
                "preprocess":{
                    "type":"array",
                    "items":{
                        "type":"object",
                        "title":"Preprocess",
                        "keys":{
                            "Table":
        {
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                    "table_name": {
                        "type": "string",
                        "title": "Table Name",
                        "required": True
                        },
                    "dataset_name": {
                        "type": "string",
                        "title": "Dataset Name",
                        "required": True
                        },
                    "show_column": {
                        "type": "string",
                        "widget": "textarea",
                        "title": "Show Column",
                        "required": False,
                        "placeholder": "select column from dataset"
                        }
                }
                }
            },
      "Bar/Line Chart":
        {
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                    "type": {
                "type": "string",
                "title": "Bar/Line Chart",
                "required": True,
                "helpText": "Choose Request Chart",
                "choices": [
                    "Line Chart",
                    "Bar Chart"
                ]
            },
                    "chart_name": {
                        "type": "string",
                        "title": "Chart Name",
                        "required": True
                        },
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
                        "placeholder": "query to dataset",
                        "helpText": "query must have where clause for time"
                        },
                   "x_axis": {
                        "type": "string",
                        "title": "x_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        },
                  "y_axis": {
                        "type": "string",
                        "title": "y_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        }
                }
                }
            },
      "Scatter_Plot":
        {
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                    "chart_name": {
                        "type": "string",
                        "title": "Chart Name",
                        "required": True
                        },
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
                        "placeholder": "query to dataset",
                        "helpText": "query must have where clause for time"
                        },
                   "x_axis": {
                        "type": "string",
                        "title": "x_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        },
                  "y_axis": {
                        "type": "string",
                        "title": "y_axis",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as x axis reference on table"
                        }
                }
                }
            },
      "Pie_chart":
        {
                "type": "array",
                "items": {
                "type": "object",
                "keys": {
                    "chart_name": {
                        "type": "string",
                        "title": "Chart Name",
                        "required": True
                        },
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
                        "placeholder": "query to dataset",
                        "helpText": "query must have where clause for time"
                        },
                   "label": {
                        "type": "string",
                        "title": "label",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as label reference on table"
                        },
                  "slices": {
                        "type": "string",
                        "title": "slices",
                        "required": False,
                        "placeholder": "column name",
                        "helpText": "column used as slices reference on table"
                        }
                }
                }
            }
                        }
                    }
                },
                "dataset":{
  "type": "array",
  "items": {
    "type": "object",
    "title": "Dataset",
    "keys": {
      "dataset_name": {
        "type": "string",
        "title":"Dataset Name",
        "required":True
      },
      "query": {
        "type": "string",
        "widget":"text area",
        "title":"SQL Query",
        "required":True,
        "place_holder":"query to dataset",
        "helpText": "select * from `project.dataset.table` where col = {D}/{D-1}"
      },
      "col_ref": {
                        "type": "string",
                        "title": "reference column",
                        "required": True,
                        "placeholder": "column name",
                        "helpText": "column used as filter reference on table"
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
                        "helpText": "(.xlsx,.xls,.csv,.txt,none)"  
                        },
                    "delimiter": {
                        "type": "string",
                        "title": "Delimiter (opt for csv,txt,none)",
                        "required": False,
                        "placeholder": "; , |",
                        "helpText": "default value: ','"
                        },
                    "template":{
                        "type": "string",
                        "title": "template name (opt)",
                        "choices": [
			    "nan",
                            "template1",
                            "template2"
                        ]
                    },"templatedate":{
                        "type": "string",
                        "title": "date inside template(opt)",
                        "placeholder": "tanggal(datasetname,kolom,day/month/year)"
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
                },"additionalProperties": {
                        "type": "string"
                    },
                }
            },
            "Daily": {
                "type": "object",
                "keys": {
                    "time": {
                        "type": "string",
                        "format": "time",
                        "helpText": "Time where job run on Asia/Jakarta"
                    }
                }
    },
    "Weekly":{
        "type": "array",
        "titles": "Day",
        "items": {
        "type": "string",
        "choices": [
        "MON","TUE","THU","WED","FRI","SAT","SUN"
        ],
        "widget": "multiselect"
        }       
    },
    "Monthly":{
      "type": "string",
      "placeholder": "Day of month",
      "helpText": "e.g: 28,29,30 or 1-7"
    },
    "Yearly":{
        "type": "array",
        "items": {
        "type": "string",
        "choices": [
        "JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"
        ],
        "widget": "multiselect"
        }       
    },
    "Custom":{
      "type": "string",
      "placeholder": "0 12 10-31 * MON-FRI",
      "helpText": "e.g At 12:00 on every day-of-month from 10 through 31 and Monday to Friday"
    }
            }
            }
       
    items = JSONField(
        schema=ITEMS_SCHEMA
        )
    def __str__(self):
        if len(self.items['schjobid'])>0:
            return str(self.items['subject']) + ' | ' + str(self.items['schjobid'])
        else:
            return str(self.items['subject'])
    
    def get_absolute_url(self):
        return reverse('home')
        