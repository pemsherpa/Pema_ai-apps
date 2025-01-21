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



# @csrf_exempt
# def add_shopping_cart(request):
#     if request.method == 'POST':
#         try:
#             print("Add to shopping cart")
#             # Parse JSON data
#             data = json.loads(request.body)
#             print("Extracted JSON input successfully.....")
#             print("Decoded JSON:", data)
#             # Extract fields from JSON
#             company_id = data.get('company_id')
#             name=data.get('title')
#             costSavings = data.get('costSavings')
#             co2savings = data.get('co2Savings')
#             transition = data.get('transition')
#             print("Extracted JSON input2 successfully.....")

#             print("Fields",company_id, name, costSavings, co2savings, transition)
            
#             # Validate required fields
#             if not all([company_id, transition]):
#                 return JsonResponse({'error': 'Missing required fields'}, status=400)
#             print("Extracted JSON input3 successfully.....")
#             # Create and save the record
#             record = ShoppingCartContent(
#                 company_id=company_id,
#                 name=name,
#                 costSavings=costSavings,
#                 co2savings=co2savings,
#                 transition=transition,
#                 )
#             print("Extracted JSON input4 successfully.....")
#             record.save()
#             print("Record: ", record)
            

#             # Return success response
#             return JsonResponse({'message': 'Record added successfully', 'id': record.id}, status=201)
        
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
    
#     else:
#         return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)
    


# @csrf_exempt
# def add_to_cart(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             provider_id = int(data.get('provider_id',0))
#             company_id = data.get('company_id', 1)  # Default to company_id = 1 if not provided
#             plan_id = int(data.get('plan_id',0))

#             if not provider_id:
#                 return JsonResponse({"success": False, "message": "provider_id is required."}, status=400)

#             provider = Providers.objects.filter(id=provider_id).first()
#             print(provider)
#             plan = Plans.objects.filter(id=plan_id).first()
#             print(plan)
#             ShoppingCartContent.objects.create(
#                 company_id=company_id,
#                 providers=provider,
#                 plan=plan   
#             )

#             return JsonResponse({"success": True, "message": "Provider added to the shopping cart successfully."})

#         except json.JSONDecodeError:
#             return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
#         except Providers.DoesNotExist:
#             return JsonResponse({"success": False, "message": "Provider not found."}, status=404)
#         except Exception as e:
#             return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"}, status=500)

#     return JsonResponse({"success": False, "message": "Invalid request method. Use POST."}, status=405)
