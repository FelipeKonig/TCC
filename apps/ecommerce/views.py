from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging

# Create your views here.
logger = logging.getLogger(__name__)


def home_page(request):
    return render(request, 'ecommerce/pagina-index.html')

