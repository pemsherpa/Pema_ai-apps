# Anomaly
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
def detect_anomalies(request):
    try:
        # Default values if inputs are not provided
        default_companies = [1, 2, 3, 4, 5]  
        default_years = [2020, 2021, 2022, 2023]  
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
        Total_CO2eVector = apps.get_model('yearly_steps', 'VectorTotalCO2e')

        
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