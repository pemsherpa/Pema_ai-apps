
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
        }
        for step in scope_steps
    ]

    return JsonResponse({"data": results}, safe=False)


#MY CODE

# @csrf_exempt
# def shopping_cart_content(request):
#     print("Get shopping cart method.")
#     return JsonResponse("Hello world",status=200)

@csrf_exempt
def shopping_cart_content(request):
    """
    API to fetch ShoppingCartContent data based on company_id.
    """
    print("Get shopping cart method.")
    if request.method != "GET":
        return JsonResponse({"error": "Only GET requests are allowed."}, status=405)

    company_id = request.GET.get('company_id')
    if not company_id:
        return JsonResponse({"error": "company_id parameter is required."}, status=400)

    print(company_id)
    try:
        # Filter records by company_id
        records = ShoppingCartContent.objects.filter(company_id=company_id)

        # Prepare JSON response
        records_data = [
            {
                "id": record.id,
                "year": record.scope_step.year,
                "quarter": record.scope_step.quarter,
                "scope_type": record.scope_step.scope_type,
                "description": record.scope_step.description,
                "difficulty": record.scope_step.difficulty,
                "transition_percentage": record.scope_step.transition_percentage,
                "company_name": record.company.company_id,
                "plan_name": record.scope_step.plan.plan_name if record.scope_step.plan else None,
                "provider_name": record.scope_step.plan.provider.providers_name if record.scope_step.plan and record.scope_step.plan.provider else None,
            }
            for record in records
        ]
        print(records_data)

        return JsonResponse({"shopping_cart_content": records_data}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def delete_shopping_cart_content(request):
    """
    API to delete a ShoppingCartContent row based on plan_name, company_id, and provider_name.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    try:
        body = json.loads(request.body)
        plan_name = body.get('plan_name')
        company_id = body.get('company_id')
        provider_name = body.get('provider_name')

        # Validate inputs
        if not (plan_name and company_id and provider_name):
            return JsonResponse({"error": "plan_name, company_id, and provider_name are required."}, status=400)

        # Query the record
        record = ShoppingCartContent.objects.filter(
            Q(scope_step__plan__plan_name=plan_name) &
            Q(company_id=company_id) &
            Q(scope_step__plan__provider__providers_name=provider_name)
        ).first()

        if not record:
            return JsonResponse({"error": "No matching record found."}, status=404)

        # Delete the record
        record.delete()
        return JsonResponse({"message": "Record deleted successfully."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


class ShoppingCartContentView(APIView):
    def get(self, request):
        company_id = request.GET.get('company_id')
        if not company_id:
            return JsonResponse({"error": "company_id parameter is required."}, status=400)

        try:
            # Query the database for shopping cart contents by company_id
            records = ShoppingCartContent.objects.filter(company_id=company_id)

            if not records.exists():
                return JsonResponse({"error": "No records found for the given company_id."}, status=404)

            # Serialize the query results
            serializer = ShoppingCartContentSerializer(records, many=True)
            return JsonResponse({"shopping_cart_content": serializer.data}, status=200)

        except Exception as e:
            # Catch unexpected errors
            return JsonResponse({"error": str(e)}, status=500)
