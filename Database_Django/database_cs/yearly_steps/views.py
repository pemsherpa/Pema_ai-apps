from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from yearly_steps.models import *
import json
import os
import numpy as np
from scipy.stats import zscore
from django.apps import apps
from django.db import models, connection


@csrf_exempt
def load_json_data(request):
    if request.method == 'POST':
        try:
            # Update the path to match where your JSON file is located
            json_file_path = os.path.join('/Users/rakesh/Desktop/BTech_3/CarbonSustain/CarbonSustainScopes', 'yearly_quarterly_steps.json')

            # Load JSON data from the file
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            # Parse the company and scope_total
            cs_backend_data = data['cs_backend_data']
            company = Company.objects.create(company_id=cs_backend_data['company_id'])

            scope_total = cs_backend_data['scope_total']
            ScopeTotal.objects.create(
                company=company,
                scope_1_total=scope_total['scope_1_total'],
                scope_2_total=scope_total['scope_2_total'],
                scope_3_total=scope_total['scope_3_total'],
                scope_total=scope_total['scope_total'],
                scope_1_target=scope_total['scope_1_target'],
                scope_2_target=scope_total['scope_2_target'],
                scope_3_target=scope_total['scope_3_target'],
                target_timeframe=scope_total['target_timeframe']
            )

            # Parse yearly_steps
            for yearly_step in data['yearly_steps']:
                year_step = YearlyStep.objects.create(
                    year=yearly_step['year'],
                    quarter=yearly_step['quarter'],
                    company=company
                )

                # Parse scope1_steps, scope2_steps, etc.
                for scope_type in ['scope1_steps', 'scope2_steps', 'scope3_steps']:
                    for step in yearly_step[scope_type]:
                        scope_step = ScopeStep.objects.create(
                            yearly_step=year_step,
                            scope_type=scope_type,
                            description=step['description'],
                            difficulty=step['difficulty'],
                            savings=step['savings'],
                            emissions_savings=step['emissions_savings']
                        )

                        # Parse recommendations
                        if 'recommendation' in step:
                            rec = step['recommendation']

                            # Check if 'provider_info' exists and is a list
                            if 'provider_info' in rec and isinstance(rec['provider_info'], list):
                                for provider in rec['provider_info']:  # Loop through all providers in provider_info
                                    Recommendation.objects.create(
                                        scope_step=scope_step,
                                        recommended_plan=rec.get('recommended_plan', ''),
                                        message=rec.get('message', ''),
                                        carbon_emission_savings=float(provider.get('Carbon savings', 0)),
                                        cost_savings=float(provider.get('Cost savings', 0)),
                                        peak_cost=float(provider.get('Peak Cost', 0)),
                                        off_peak_cost=float(provider.get('Off-Peak Cost', 0))
                                    )

            return JsonResponse({'message': 'Data loaded successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def process_scopes_and_store_vectors_from_db():
    try:
        # Fetch all yearly steps
        yearly_steps = YearlyStep.objects.all()

        for yearly_step in yearly_steps:
            year = yearly_step.year
            quarter = yearly_step.quarter
            
            # Fetch associated scope steps
            scope_steps = ScopeStep.objects.filter(yearly_step=yearly_step)

            for scope_step in scope_steps:
                scope_name = scope_step.scope_type  # 'scope1', 'scope2', or 'scope3'

                # Extract savings and emissions savings
                savings = scope_step.savings or 0.0
                emissions_savings = scope_step.emissions_savings or 0.0

                # Fetch associated recommendations
                recommendation = Recommendation.objects.filter(scope_step=scope_step).first()

                # Handle cases where no recommendation exists
                if recommendation:
                    carbon_savings = recommendation.carbon_emission_savings or 0.0
                    cost_savings = recommendation.cost_savings or 0.0
                    peak_cost = recommendation.peak_cost or 0.0
                    off_peak_cost = recommendation.off_peak_cost or 0.0
                else:
                    # Default values when no recommendation exists
                    carbon_savings = 0.0
                    cost_savings = 0.0
                    peak_cost = 0.0
                    off_peak_cost = 0.0

                # Create the 6-dimensional vector
                vector = [savings, emissions_savings, carbon_savings, cost_savings, peak_cost, off_peak_cost]

                # Save the vector to the database
                ScopeVector.objects.create(
                    year=year,
                    quarter=quarter,
                    scope_name=scope_name,
                    vector=vector
                )

        return JsonResponse({"status": "success", "message": "Data processed and stored successfully."}, status=201)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt  # For testing in Postman; remove in production
def trigger_vector_processing(request):
    if request.method == 'POST':
        return process_scopes_and_store_vectors_from_db()
    return JsonResponse({"status": "error", "message": "Invalid request method. Only POST is allowed."}, status=405)


#Vector table

from django.http import JsonResponse
from django.apps import apps
from django.db import models, connection
from django.views.decorators.csrf import csrf_exempt
from pgvector.django import VectorField


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

        
        vector_dim = len(included_fields)
        table_name = 'total_co2e_vector'
        class_name = 'Total_CO2eVector'

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
    models_file = '/Users/rakesh/Desktop/BTech_3/CarbonSustain/Yearly_quarterly_scopes/database_cs/yearly_steps/models.py'  # Update to your actual models.py file path
    with open(models_file, 'a') as f:
        f.write("\n" + model_code)

# OUTLIERS

@csrf_exempt
def detect_anomalies(request):
    try:
        # Default values if inputs are not provided
        default_companies = [1, 2, 3]  
        default_years = [2020, 2021, 2022, 2023, 2024]  
        default_scopes = [1, 2, 3]  
        default_subcategories = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  
        
        def parse_input(input_str, default_values):
            if input_str:
                return [int(value.strip()) for value in input_str.split(',')]
            return default_values

        
        companies = parse_input(request.GET.get("comp"), default_companies)
        years = parse_input(request.GET.get("year"), default_years)
        scopes = parse_input(request.GET.get("scope"), default_scopes)
        subcategories = parse_input(request.GET.get("subcategory"), default_subcategories)

        # read the models 
        Total_CO2e = apps.get_model('yearly_steps', 'Total_CO2e')
        Total_CO2eVector = apps.get_model('yearly_steps', 'Total_CO2eVector')

        
        query = Total_CO2e.objects.filter(
            comp__in=companies,
            year__in=years,
            scope__in=scopes,
            subcategory__in=subcategories
        )
        parent_records = query.values('id', 'comp', 'year', 'scope', 'subcategory') # relavent records

        # If no records are found, return an error
        if not parent_records.exists():
            return JsonResponse({"status": "error", "message": "No records found for the given filters."})

        # Build a mapping of parent IDs to their metadata
        parent_metadata = {}
        for record in parent_records:
            parent_metadata[record['id']] = {
                "comp": record['comp'],
                "year": record['year'],
                "scope": record['scope'],
                "subcategory": record['subcategory']
            }
        print("\nparent_metadata",parent_metadata)
        parent_ids = list(parent_metadata.keys())

        # Query the Total_CO2eVector table for vectors corresponding to parent_ids
        vector_query = Total_CO2eVector.objects.filter(total_co2e_id__in=parent_ids)
        vector_data = vector_query.values_list('total_co2e_id', 'co2e_vector')
        print("Vector_data",vector_data)

        # If no vectors are found, return an error
        if not vector_data:
            return JsonResponse({"status": "error", "message": "No vectors found for the given records."})

        # Extract vectors and prepare for anomaly detection
        parent_to_vector_map = {} 
        for total_co2e_id, co2e_vector in vector_data:
            parent_to_vector_map[total_co2e_id] = co2e_vector
        print("Parent_to_vector_map :",parent_to_vector_map)
        # Convert vectors to numpy array
        vector_values = np.array(list(parent_to_vector_map.values()), dtype=float)

        # IQR
        q1 = np.percentile(vector_values, 25, axis=0)
        q3 = np.percentile(vector_values, 75, axis=0)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        print("Upper Bound:", upper_bound)
        print("Lower Bound:", lower_bound)

        # Detect anomalies
        anomalies = []
        for parent_id, vector in parent_to_vector_map.items():
            for idx, value in enumerate(vector):
                value = float(value)  # Convert value to Python float
                is_anomalous = value < lower_bound[idx] or value > upper_bound[idx]
                if is_anomalous:
                    anomaly = {
                        "parent_id": parent_id,
                        "comp": parent_metadata[parent_id]["comp"],
                        "year": parent_metadata[parent_id]["year"],
                        "scope": parent_metadata[parent_id]["scope"],
                        "subcategory": parent_metadata[parent_id]["subcategory"],
                        "anomalous_value": value
                    }
                    anomalies.append(anomaly)

        # Return the anomalies as JSON
        return JsonResponse({
            "status": "success",
            "anomalies": anomalies
        })

    except Exception as e:
        # Handle unexpected errors and return as JSON
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })


# CART
@csrf_exempt
def add_shopping_cart(request):
    if request.method == 'POST':
        try:
            print("Add to shopping cart")
            # Parse JSON data
            data = json.loads(request.body)
            
            # Extract fields from JSON
            company_id = data.get('company_id')
            name=data.get('name')
            costSavings = data.get('costSavings')
            co2savings = data.get('co2savings')
            transition = data.get('transition')
            
            # Validate required fields
            if not all([company_id, transition]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            # Create and save the record
            record = ShoppingCartContent(
                company_id=company_id,
                name=name,
                costSavings=costSavings,
                co2savings=co2savings,
                transition=transition,
                )
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