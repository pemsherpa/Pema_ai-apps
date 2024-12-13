import json
import os
from django.db import transaction
from pathlib import Path
from .models import *
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def load_json_data(request):
    if request.method == "POST":
        json_path = '/Users/rakesh/Desktop/CarbonSustain/ai-apps/decarbFrontEnd/src/assets/yearly_quarterly_steps.json'
        with open(json_path, 'r') as file:
            data = json.load(file)

        with transaction.atomic():
            company_data = data['cs_backend_data']
            company, _ = Companys.objects.get_or_create(company_id=company_data['company_id'])

            scope_total_data = company_data['scope_total']
            ScopeTotals.objects.update_or_create(
                company=company,
                defaults={
                    'scope_1_total': scope_total_data['scope_1_total'],
                    'scope_2_total': scope_total_data['scope_2_total'],
                    'scope_3_total': scope_total_data['scope_3_total'],
                    'scope_total': scope_total_data['scope_total'],
                    'scope_1_target': scope_total_data['scope_1_target'],
                    'scope_2_target': scope_total_data['scope_2_target'],
                    'scope_3_target': scope_total_data['scope_3_target'],
                    'target_timeframe': scope_total_data['target_timeframe']
                }
            )

            for yearly_data in data['yearly_steps']:
                year = yearly_data['year']
                quarter = yearly_data['quarter']

                for scope_type, steps in [('scope1_steps', 1), ('scope2_steps', 2), ('scope3_steps', 3)]:
                    print(scope_type, steps)

                    for step in yearly_data[scope_type]:
                        scope_step = ScopeSteps.objects.create(
                            company=company,
                            year=year,
                            quarter=quarter,
                            scope_type=steps,  
                            description=step['description'],
                            difficulty=step['difficulty'],
                            cost_savings=step['cost_savings'],
                            emissions_savings=step['co2_savings'],
                            total_cost=step['total_cost'],
                            total_emissions=step['total_emissions'],
                            transition_percentage=step['transition_percentage']
                        )
                        
                        if 'recommendation' in step and steps != 3:  # Recommendations for Scope 1 and 2 only
                            recommendation_data = step['recommendation']

                            # Ensure recommendation data is valid
                            if 'provider_info' not in recommendation_data:
                                return JsonResponse({"error": "Provider info missing in recommendation."}, status=400)

                            providers = []
                            for provider_data in recommendation_data['provider_info']:
                                provider = ProviderInfo.objects.create(
                                    company=provider_data.get('company', ''),
                                    plan_name=provider_data.get('plan_name', ''),
                                    renewable_percent_provided=provider_data.get('renewable percent provided', 0),
                                    phone_number=provider_data.get('phone_number', ''),
                                    website_link=provider_data.get('website_link', ''),
                                    description_of_company=provider_data.get('description of the company', ''),
                                    location=provider_data.get('location', ''),
                                    carbon_savings=provider_data.get('Carbon savings', 0.0),
                                    cost_savings=provider_data.get('Cost savings', 0.0),
                                    peak_cost=provider_data.get('Peak Cost', 0.0),
                                    off_peak_cost=provider_data.get('Off-Peak Cost', 0.0),
                                    total_cost=provider_data.get('Total-Cost_with_peak_and_off-peak', 0.0)
                                )
                                providers.append(provider)

                            # Create the recommendation entry and add all providers
                            recommendation = Recommendations.objects.create(
                                scope_step=scope_step,
                                recommended_plan=recommendation_data.get('recommended_plan', ''),
                                message=recommendation_data.get('message', '')
                            )
                            recommendation.providers.set(providers)  # Link all providers
        return JsonResponse({"message": "Data successfully loaded"}, status=200)


# @csrf_exempt
# def load_json_data(request):
#     if request.method=="POST":
#         """
#         Load data from a JSON file and populate the database models.

#         :param json_path: Path to the JSON file.
#         """
#         json_path = os.path.join('/Users/rakesh/Desktop/CarbonSustain/ai-apps/decarbFrontEnd/src/assets', 'yearly_quarterly_steps.json')
#         with open(json_path, 'r') as file:
#             data = json.load(file)

#         # Extract company and scope total data
#         company_id = data['cs_backend_data']['company_id']

#         with transaction.atomic():
#             # Create or get the company
#             company, created = Companys.objects.get_or_create(company_id=company_id)

#             # Create or update ScopeTotals
#             scope_total_data = data['cs_backend_data']['scope_total']
#             ScopeTotals.objects.update_or_create(
#                 company=company,
#                 defaults={
#                     'scope_1_total': scope_total_data['scope_1_total'],
#                     'scope_2_total': scope_total_data['scope_2_total'],
#                     'scope_3_total': scope_total_data['scope_3_total'],
#                     'scope_total': scope_total_data['scope_total'],
#                     'scope_1_target': scope_total_data['scope_1_target'],
#                     'scope_2_target': scope_total_data['scope_2_target'],
#                     'scope_3_target': scope_total_data['scope_3_target'],
#                     'target_timeframe': scope_total_data['target_timeframe'],
#                 }
#             )

#             # Process yearly steps
#             yearly_steps = data['yearly_steps']
#             for step in yearly_steps:
#                 year = step['year']
#                 quarter = step['quarter']

#                 for scope_type, scope_steps in step.items():
#                     if scope_type.startswith('scope') and isinstance(scope_steps, list):
#                         for step_data in scope_steps:
#                             scope_step = ScopeSteps.objects.create(
#                                 company=company,
#                                 year=year,
#                                 quarter=quarter,
#                                 scope_type=int(''.join(filter(str.isdigit, scope_type))),
#                                 description=step_data['description'],
#                                 difficulty=step_data['difficulty'],
#                                 savings=step_data['savings'],
#                                 emissions_savings=step_data['emissions_savings'],
#                             )

#                             # Create Recommendations
#                             if 'recommendation' in step_data:
#                                 recommendation_data = step_data['recommendation']
#                                 recommendation = Recommendations.objects.create(
#                                     scope_step=scope_step,
#                                     recommended_plan=recommendation_data.get('recommended_plan'),
#                                     message=recommendation_data.get('message'),
#                                     #carbon_emission_savings=recommendation_data.get('carbon_emission_savings'),
#                                     #cost_savings=recommendation_data.get('cost_savings'),
#                                 )

#                                 # Add ProviderInfo
#                                 provider_infos = recommendation_data.get('provider_info', [])
#                                 for provider_data in provider_infos:
#                                     ProviderInfo.objects.create(
#                                         recommendation=recommendation,
#                                         company=provider_data.get('company', ''),
#                                         renewable_percent_provided=provider_data.get('renewable percent provided'),
#                                         phone_number=provider_data.get('phone_number', ''),
#                                         website_link=provider_data.get('website_link', ''),
#                                         description_of_company=provider_data.get('description of the company', ''),
#                                         location=provider_data.get('location', ''),
#                                         carbon_savings=provider_data.get('Carbon savings'),
#                                         cost_savings=provider_data.get('Cost savings'),
#                                         peak_cost=provider_data.get('Peak Cost'),
#                                         off_peak_cost=provider_data.get('Off-Peak Cost'),
#                                         total_cost=provider_data.get('Total-Cost', 0),
#                                     )
#         return JsonResponse({'message': 'Data loaded successfully'}, status=201)
#     else:
#         return JsonResponse({'message STATE': 'Wrong State, Use POST'}, status=201)
    



    # /Users/rakesh/Desktop/CarbonSustain/ai-apps/decarbFrontEnd/src/assets', 'yearly_quarterly_steps.json