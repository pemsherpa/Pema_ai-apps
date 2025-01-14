
from django.apps import apps
from django.db import connection, models
from django.http import JsonResponse
from pgvector.django import VectorField
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.apps import apps


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