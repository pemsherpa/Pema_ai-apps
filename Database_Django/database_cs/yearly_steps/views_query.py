
from django.apps import apps
from django.db import connection, models
from django.http import JsonResponse
from pgvector.django import VectorField
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.apps import apps
from django.shortcuts import get_object_or_404
from .models import *


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


