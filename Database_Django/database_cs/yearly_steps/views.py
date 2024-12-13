from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from yearly_steps.models import *
import json
import os
import numpy as np
from scipy.stats import zscore
from django.apps import apps
from django.db import models, connection


# @csrf_exempt
# def load_json_data(request):
#     if request.method == 'POST':
#         try:
#             # Update the path to match where your JSON file is located
#             json_path = os.path.join('/Users/rakesh/Desktop/CarbonSustain/ai-apps/decarbFrontEnd/src/assets', 'yearly_quarterly_steps.json')

#             with open(json_path, 'r') as json_file:
#                 data = json.load(json_file)
#             print("Data: ",data.type())
#             for yearly_step_data in data:
#                 year = yearly_step_data["year"]
#                 quarter = yearly_step_data["quarter"]

#                 # Iterate through all scope types
#                 for scope_type in ["scope1_steps", "scope2_steps", "scope3_steps"]:
#                     for scope_step in yearly_step_data.get(scope_type, []):
#                         description = scope_step["description"]
#                         difficulty = scope_step["difficulty"]
#                         savings = scope_step["savings"]
#                         emissions_savings = scope_step["emissions_savings"]

#                         # Save ScopeStep
#                         scope_step_obj = ScopeSteps.objects.create(
#                             year=year,
#                             quarter=quarter,
#                             scope_type=scope_type.replace("_steps", ""),  # Converts to 'scope1', 'scope2', 'scope3'
#                             description=description,
#                             difficulty=difficulty,
#                             savings=savings,
#                             emissions_savings=emissions_savings,
#                         )

#                         # Save Recommendations
#                         recommendation_data = scope_step.get("recommendation", {})
#                         rec = Recommendations.objects.create(
#                             scope_step=scope_step_obj,
#                             recommended_plan=recommendation_data.get("recommended_plan"),
#                             message=recommendation_data.get("message"),
#                             carbon_emission_savings=recommendation_data.get("carbon_emission_savings"),
#                             cost_savings=recommendation_data.get("cost_savings"),
#                         )

#                         # Save ProviderInfo
#                         for provider_info_data in recommendation_data.get("provider_info", []):
#                             ProviderInfo.objects.create(
#                                 recommendation=rec,
#                                 company=provider_info_data["company"],
#                                 renewable_percent_provided=provider_info_data.get("renewable percent provided"),
#                                 phone_number=provider_info_data.get("phone_number"),
#                                 website_link=provider_info_data.get("website_link"),
#                                 description_of_company=provider_info_data.get("description of the company"),
#                                 location=provider_info_data.get("location"),
#                                 carbon_savings=provider_info_data.get("Carbon savings"),
#                                 cost_savings=provider_info_data.get("Cost savings"),
#                                 peak_cost=provider_info_data.get("Peak Cost"),
#                                 off_peak_cost=provider_info_data.get("Off-Peak Cost"),
#                                 total_cost=provider_info_data.get("Total-Cost"),
#                             )

#         # Usage example:
#         # parse_json_and_save_from_path('/path/to/your/json/file.json')
#             return JsonResponse({'message': 'Data loaded successfully'}, status=201)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# def process_scopes_and_store_vectors_from_db():
#     try:
#         # Fetch all yearly steps
#         yearly_steps = YearlyStep.objects.all()

#         for yearly_step in yearly_steps:
#             year = yearly_step.year
#             quarter = yearly_step.quarter
            
#             # Fetch associated scope steps
#             scope_steps = ScopeStep.objects.filter(yearly_step=yearly_step)

#             for scope_step in scope_steps:
#                 scope_name = scope_step.scope_type  # 'scope1', 'scope2', or 'scope3'

#                 # Extract savings and emissions savings
#                 savings = scope_step.savings or 0.0
#                 emissions_savings = scope_step.emissions_savings or 0.0

#                 # Fetch associated recommendations
#                 recommendation = Recommendation.objects.filter(scope_step=scope_step).first()

#                 # Handle cases where no recommendation exists
#                 if recommendation:
#                     carbon_savings = recommendation.carbon_emission_savings or 0.0
#                     cost_savings = recommendation.cost_savings or 0.0
#                     peak_cost = recommendation.peak_cost or 0.0
#                     off_peak_cost = recommendation.off_peak_cost or 0.0
#                 else:
#                     # Default values when no recommendation exists
#                     carbon_savings = 0.0
#                     cost_savings = 0.0
#                     peak_cost = 0.0
#                     off_peak_cost = 0.0

#                 # Create the 6-dimensional vector
#                 vector = [savings, emissions_savings, carbon_savings, cost_savings, peak_cost, off_peak_cost]

#                 # Save the vector to the database
#                 ScopeVector.objects.create(
#                     year=year,
#                     quarter=quarter,
#                     scope_name=scope_name,
#                     vector=vector
#                 )

#         return JsonResponse({"status": "success", "message": "Data processed and stored successfully."}, status=201)

#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)}, status=400)

# @csrf_exempt  # For testing in Postman; remove in production
# def trigger_vector_processing(request):
#     if request.method == 'POST':
#         return process_scopes_and_store_vectors_from_db()
#     return JsonResponse({"status": "error", "message": "Invalid request method. Only POST is allowed."}, status=405)


# Vector table

# from django.http import JsonResponse
# from django.apps import apps
# from django.db import models, connection
# from django.views.decorators.csrf import csrf_exempt
# from pgvector.django import VectorField


# @csrf_exempt
# def create_and_update_vector_table(request):
#     """
#     Dynamically creates a vector table model for the Total_CO2e table,
#     creates the table in the database, registers the model dynamically,
#     and updates the vector table with data from Total_CO2e.
#     """
#     try:

#         Total_CO2e = apps.get_model('yearly_steps', 'Total_CO2e')
#         all_fields = Total_CO2e._meta.get_fields()

#         # FIELDS
#         EXCLUDED_FIELDS = ['id', 'comp', 'year', 'scope', 'subcategory'] # do included fields not exluded 

#         # Extracting records : float and integer 
#         included_fields = [
#             field.name for field in all_fields
#             if isinstance(field, (models.FloatField, models.IntegerField)) and field.name not in EXCLUDED_FIELDS
#         ]

#         # Naming 
#         vector_dim = len(included_fields)
#         table_name = 'vector_total_co2e' 
#         class_name = 'VectorTotalCO2e'

#         # dynamically
#         class DynamicVectorModel(models.Model):
#             co2e_vector = VectorField()
#             total_co2e = models.ForeignKey(Total_CO2e, on_delete=models.CASCADE, db_column="parent_id") # creates a column in PostgresSQl called parent_id, Through Django we can acessing through total_co2e_id name.

#             class Meta:
#                 managed = True
#                 db_table = table_name


#         apps.register_model("yearly_steps", DynamicVectorModel)


#         with connection.schema_editor() as schema_editor:
#             schema_editor.create_model(DynamicVectorModel)

#         # Generate the model code, calls generate_model_code which then uses append_model_to_file to append to model.py
#         model_code = generate_model_code(class_name, included_fields, table_name, vector_dim)
#         append_model_to_file(model_code)

#         # Updating vector table 
#         total_co2e_records = Total_CO2e.objects.all()

#         vector_data = []
#         for record in total_co2e_records:
#             vector_values = [getattr(record, field) for field in included_fields]
#             vector_data.append(DynamicVectorModel(
#                 co2e_vector=vector_values,
#                 total_co2e=record  # Set ForeignKey reference
#             ))

#         # Bulk create records in vector table
#         DynamicVectorModel.objects.bulk_create(vector_data)

#         return JsonResponse({
#             "status": "success",
#             "message": f"Vector table '{table_name}' created with a foreign key reference, and data updated."
#         })

#     except Exception as e:
#         return JsonResponse({
#             "status": "error",
#             "message": str(e)
#         })


# def generate_model_code(class_name, included_fields, table_name, vector_dim):
#     """
#     Generates Python code for the vector table model.
#     """
#     model_code = f"""
# class {class_name}(models.Model):
#     co2e_vector = VectorField(dimensions={vector_dim})
#     total_co2e = models.ForeignKey('yearly_steps.Total_CO2e', on_delete=models.CASCADE, db_column='parent_id')

#     class Meta:
#         managed = True
#         db_table = '{table_name}'
# """
#     return model_code


# def append_model_to_file(model_code):
#     """
#     Appends the generated model code to the models.py file.
#     """
#     models_file = '/Users/rakesh/Desktop/BTech_3/CarbonSustain/Yearly_quarterly_scopes/database_cs/yearly_steps/models.py'  # Update to your actual models.py file path
#     with open(models_file, 'a') as f:
#         f.write("\n" + model_code)


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


            provider_id = data.get('provider_id')
            company_id = data.get('company_id', 1)  # Default to company_id = 1 if not provided

            if not provider_id:
                return JsonResponse({"success": False, "message": "provider_id is required."}, status=400)


            provider = ProviderInfo.objects.get(id=provider_id)

            ShoppingCartContent.objects.create(
                company_id=company_id,
                provider=provider  
            )

            return JsonResponse({"success": True, "message": "Provider added to the shopping cart successfully."})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except ProviderInfo.DoesNotExist:
            return JsonResponse({"success": False, "message": "Provider not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method. Use POST."}, status=405)
