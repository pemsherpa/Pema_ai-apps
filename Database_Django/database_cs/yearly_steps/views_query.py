
from django.apps import apps
from django.db import connection, models
from django.http import JsonResponse
from pgvector.django import VectorField
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.apps import apps
from django.shortcuts import get_object_or_404
from .models import *
from yearly_steps.models import ShoppingCartContent
from django.db.models import Q
import json
from .serializers import *
from django.views.decorators.http import require_http_methods

from yearly_steps.serializers import ShoppingCartContentSerializer
from rest_framework.views import APIView

def get_table_records(request, table_name):
    try:
        # Replace 'yearly_steps' with the actual app name
        model = apps.get_model(app_label='yearly_steps', model_name=table_name)
        if not model:
            return JsonResponse({"error": f"Table '{table_name}' does not exist."}, status=404)

        # Fetch all records from the table
        records = model.objects.all()

        # Convert the records to a list of dictionaries
        records_data = []
        for record in records:
            record_dict = {}
            for field in model._meta.fields:
                value = getattr(record, field.name)
                if field.related_model:  # Check if field is a related object
                    record_dict[field.name] = value.pk if value else None  # Use primary key for related objects
                else:
                    record_dict[field.name] = value  # Use the field's value directly
            records_data.append(record_dict)

        # Return the data as JSON
        return JsonResponse({table_name: records_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def query_scope_steps(request):
    print("Querying.......")
    quarter = request.GET.get('quarter')
    company_id = request.GET.get('company')
    year = request.GET.get('year')  # Can contain multiple years (comma-separated)

    filters = {}

    # Filter by quarter
    if quarter:
        filters['quarter'] = quarter

    # Filter by company
    if company_id:
        company = get_object_or_404(Companys, company_id=company_id)
        filters['company'] = company

    # Filter by multiple years
    if year:
        year_list = [int(y) for y in year.split(',') if y.isdigit()]
        if year_list:
            filters['year__in'] = year_list

    # Query the database with filters (or return all if no filters are provided)
    scope_steps = ScopeSteps.objects.filter(**filters).select_related('company', 'plan__provider')

    # Prepare results
    results = [
        {
            "id": step.id,
            "year": step.year,
            "quarter": step.quarter,
            "scope_type": step.scope_type,
            "description": step.description,
            "difficulty": step.difficulty,
            "transition_percentage": step.transition_percentage,
            "company_name": step.company.company_id,
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
        }
        for step in scope_steps
    ]

    response = JsonResponse({"data": results}, safe=False)
    response["Access-Control-Allow-Origin"] = "http://localhost:4200"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"

    return JsonResponse({"data": results}, safe=False)


# @csrf_exempt
# def query_scope_steps(request):
#     print("Querying.......")
#     quarter = request.GET.get('quarter')
#     company_id = request.GET.get('company')
#     year = request.GET.get('year')  # Can contain multiple years (comma-separated)
    
#     filters = {}

#     # Filter by quarter
#     if quarter:
#         filters['quarter'] = quarter

#     # Filter by company
#     if company_id:
#         company = get_object_or_404(Companys, company_id=company_id)
#         filters['company'] = company

#     # Filter by multiple years
#     if year:
#         year_list = [int(y) for y in year.split(',') if y.isdigit()]
#         if year_list:
#             filters['year__in'] = year_list

#     # Query the database with filters (or return all if no filters are provided)
#     scope_steps = ScopeSteps.objects.filter(**filters).select_related('company', 'plan__provider')

#     # Prepare results
#     results = [
#         {
#             "id": step.id,
#             "year": step.year,
#             "quarter": step.quarter,
#             "scope_type": step.scope_type,
#             "description": step.description,
#             "difficulty": step.difficulty,
#             "transition_percentage": step.transition_percentage,
#             "company_name": step.company.company_id,
#             "plan_name": step.plan.plan_name if step.plan else None,
#             "provider_name": step.plan.provider.providers_name if step.plan and step.plan.provider else None,
#             "provider_phone_number": step.plan.provider.phone_number if step.plan and step.plan.provider else None,
#             "provider_website_link": step.plan.provider.website_link if step.plan and step.plan.provider else None,
#             "provider_description": step.plan.provider.description if step.plan and step.plan.provider else None,
#         }
#         for step in scope_steps
#     ]

#     return JsonResponse({"data": results}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])  # Ensure only POST requests are allowed
def add_shopping_cart(request):
    try:
        data = json.loads(request.body)
        # Parse input data from query parameters
        provider_name = data.get('provider_name')
        company_name = data.get('company_name')
        plan_name = data.get('plan_name')

        # Validate input data
        if not (provider_name and company_name and plan_name):
            if not provider_name:
                return JsonResponse(
                    {"error": "Missing required fields: provider_name"},
                    status=400
                )
            elif not company_name:
                return JsonResponse(
                    {"error": "Missing required fields:company_name"},
                    status=400
                )
            elif not plan_name:
                return JsonResponse(
                    {"error": "Missing required fields: plan_name."},
                    status=400
                )
            else:
                return JsonResponse(
                    {"error:" "I have no clue this is so weird"}
                )

        # Fetch the company
        company = get_object_or_404(Companys, company_id=company_name)

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

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
