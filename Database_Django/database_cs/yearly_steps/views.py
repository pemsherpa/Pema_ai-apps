from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from yearly_steps.models import *
import json
import os
import numpy as np
from scipy.stats import zscore
from django.apps import apps
from django.db import models, connection

# CART
@csrf_exempt
def add_shopping_cart(request):
    if request.method == 'POST':
        try:
            print("Add to shopping cart")
            # Parse JSON data
            data = json.loads(request.body)
            print("Extracted JSON input successfully.....")
            print("Decoded JSON:", data)
            # Extract fields from JSON
            company_id = data.get('company_id')
            name=data.get('title')
            costSavings = data.get('costSavings')
            co2savings = data.get('co2Savings')
            transition = data.get('transition')
            print("Extracted JSON input2 successfully.....")

            print("Fields",company_id, name, costSavings, co2savings, transition)
            
            # Validate required fields
            if not all([company_id, transition]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            print("Extracted JSON input3 successfully.....")
            # Create and save the record
            record = ShoppingCartContent(
                company_id=company_id,
                name=name,
                costSavings=costSavings,
                co2savings=co2savings,
                transition=transition,
                )
            print("Extracted JSON input4 successfully.....")
            record.save()
            print("Record: ", record)
            

            # Return success response
            return JsonResponse({'message': 'Record added successfully', 'id': record.id}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)
    


@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            provider_id = int(data.get('provider_id',0))
            company_id = data.get('company_id', 1)  # Default to company_id = 1 if not provided
            plan_id = int(data.get('plan_id',0))

            if not provider_id:
                return JsonResponse({"success": False, "message": "provider_id is required."}, status=400)

            provider = Providers.objects.filter(id=provider_id).first()
            print(provider)
            plan = Plans.objects.filter(id=plan_id).first()
            print(plan)
            ShoppingCartContent.objects.create(
                company_id=company_id,
                providers=provider,
                plan=plan   
            )

            return JsonResponse({"success": True, "message": "Provider added to the shopping cart successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Providers.DoesNotExist:
            return JsonResponse({"success": False, "message": "Provider not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method. Use POST."}, status=405)
