from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from polls.forms import EmailForm, JsonForm
import os
import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests

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

