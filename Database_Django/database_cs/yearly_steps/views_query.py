
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
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    scope_type = request.GET.get('scope_type')
    description = request.GET.get('description')
    difficulty = request.GET.get('difficulty')
    transition_percentage = request.GET.get('transition_percentage')
    company_id = request.GET.get('company_id')
    plan_name = request.GET.get('plan_name')
    provider_name = request.GET.get('provider_name')

    
    filters = {}
    if year:
        filters['year'] = year
    if quarter:
        filters['quarter'] = quarter
    if scope_type:
        filters['scope_type'] = scope_type
    if description:
        filters['description__icontains'] = description
    if difficulty:
        filters['difficulty'] = difficulty
    if transition_percentage:
        filters['transition_percentage'] = transition_percentage

    
    if company_id:
        company = get_object_or_404(Companys, company_id=company_id)
        filters['company'] = company

    if plan_name:
        plans = Plans.objects.filter(plan_name=plan_name)  # Use filter instead of get
        if plans.exists():
            filters['plan__id__in'] = plans.values_list('id', flat=True)
        else:
            return JsonResponse({"error": f"No plans found with name '{plan_name}'"}, status=404)

    if provider_name:
        providers = Providers.objects.filter(providers_name=provider_name)
        if providers.exists():
            provider_ids = providers.values_list('id', flat=True)
            plan_ids = Plans.objects.filter(provider_id__in=provider_ids).values_list('id', flat=True)
            filters['plan__id__in'] = plan_ids
        else:
            return JsonResponse({"error": f"No providers found with name '{provider_name}'"}, status=404)

    
    scope_steps = ScopeSteps.objects.filter(**filters).select_related('company', 'plan__provider')

    
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
            "plan_name": step.plan.plan_name,
            "provider_name": step.plan.provider.providers_name,
        }
        for step in scope_steps
    ]

    return JsonResponse({"data": results}, safe=False)
