# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from Ecom_PC_portal.myapp.models import Document
from Ecom_PC_portal.myapp.forms import DocumentForm
import time
import subprocess
from Ecom_PC_portal.myapp import label_image
import os

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    path_for_prediction = "/Users/gaurav/Desktop/Flipkart/Ecom_PC_portal"+documents[len(documents)-1].docfile.url
    path = documents[len(documents)-1].docfile.url
    # Render list page with the documents and the form
    # change categories to actual categories returned from predictor
    # change the color change to the predicted color value
    classes_scores = get_prediction( path_for_prediction)
    return render(
        request,
        'list.html',
        {'form': form, 'path':path, 'categories':["cat1","cat2","cat3"]
        , 'color':"Red", 'classes_scores':classes_scores}
    )

# get prediction from the trained model and return categories list, color - string,
# and two list for all categories name combined and their prooperties
def get_prediction(image_path = None):
    path = os.path.dirname(os.path.abspath(__file__))
    print("path:{}".format(path))
    print("image_path:{}".format(image_path))
    #run python command to fetch prediction.
    #if not image_path:
    output = label_image.predict(path, image_path)
    print("output is :{}".format(output))
    scores=["0.5","0.3","0.2"]
    classes=["cat11-cat12-cat13","cat21-cat22-cat23","cat31-cat32-cat33"]
    classes_scores = zip(classes, scores)
    return classes_scores
