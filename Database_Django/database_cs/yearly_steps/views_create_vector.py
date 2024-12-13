# CREATION OF VECTOR TABLE FOR ANOMALY DETECTION
from django.apps import apps
from django.db import connection, models
from django.http import JsonResponse
from pgvector.django import VectorField
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_and_update_vector_table(request):
    """
    Dynamically creates a vector table model for the Total_CO2e table,
    creates the table in the database, registers the model dynamically,
    and updates the vector table with data from Total_CO2e.
    """
    try:
        Total_CO2e = apps.get_model('yearly_steps', 'Total_CO2e')
        all_fields = Total_CO2e._meta.get_fields()

        # Specify fields to include
        INCLUDED_FIELDS = ['gas1', 'gas2', 'gas3']  # Replace with actual field names to include

        # Extract records only for the included fields (must be FloatField or IntegerField)
        included_fields = [
            field.name for field in all_fields
            if isinstance(field, (models.FloatField, models.IntegerField)) and field.name in INCLUDED_FIELDS
        ]

        # Naming
        vector_dim = len(included_fields)
        table_name = 'vector_total_co2e'
        class_name = 'VectorTotalCO2e'

        # Define the dynamic vector model
        class DynamicVectorModel(models.Model):
            co2e_vector = VectorField()
            total_co2e = models.ForeignKey(Total_CO2e, on_delete=models.CASCADE, db_column="parent_id")  # Creates a column in PostgreSQL called parent_id; accessible through total_co2e_id.

            class Meta:
                managed = True
                db_table = table_name

        # Register the model dynamically
        apps.register_model("yearly_steps", DynamicVectorModel)

        # Create the table in the database
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(DynamicVectorModel)

        # Generate the model code and append it to the models.py file
        model_code = generate_model_code(class_name, included_fields, table_name, vector_dim)
        append_model_to_file(model_code)

        # Updating the vector table with data from Total_CO2e
        total_co2e_records = Total_CO2e.objects.all()

        vector_data = []
        for record in total_co2e_records:
            vector_values = [getattr(record, field) for field in included_fields]
            vector_data.append(DynamicVectorModel(
                co2e_vector=vector_values,
                total_co2e=record  # Set ForeignKey reference
            ))

        # Bulk create records in vector table
        DynamicVectorModel.objects.bulk_create(vector_data)

        return JsonResponse({
            "status": "success",
            "message": f"Vector table '{table_name}' created with a foreign key reference, and data updated."
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })


def generate_model_code(class_name, included_fields, table_name, vector_dim):
    """
    Generates Python code for the vector table model.
    """
    model_code = f"""
class {class_name}(models.Model):
    co2e_vector = VectorField(dimensions={vector_dim})
    total_co2e = models.ForeignKey('yearly_steps.Total_CO2e', on_delete=models.CASCADE, db_column='parent_id')

    class Meta:
        managed = True
        db_table = '{table_name}'
"""
    return model_code


def append_model_to_file(model_code):
    """
    Appends the generated model code to the models.py file.
    """
    models_file = '/Users/rakesh/Desktop/CarbonSustain/ai-apps/Database_Django/database_cs/yearly_steps/models.py'
    with open(models_file, 'a') as f:
        f.write("\n" + model_code)