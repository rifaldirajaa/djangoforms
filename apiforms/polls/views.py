from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from polls.forms import EmailForm, JsonForm, TypeForm, BasicForm, DataForm, EditDataForm, DeleteDataForm
import os
import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests
from formtools.wizard.views import SessionWizardView
from datetime import datetime
from itertools import compress
from dateutil.parser import parse,isoparse
import re
import google.auth
from google.cloud import scheduler_v1
from google.cloud.scheduler_v1 import HttpTarget,OidcToken
import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, DataEmail
from google.protobuf import duration_pb2, field_mask_pb2
from django.http import HttpResponse
from django.urls import reverse_lazy

sapath = '/Users/buttercup/Documents/GitHub/key/celerates-playground-318603-f9d994464b15.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = sapath
requestgcp = google.auth.transport.requests.Request()
audience = 'https://asia-southeast2-celerates-playground-318603.cloudfunctions.net/xl_email_ready'
TOKEN = google.oauth2.id_token.fetch_id_token(requestgcp, audience)
projectid = 'celerates-playground-318603'

class HomeView(ListView):
  model = DataEmail
  template_name = 'home.html'

class ArticleView(DetailView):
  model = DataEmail
  template_name = 'index.html'
  fields = '__all__'
  def get_form(self):
    form = self.form_class(instance=self.object)
    return form

  def get_context_data(self, **kwargs):
    context = super(ArticleView, self).get_context_data(**kwargs)
    context
    return context

class AddPostView(CreateView):
  model = DataEmail
  template_name = 'addpost.html'

class UpdatePostView(UpdateView):
  model = DataEmail
  form_class = EditDataForm
  template_name='edit.html'
  # fields = '__all__'

  def post(self,request, pk):
    context ={}
    form = EditDataForm(request.POST or None)
    if form.is_valid():
      jsondata = json.loads(form.data['items'])
      print(jsondata)
      retlis,datalis = mixmatch(jsondata['bodyhtml'],jsondata)
      jsonfinal = makejsonemaildata(jsondata,datalis,retlis,jsondata['bodyhtml'])
      
      olddata = DataEmail.objects.get(id=pk)
      olddata.items = jsondata

      print(jsonfinal)
      if len(jsondata['schjobid'])>0:
        client,project = get_cloud_scheduler_client(sapath)
        jobid = jsondata['schjobid']
        schedule = makecron(jsondata)
        timezone = jsondata['schtimezone']
        description = jsondata['schdescription']
        try:
          job = update_job(client, projectid, jobid, schedule, jsonfinal, description, timezone, location='asia-southeast2')
          context['data']=job
          olddata.save()
        except Exception as e:
          context['data']=e
      # elif len(jsondata['schjobid'])==0:
        
        # r = requests.post(
        #         audience, 
        #         headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
        #         data=json.dumps(jsonfinal)  # possible request parameters
        #     )
        # context['response']=r.status_code, r.text
        # print(r.status_code, r.text)
        # context['data']=jsonfinal
    else:
        form = EditDataForm()
    context['form']= form
    return render(request, "index.html", context)
  # fields = '__all__'

class DeletePostView(DeleteView):
  model = DataEmail
  template_name = 'delete_post.html'
  success_url=reverse_lazy('home')
  

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

# def indexdataedit(request):
#   context ={}
#   form = EditDataForm(request.POST or None)
#   context['form']= form
#   return render(request, "edit.html", context)

def indexdata(request):
    context ={}
    form = DataForm(request.POST or None)
    print(form.data)
    if form.is_valid():
        formlist = [form]
        jsondata = json.loads(form.data['items'])
        print(jsondata)
        retlis,datalis = mixmatch(jsondata['bodyhtml'],jsondata)
        jsonfinal = makejsonemaildata(jsondata,datalis,retlis,jsondata['bodyhtml'])
        print(jsonfinal)

        if len(jsondata['schjobid'])>0:
          client,project = get_cloud_scheduler_client(sapath)
          jobid = jsondata['schjobid']
          schedule = makecron(jsondata)
          timezone = jsondata['schtimezone']
          description = jsondata['schdescription']
        #   try:
        #     # output=create_job(client, projectid, jobid, schedule, jsonfinal, timezone, description, location='asia-southeast2')
        #     # print('Succes')
        #     # print(output)
        #     # form.save()
        #     context['data']=output
        #   except Exception as e:
        #     print('Failed')
        #     print(e)
        #     context['data']=e
        # elif len(jsondata['schjobid'])==0:
        #   r = requests.post(
        #           audience, 
        #           headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
        #           data=json.dumps(jsonfinal)  # possible request parameters
        #   )
        #   if r.status_code=='200':
        #     context['response']=r.status_code, r.text
        #     form.save()
        #     print(r.status_code, r.text)
        #   else:
        #     context['response']=r.status_code, r.text
        #   context['data']=jsonfinal
    else:
        print("form is not valid!")
        print(form.errors.as_json())
        form = DataForm()
        
    context['form']= form
    return render(request, "index.html", context)



def checkschedule(request):
  context ={}
  client,project = get_cloud_scheduler_client(sapath)
  getlist = get_job_list(client, project, region='asia-southheast1')
  context['job']=getlist
  return render(request, "index.html", context)

def checkdataset(dname,query):
  a = []
  for y in query['dataset']:
    if y['dataset_name']==dname:
      a = y
    else:
      pass
  return a

def checktblname(name,data):
  a = []
  for y in data:
      if y['table_name']==name:
        a = y
      else:
        pass
  return a


def is_date(string):
    try: 
        isoparse(string)
        return True
    except ValueError:
        return False

def extractdate(a,timespec):
  asp = a.split(" ")
  asp2 = list(map(lambda item: (item.replace("'","")), asp))
  result = map(is_date,asp2 )
  lis = list(compress(asp, list(result)))
  my_list = list(map(lambda item: (item.replace("'","")), lis))
  my_list.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d')) 
  my_list = list(map(lambda item: datetime.strptime(item, '%Y-%m-%d'),my_list))

  if timespec == 'day':
    
    my_list = [str(date.strftime('%Y'))+'-'+str(date.strftime('%m'))+'-'+str(date.strftime('%d')) for date in my_list]
    
  elif timespec == 'month':
    my_list = [str(date.strftime('%Y'))+'-'+str(date.strftime('%m')) for date in my_list]
  
  elif timespec == 'year':
    my_list = [str(date.strftime('%Y')) for date in my_list]
  else:
    my_list = ['please specify the time correctly "Tanggal(datasetname,day/month/year)"']

  return my_list

def makestringfromlis(lis):
  a = ""
  lis.sort()
  for x in lis:
    a = a + str(x) + " "
  return a


def getparenthesis(x):
      a = x[x.find("(")+1:x.find(")")].split(",")
      return a
      
def mixmatch(input,inputjson):
  regex = r"\{(.*?)\}"
  matches = re.finditer(regex, input, re.MULTILINE | re.DOTALL)
  lishttp = []
  for matchNum, match in enumerate(matches):
      for groupNum in range(0, len(match.groups())):
          lishttp.append(match.group(0))
  retlis = {}
  datalis = []

  for x in lishttp:
      e = {}
      if  'recepient' in x:
        retlis[x]='{{recepient}}'

      elif 'table(' in x:
        dsetname = getparenthesis(x)
        tbljsontemp = inputjson['preprocess_data'][0]['Table']
        tbljson= checktblname(str(dsetname[0]),tbljsontemp)
        tbldset = checkdataset(tbljson['dataset_name'],inputjson)
        e['serve_type'] = 'table'
        e['dataset_name'] = tbljson['dataset_name']
        e['table_name'] = tbljson['table_name']
        e['preprocess_show_column_'] = tbljson['show_column']
        e['ref_column'] = tbldset['col_ref']
        if len(dsetname)==1:
          retlis[x]=" Table Data: \n"+"{{"+"table_"+str(dsetname[0])+"}}"
        else:
          retlis[x]=str(dsetname[1])+"\n"+"{{"+"table_"+str(dsetname[0])+str(dsetname[1].replace(" ",""))+"}}"
          e['title'] = str(dsetname[1])
        datalis.append(e)

      elif 'image(' in x:
        dsetname = getparenthesis(x)
        tbljson = inputjson['preprocess_data'][0]
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
    htmljadi = htmljadi + "<p style='font-size:20px' >"+str(x)+"</p>"
  return htmljadi

def addbaru(item,inputjson):
  item["serve_type"]="attachment"
  item["attachment_name"]=item["attachment_name"].replace("{recepient}","{{recepient}}")
  tbldset = checkdataset(item['dataset_name'],inputjson)
  item['ref_column'] = tbldset['col_ref']
  # item["ref_column"]="receiver_id"
  return item

def addtbl(item):
   item["serve_type"]="table"
   return item

def changematch(input,html):
  a = html
  for key,value in input.items():
    a = a.replace(key,value)
  return a

def makejsonemaildata(jsonbaru,datalis,retlis,html):
  retlist_a,datalis2 = mixmatch(jsonbaru['subject'],jsonbaru)
  subject_ready = changematch(retlist_a,jsonbaru['subject'])
  a = {"type":"dataset",
      "queries": jsonbaru['dataset']
      }
  attachlist = [addbaru(item,jsonbaru) for item in jsonbaru['attachment']]
  # tbllist = [addtbl(item) for item in jsonbaru['preprocess_data'][0]['Table']]
  datalis.extend(attachlist)
  # datalis.extend(datalis2)
  b = {"data":datalis}
  baru = {
      "type": "email_data",
      "sender": jsonbaru['sender'],
      "receiver": jsonbaru['receiver'],
      "receiver_table" : jsonbaru['receiver_table'],
      "cc": jsonbaru['cc'],
      "bcc": jsonbaru['bcc'],
      "subject": subject_ready,
      "bodyhtml": changematchtohtml(retlis,html)
  }
  baru.update(b)
  retjson = [a,baru]
  return retjson

def get_cloud_scheduler_client(sa_credential_filepath):
    credentials, project_id = google.auth.load_credentials_from_file(sa_credential_filepath)
    client = scheduler_v1.CloudSchedulerClient(credentials=credentials)
    return client, project_id


def get_job_list(cs_client, project_id, region='asia-southheast1'):
    request = scheduler_v1.ListJobsRequest(parent = f"projects/{project_id}/locations/{region}")
    page_result = cs_client.list_jobs(request=request)
    return [r.name for r in page_result]


def create_job(cs_client, project_id, job_id, schedule, bodyreq, timezone, description, location='asia-southeast2'):
    # parent= cs_client.location_path(project_id, location)
    if len(timezone)==0:
      timezone='Asia/Jakarta'
    parent = f'projects/{project_id}/locations/{location}'
    job_name = f'projects/{project_id}/locations/{location}/jobs/{job_id}'
    ht = HttpTarget(
        http_method = "POST",
        uri         = "https://asia-southeast2-celerates-playground-318603.cloudfunctions.net/xl_email_ready",
        headers     = {"Content-Type": "application/json"},
        # body        = base64.b64decode("{\"foo\":\"bar\"}")
        body        = json.dumps(bodyreq).encode("utf-8"),
        oidc_token  = OidcToken(service_account_email="querytobq@celerates-playground-318603.iam.gserviceaccount.com")
    )
    job_dict = {
        'name': f'projects/{project_id}/locations/{location}/jobs/{job_id}',
        'http_target': ht,
        'schedule': schedule,
        'time_zone': timezone,
        'description': description
    }
    job = cs_client.create_job(parent=parent, job=job_dict)

    return job

def update_job(cs_client, project_id, job_id, schedule, bodyreq, timezone, description, location='asia-southeast2'):
    # parent= cs_client.location_path(project_id, location)
    if len(timezone)==0:
      timezone='Asia/Jakarta'
    parent = f'projects/{project_id}/locations/{location}'
    job_name = f'projects/{project_id}/locations/{location}/jobs/{job_id}'
    # ht = HttpTarget(
    #     http_method = "POST",
    #     uri         = "https://asia-southeast2-celerates-playground-318603.cloudfunctions.net/xl_email_ready",
    #     headers     = {"Content-Type": "application/json"},
    #     # body        = base64.b64decode("{\"foo\":\"bar\"}")
    #     body        = json.dumps(bodyreq).encode("utf-8"),
    #     oidc_token  = OidcToken(service_account_email="querytobq@celerates-playground-318603.iam.gserviceaccount.com")
    # )
    # job_dict = {
    #     'http_target': ht,
    #     'schedule': schedule,
    #     'time_zone': timezone,
    #     'description': description
    # }
    # job = cs_client.create_job(parent=parent, job=job_dict)
    ht = scheduler_v1.HttpTarget()
    ht.http_method = "POST"
    ht.uri = "https://asia-southeast2-celerates-playground-318603.cloudfunctions.net/xl_email_ready"
    ht.headers = {"Content-Type": "application/json"}
    ht.body = json.dumps(bodyreq).encode("utf-8")
    ht.oidc_token = OidcToken(service_account_email="querytobq@celerates-playground-318603.iam.gserviceaccount.com")
    jobedit = scheduler_v1.Job()
    jobedit.name = job_name
    jobedit.http_target = ht
    jobedit.schedule = schedule
    jobedit.description = description
    jobedit.time_zone = timezone
    update_mask = field_mask_pb2.FieldMask(paths=['http_target','schedule','time_zone','description'])
    request = scheduler_v1.UpdateJobRequest(
          job=jobedit,
          update_mask=update_mask
      )
    response = cs_client.update_job(request=request)
    return response

def makecron(jsonbaru):
  if len(jsonbaru['Custom'])>0:
    cronsch = jsonbaru['Custom']
  else:
    if len(jsonbaru['Daily']['time'])>0:
      timearr = jsonbaru['Daily']['time'].split(":")
      time = ' '.join([timearr[1],timearr[0]])
    else:
      time = ' '.join(['00','00'])
    if len(jsonbaru['Monthly'])>0:
      daymonth = jsonbaru['Monthly']
    else:
      daymonth = "*"
    if len(jsonbaru['Yearly'])>0:
      monthyear = ','.join(map(str,jsonbaru['Yearly']))
    else:
      monthyear = "*"
    if len(jsonbaru['Weekly'])>0:
      dayweek = ','.join(map(str,jsonbaru['Weekly']))
    else:
      dayweek = "*"
    cronsch=" ".join([time,daymonth,monthyear,dayweek])
  return cronsch

