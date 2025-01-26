from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from yearly_steps.models import *
import json
import os
import numpy as np
from scipy.stats import zscore
from django.apps import apps
from django.db import models, connection
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_http_methods
# CART


@csrf_exempt
@require_http_methods(["GET"]) 
def get_shopping_cart(request):
    try:
        # Get company_id from query parameters
        company_id = request.GET.get("company_id")
        print(company_id)
        if not company_id:
            return JsonResponse({"status": "error", "message": "Missing company_id parameter."}, status=400)

        # Fetch data from ShoppingCartContent filtered by company_id
        shopping_cart_items = ShoppingCartContent.objects.filter(company_id=company_id).select_related('company', 'scope_step')

        # Serialize the data
        data = [
            {
                "id": item.id,
                "company_name": item.company.name,  # Access related Companys name
                "scope_step_name": item.scope_step.name,  # Access related ScopeSteps name
            }
            for item in shopping_cart_items
        ]

        return JsonResponse({"status": "success", "data": data}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)



# @csrf_exempt
# @require_http_methods(["POST"]) 
# def delete_shopping_cart(request):
#     try:
#         # Parse the JSON body
        
#         body = json.loads(request.body)
#         company_id = body.get("company_id")
#         scope_step_id = body.get("scope_step_id")

#         # Validate input
#         if not (company_id and scope_step_id):
#             return JsonResponse({"status": "error", "message": "Missing required parameters."}, status=400)

#         # Fetch and delete the item
#         shopping_cart_item = get_object_or_404(
#             ShoppingCartContent,
#             company_id=company_id,
#             scope_step_id=scope_step_id,
#         )
#         shopping_cart_item.delete()

#         return JsonResponse({"status": "success", "message": "Item deleted successfully."}, status=200)
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)}, status=500)



