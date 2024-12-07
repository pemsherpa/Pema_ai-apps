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

        # FIELDS
        EXCLUDED_FIELDS = ['id', 'comp', 'year', 'scope', 'subcategory'] # do included fields not exluded 

        # Extracting records : float and integer 
        included_fields = [
            field.name for field in all_fields
            if isinstance(field, (models.FloatField, models.IntegerField)) and field.name not in EXCLUDED_FIELDS
        ]

        # Naming 
        vector_dim = len(included_fields)
        table_name = 'vector_total_co2e' 
        class_name = 'VectorTotalCO2e'

        # dynamically
        class DynamicVectorModel(models.Model):
            co2e_vector = VectorField()
            total_co2e = models.ForeignKey(Total_CO2e, on_delete=models.CASCADE, db_column="parent_id") # creates a column in PostgresSQl called parent_id, Through Django we can acessing through total_co2e_id name.

            class Meta:
                managed = True
                db_table = table_name


        apps.register_model("yearly_steps", DynamicVectorModel)


        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(DynamicVectorModel)

        # Generate the model code, calls generate_model_code which then uses append_model_to_file to append to model.py
        model_code = generate_model_code(class_name, included_fields, table_name, vector_dim)
        append_model_to_file(model_code)

        # Updating vector table 
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
    models_file = '/Users/rakesh/Desktop/CarbonSustain/ai-apps/Database_Django/database_cs/yearly_steps/models.py'  # Update to your actual models.py file path
    with open(models_file, 'a') as f:
        f.write("\n" + model_code)