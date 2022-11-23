from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from polls.forms import EmailForm, JsonForm, TypeForm, BasicForm, DataForm
import os
import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests
from formtools.wizard.views import SessionWizardView
from datetime import datetime
from itertools import compress
from dateutil.parser import parse,isoparse

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/buttercup/Documents/GitHub/key/celerates-playground-318603-f9d994464b15.json'
request = google.auth.transport.requests.Request()
audience = 'https://asia-southeast2-celerates-playground-318603.cloudfunctions.net/xl_email_ready'
TOKEN = google.oauth2.id_token.fetch_id_token(request, audience)

def index(request):
    # context = {'form': EmailForm()}
    # # return HttpResponse("Hello, world. You're at the polls index.")

    # if request.method == 'POST':
    #     form = EmailForm(request.POST)
    #     if form.is_valid():
    #         print(form.data)

    # return render(request, 'index.html', context)

    context ={}
 
    # create object of form
    
     
    # check if form data is valid
    if request.method == 'POST':
        form = JsonForm(request.POST or None)
        if form.is_valid():
            # save the form data to model
            print(form)
            form.save()
            jsondata = json.loads(form.data['items'])
            print(jsondata)
            context['data']=jsondata

            r = requests.post(
                audience, 
                headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
                data=json.dumps(jsondata)  # possible request parameters
            )
            context['response']=r.status_code, r.text
            print(r.status_code, r.text)
    else:
        form = JsonForm()
        
    context['form']= form


    
    return render(request, "index.html", context)

class FormWizard(SessionWizardView):
    template_name= "email_form.html"

    def done(self, form_list, **kwargs):
        form_data = process_form_data(form_list)
        return render('done.html',{'form_data':form_data})

def process_form_data(form_list):
    temp_data = []
    form_data_json = []
    for x in form_list:
        dicttemp = x.cleaned_data['items']
        temp_data.append(dicttemp)

    for y in temp_data[1]:
        y.update(temp_data[0])
        form_data_json.append(y)
        
    print(form_data_json)
    # form_data= json.dumps(form_data_json)
    return form_data_json

def indexdata(request):
    context ={}
    form = DataForm(request.POST or None)
    
    if form.is_valid():
        # save the form data to model
        form.save()
        formlist = [form]
        # form.save()
        jsondata = json.loads(form.data['items'])
        print(jsondata)

        retlis,datalis = mixmatch(jsondata['bodyhtml'],jsondata)
        jsonfinal = makejsonemaildata(jsondata,datalis,retlis,jsondata['bodyhtml'])
        print(jsonfinal)
        r = requests.post(
                audience, 
                headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
                data=json.dumps(jsonfinal)  # possible request parameters
            )
        context['response']=r.status_code, r.text
        print(r.status_code, r.text)
        
        context['data']=jsonfinal
    else:
        form = DataForm()
        
    context['form']= form
    return render(request, "index.html", context)

def checkdataset(dname,query):
  a = []
  for y in query['dataset']:
    if y['dataset_name']==dname:
      a = y['query']
    else:
      pass
  return a


def is_date(string):
    try: 
        isoparse(string)
        return True
    except ValueError:
        return False

def extractdate(a):
  asp = a.split(" ")
  asp2 = list(map(lambda item: (item.replace("'","")), asp))
  result = map(is_date,asp2 )
  lis = list(compress(asp, list(result)))
  my_list = list(map(lambda item: (item.replace("'","")), lis))
  my_list.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d')) 
  return my_list

def makestringfromlis(lis):
  a = ""
  for x in lis:
    a = a + str(x) + " "
  return a

import re
def getparenthesis(x):
      a = x[x.find("(")+1:x.find(")")].split(",")
      return a
      
def mixmatch(input,jsondata):
  regex = r"\{(.*?)\}"
  matches = re.finditer(regex, input, re.MULTILINE | re.DOTALL)
  lishttp = []
  for matchNum, match in enumerate(matches):
      for groupNum in range(0, len(match.groups())):
          lishttp.append(match.group(0))
  retlis = {}
  datalis = []

  for x in lishttp:
      e = {
          "serve_type": "",
          "dataset_name": "",
          "ref_column": "receiver_id"
      }
      if  'partner' in x:
        retlis[x]='{{partner}}'
      elif 'tanggal(' in x:
        retlis[x]= makestringfromlis(extractdate(checkdataset(x[x.find("(")+1:x.find(")")].split(',')[0],jsondata)))
        # retlis[x]=
      elif 'table(' in x:
        dsetname = getparenthesis(x)
        e['serve_type'] = 'table'
        e['dataset_name'] = str(dsetname[0])
        if len(dsetname)==1:
          retlis[x]=" Table Data: \n"+"{{"+"table_"+str(dsetname[0])+"}}"
        else:
          retlis[x]=str(dsetname[1])+"\n"+"{{"+"table_"+str(dsetname[0])+str(dsetname[1].replace(" ",""))+"}}"
          e['title'] = str(dsetname[1])
        datalis.append(e)
      elif 'image(' in x:
        dsetname = getparenthesis(x)
        e['serve_type'] = 'image'
        e['dataset_name'] = str(dsetname[0])
        if len(dsetname)==1:
          retlis[x]=" Plot Data: \n"+"{{"+"image_"+str(dsetname[0])+"}}"
        else:
          retlis[x]=str(dsetname[1])+"\n"+"{{"+"image_"+str(dsetname[0])+str(dsetname[1].replace(" ",""))+"}}"
          e['title'] = str(dsetname[1])
        datalis.append(e)
        print(datalis)
  return retlis, datalis

def changematchtohtml(input,html):
  a = html
  for key,value in input.items():
    a = a.replace(key,value)
  k = a.split('\n')
  htmljadi = ""
  for x in k:
    htmljadi = htmljadi + '<p style="font-size:10px" >'+str(x)+'</p>'
  return htmljadi

def addbaru(item):
  item["serve_type"]="attachment"
  return item


def makejsonemaildata(jsonbaru,datalis,retlis,html):
  a = {"type":"dataset",
      "queries": jsonbaru['dataset']
      }
  attachlist = [addbaru(item) for item in jsonbaru['attachment']]
  datalis.extend(attachlist)
  b = {"data":datalis}
  baru = {
      "type": "email_data",
      "sender": jsonbaru['sender'],
      "receiver": jsonbaru['receiver'],
      "receiver_table" : jsonbaru['receiver_table'],
      "cc": jsonbaru['cc'],
      "bcc": jsonbaru['bcc'],
      "subject": jsonbaru['subject'],
      "bodyhtml": changematchtohtml(retlis,html)
  }
  baru.update(b)
  retjson = [a,baru]
  return retjson