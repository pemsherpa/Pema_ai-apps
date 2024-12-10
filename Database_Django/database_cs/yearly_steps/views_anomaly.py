from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from yearly_steps.models import *
import json
import os
import numpy as np
from scipy.stats import zscore
from django.apps import apps
from django.db import models, connection
from scipy.spatial.distance import cosine


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

        # Read the models
        Total_CO2e = apps.get_model('yearly_steps', 'Total_CO2e')
        Total_CO2eVector = apps.get_model('yearly_steps', 'VectorTotalCO2e')

        # Query the parent data
        query = Total_CO2e.objects.filter(
            comp__in=companies,
            year__in=years,
            scope__in=scopes,
            subcategory__in=subcategories
        )
        parent_records = query.values('id', 'comp', 'year', 'scope', 'subcategory')

        # If no records are found, return an error
        if not parent_records.exists():
            return JsonResponse({"status": "error", "message": "No records found for the given filters."})

        # Map parent data to metadata
        parent_metadata = {}
        for record in parent_records:
            parent_metadata[record['id']] = {
                "comp": record['comp'],
                "year": record['year'],
                "scope": record['scope'],
                "subcategory": record['subcategory']
            }
        parent_ids = list(parent_metadata.keys())

        # Query the vector data for anomalies
        vector_query = Total_CO2eVector.objects.filter(total_co2e_id__in=parent_ids)
        vector_data = vector_query.values_list('total_co2e_id', 'co2e_vector')

        # If no vectors are found, return an error
        if not vector_data:
            return JsonResponse({"status": "error", "message": "No vectors found for the given records."})

        # Map vectors to their IDs
        parent_to_vector_map = {}
        for total_co2e_id, co2e_vector in vector_data:
            parent_to_vector_map[total_co2e_id] = np.array(co2e_vector, dtype=float)

        # IQR anomaly detection
        vector_values = np.array(list(parent_to_vector_map.values()), dtype=float)
        q1 = np.percentile(vector_values, 25, axis=0)
        q3 = np.percentile(vector_values, 75, axis=0)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Detect IQR anomalies
        iqr_anomalies = []
        for parent_id, vector in parent_to_vector_map.items():
            for idx, value in enumerate(vector):
                is_anomalous = value < lower_bound[idx] or value > upper_bound[idx]
                if is_anomalous:
                    anomaly = {
                        "parent_id": parent_id,
                        "comp": parent_metadata[parent_id]["comp"],
                        "year": parent_metadata[parent_id]["year"],
                        "scope": parent_metadata[parent_id]["scope"],
                        "subcategory": parent_metadata[parent_id]["subcategory"],
                        "anomalous_value": value,
                        "vector_value": vector.tolist()
                    }
                    iqr_anomalies.append(anomaly)

        # Cosine similarity anomaly detection
        # Calculate mean vector
        mean_vector = np.mean(vector_values, axis=0)

        # Calculate cosine similarity and detect anomalies
        cosine_anomalies = []
        for parent_id, vector in parent_to_vector_map.items():
            # Cosine similarity
            print(vector)
            similarity = 1 - cosine(vector, mean_vector) if np.linalg.norm(vector) and np.linalg.norm(mean_vector) else 0
            # Flag as anomaly if similarity is too far from the expected range
            if similarity < 0.95:  # Threshold set for detecting deviations
                anomaly = {
                    "parent_id": parent_id,
                    "comp": parent_metadata[parent_id]["comp"],
                    "year": parent_metadata[parent_id]["year"],
                    "scope": parent_metadata[parent_id]["scope"],
                    "subcategory": parent_metadata[parent_id]["subcategory"],
                    "cosine_similarity": similarity,
                    "vector_value": vector.tolist()
                }
                cosine_anomalies.append(anomaly)

        # Return JSON response
        return JsonResponse({
            "status": "success",
            "iqr_anomalies": iqr_anomalies,
            "cosine_anomalies": cosine_anomalies
        })

    except Exception as e:
        # Handle unexpected errors and return as JSON
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })
