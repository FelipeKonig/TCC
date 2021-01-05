from django.shortcuts import render

import logging

# Create your views here.
logger = logging.getLogger(__name__)

def home_page(request):
    return render(request, 'ecommerce/page-index.html')
