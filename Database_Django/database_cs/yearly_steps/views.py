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
# CART

@csrf_exempt
@require_http_methods(["POST"])  # Ensure only POST requests are allowed
def add_shopping_cart(request):
    try:
        # Parse input data from request body
        import json
        body = json.loads(request.body.decode('utf-8'))
        provider_name = body.get('provider_name')
        company_id = body.get('company_id')
        plan_name = body.get('plan_name')

        # Validate input data
        if not (provider_name and company_id and plan_name):
            return JsonResponse(
                {"error": "Missing required fields: provider_name, company_id, plan_name."},
                status=400
            )

        # Fetch the company
        company = get_object_or_404(Companys, company_id=company_id)

        # Fetch the provider
        provider = get_object_or_404(Providers, providers_name=provider_name)

        # Fetch the plan
        plan = get_object_or_404(Plans, provider=provider, plan_name=plan_name)

        # Fetch the corresponding scope steps
        scope_steps = ScopeSteps.objects.filter(company=company, plan=plan)

        if not scope_steps.exists():
            return JsonResponse(
                {"error": "No scope steps found for the specified company and plan."},
                status=404
            )

        # Add each scope step to the shopping cart
        added_steps = []
        already_in_cart = []

        for scope_step in scope_steps:
            shopping_cart_entry, created = ShoppingCartContent.objects.get_or_create(
                company=company, scope_step=scope_step
            )
            if created:
                added_steps.append(scope_step.id)  # Use scope_step.id for unique identification
            else:
                already_in_cart.append(scope_step.id)

        response_data = {
            "message": "Shopping cart updated successfully.",
            "added_steps": added_steps,
            "already_in_cart": already_in_cart,
        }

        return JsonResponse(response_data, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
@require_http_methods(["GET"]) 
def get_shopping_cart_content(request):
    try:
        # Get company_id from query parameters
        company_id = request.GET.get("company_id")

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



@csrf_exempt
@require_http_methods(["POST"]) 
def delete_shopping_cart_item(request):
    try:
        # Parse the JSON body
        
        body = json.loads(request.body)
        company_id = body.get("company_id")
        scope_step_id = body.get("scope_step_id")

        # Validate input
        if not (company_id and scope_step_id):
            return JsonResponse({"status": "error", "message": "Missing required parameters."}, status=400)

        # Fetch and delete the item
        shopping_cart_item = get_object_or_404(
            ShoppingCartContent,
            company_id=company_id,
            scope_step_id=scope_step_id,
        )
        shopping_cart_item.delete()

        return JsonResponse({"status": "success", "message": "Item deleted successfully."}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)



