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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ShoppingCartContent

@csrf_exempt  # Exempt from CSRF for testing (remove in production)
@require_http_methods(["GET"])  # Restrict method to GET
def get_shopping_cart_content(request):
    try:
        # Get 'company_id' from query parameters
        company_id = request.GET.get("company_id")

        # Validate input
        if not company_id:
            return JsonResponse({"status": "error", "message": "Missing 'company_id' parameter."}, status=400)

        # Fetch records for the given company_id
        shopping_cart_items = ShoppingCartContent.objects.filter(company_id=company_id)

        # Serialize the data
        data = []
        for item in shopping_cart_items:
            step = item.scope_step  # Follow foreign key to ScopeSteps
            data.append({
                "id": step.id,
                "year": step.year,
                "quarter": step.quarter,
                "scope_type": step.scope_type,
                "description": step.description,
                "difficulty": step.difficulty,
                "transition_percentage": step.transition_percentage,
                "company_name": step.company.company_id if step.company else None,
                "plan_name": step.plan.plan_name if step.plan else None,
                "provider_name": step.plan.provider.providers_name if step.plan and step.plan.provider else None,
                "phone_number": step.plan.provider.phone_number if step.plan and step.plan.provider else None,
                "website_link": step.plan.provider.website_link if step.plan and step.plan.provider else None,
                "provider_description": step.plan.provider.description if step.plan and step.plan.provider else None,
                "carbon_cost": step.plan.carbon_cost if step.plan else None,
                "total_cost": step.plan.total_cost if step.plan else None,
                "peak_cost": step.plan.peak_cost if step.plan else None,
                "off_peak_cost": step.plan.off_peak_cost if step.plan else None,
                "data": step.plan.data if step.plan else None,
            })

        # Return JSON response
        return JsonResponse({"status": "success", "data": data}, status=200)

    except Exception as e:
        # Handle unexpected errors
        return JsonResponse({"status": "error", "message": str(e)}, status=500)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import ShoppingCartContent, Plans, Providers, Companys, ScopeSteps
import json

@csrf_exempt
@require_http_methods(["POST"])  # Ensures that only POST requests are allowed
def delete_shopping_cart(request):
    try:
        # Debug: Print the request method and body for troubleshooting
        print(f"Request method: {request.method}")
        print(f"Request body: {request.body.decode('utf-8')}")  # Log the request body

        # Ensure the body is not empty
        if not request.body:
            return JsonResponse({"status": "error", "message": "Request body is empty."}, status=400)

        # Parse the JSON body
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)

        # Get the plan_name, company_id, and provider_name from the request body
        plan_name = body.get("plan_name")
        company_id = body.get("company_id")
        provider_name = body.get("provider_name")

        # Ensure plan_name, company_id, and provider_name are provided
        if not plan_name or not company_id or not provider_name:
            return JsonResponse({"status": "error", "message": "plan_name, company_id, and provider_name are required."}, status=400)

        # Fetch the related provider, plan, and scope_step
        provider = get_object_or_404(Providers, providers_name=provider_name)
        plan = get_object_or_404(Plans, plan_name=plan_name, provider=provider)
        company = get_object_or_404(Companys, company_id=company_id)

        # Fetch the corresponding scope_step for the given company_id and plan
        scope_step = get_object_or_404(ScopeSteps, company=company, plan=plan)

        # Delete the shopping cart item that matches the scope_step_id and company_id
        shopping_cart_item = get_object_or_404(ShoppingCartContent, company=company, scope_step=scope_step)
        
        # Deleting the item
        shopping_cart_item.delete()

        # Return a success message
        return JsonResponse({"status": "success", "message": "ShoppingCartContent item deleted successfully."}, status=200)

    except Exception as e:
        # Catch any unexpected exceptions and return a general error
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
