import json
import os
from django.db import transaction
from pathlib import Path
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@transaction.atomic
def load_json_data(data, output_data):
    data = {"yearly_steps": data}  # Wrap data if needed

    company_id = output_data.get('company_id')
    print(company_id)
    if not company_id:
        print("\n Company_id missing...............")
        return JsonResponse({"error": "Company ID missing in data."}, status=400)

    company, _ = Companys.objects.get_or_create(company_id=company_id)

    # Save ScopeTotals
    scope_total_data = output_data.get('scope_total', {})
    ScopeTotals.objects.update_or_create(
        company=company,
        defaults={
            'scope_1_total': scope_total_data.get('scope_1_total', 0),
            'scope_2_total': scope_total_data.get('scope_2_total', 0),
            'scope_3_total': scope_total_data.get('scope_3_total', 0),
            'scope_total': scope_total_data.get('scope_total', 0),
            'scope_1_target': scope_total_data.get('scope_1_target', 0),
            'scope_2_target': scope_total_data.get('scope_2_target', 0),
            'scope_3_target': scope_total_data.get('scope_3_target', 0),
            'target_timeframe': scope_total_data.get('target_timeframe', 0),
        },
    )

    # Save ScopeSteps and related data
    for yearly_data in data.get('yearly_steps', []):
        print("YEARLY_DATA list", yearly_data)
        year = yearly_data.get('year')
        quarter = yearly_data.get('quarter')

        for scope_type, scope_id in [('scope1_steps', 1), ('scope2_steps', 2), ('scope3_steps', 3)]:
            if scope_id != 3:  # Scope-specific filtering
                print("\nScope: ", scope_id)
                for step_data in yearly_data.get(scope_type, []):
                    recommendation = step_data.get('recommendation', {})
                    our_recommendation = recommendation.get('our recommendation', {})
                    provider_info_list = recommendation.get('provider_info', [])
                    plan = None
                    print("\nStep Data:", step_data)

                    # Look for plans via 'our_recommendation' first
                    company_name = our_recommendation.get('company', '')
                    plan_name = our_recommendation.get('plan_name', 'Default Plan')
                    provider = Providers.objects.filter(providers_name=company_name).first()

                    if provider:
                        plan = Plans.objects.filter(plan_name=plan_name, provider=provider).first()

                    # Fallback to 'provider_info_list'
                    if not plan:
                        for provider_info in provider_info_list:
                            provider, _ = Providers.objects.get_or_create(
                                providers_name=provider_info.get('company', 'Unknown'),
                                defaults={
                                    'phone_number': provider_info.get('phone_number', ''),
                                    'website_link': provider_info.get('website_link', ''),
                                    'description': provider_info.get('description of the company', ''),
                                },
                            )

                            plan, _ = Plans.objects.get_or_create(
                                provider=provider,
                                plan_name=provider_info.get('plan_name', 'Default Plan'),
                                defaults={
                                    'carbon_cost': provider_info.get('Carbon savings', 0),
                                    'total_cost': provider_info.get('Total-Cost_with_peak_and_off-peak', 0),
                                    'peak_cost': provider_info.get('Peak Cost', 0),
                                    'off_peak_cost': provider_info.get('Off-Peak Cost', 0),
                                },
                            )

                    if plan and isinstance(plan, Plans):
                        print("\nEntering ScopeSteps, Plan present............")
                        ScopeSteps.objects.create(
                            company=company,
                            plan=plan,
                            year=year,
                            quarter=quarter,
                            scope_type=scope_id,
                            description=step_data.get('description', ''),
                            difficulty=step_data.get('difficulty', 0),
                            transition_percentage=step_data.get('transition_percentage', 0),
                        )
                    else:
                        return JsonResponse({"error": f"Invalid plan assigned for year {year}, quarter {quarter}."}, status=400)

    return JsonResponse({"success": "Data successfully added."}, status=200)


# @csrf_exempt
# def load_json_data(data,output_data):
#     # Loop through the list of dictionaries (since data is a list of dictionaries)
#     data = {"yearly_steps": data}
#     print (data)
#     company_id = data.get('company_id')  # Modify this line if needed
#     if not company_id:
#         print("\n Company_id missing...............")
#         return JsonResponse({"error": "Company ID missing in data."}, status=400)

#     company, _ = Companys.objects.get_or_create(company_id=company_id)

#         # Save ScopeTotals
#     scope_total_data = output_data.get('scope_total', {})
#     ScopeTotals.objects.update_or_create(
#             company=company,
#             defaults={
#                 'scope_1_total': scope_total_data.get('scope_1_total', 0),
#                 'scope_2_total': scope_total_data.get('scope_2_total', 0),
#                 'scope_3_total': scope_total_data.get('scope_3_total', 0),
#                 'scope_total': scope_total_data.get('scope_total', 0),
#                 'scope_1_target': scope_total_data.get('scope_1_target', 0),
#                 'scope_2_target': scope_total_data.get('scope_2_target', 0),
#                 'scope_3_target': scope_total_data.get('scope_3_target', 0),
#                 'target_timeframe': scope_total_data.get('target_timeframe', 0),
#             },
#         )

#         # Save ScopeSteps and related data
#     for yearly_data in data.get('yearly_steps', []):
#             print("YEARLY_DATA list",yearly_data)
#             year = yearly_data.get('year')
#             quarter = yearly_data.get('quarter')

#     for scope_type, scope_id in [('scope1_steps', 1), ('scope2_steps', 2), ('scope3_steps', 3)]:
#             if scope_id != 3:
#                     print("\nScope: ", scope_id)
#                     for step_data in yearly_data.get(scope_type, []):
#                         recommendation = step_data.get('recommendation', {})
#                         our_recommendation = recommendation.get('our recommendation', {})
#                         provider_info_list = recommendation.get('provider_info', [])
#                         plan = None
#                         print("\n Step Data:",step_data)
#                         # Check 'our_recommendation' first
#                         #if our_recommendation:


#                         # Fallback to 'provider_info_list' if no plan found from 'our_recommendation'
#                         #if not plan:
#                             #print("\nFallback......")
#                         for provider_info in provider_info_list:
#                             # Create Providers first
#                             provider, _ = Providers.objects.get_or_create(
#                                 providers_name=provider_info.get('company', 'Unknown'),
#                                 defaults={
#                                     'phone_number': provider_info.get('phone_number', ''),
#                                     'website_link': provider_info.get('website_link', ''),
#                                     'description': provider_info.get('description of the company', ''),
#                                 }
#                             )

#                             # Create Plans after Providers
#                             plan, _ = Plans.objects.get_or_create(
#                                 provider=provider,
#                                 plan_name=provider_info.get('plan_name', 'Default Plan'),
#                                 defaults={
#                                     'carbon_cost': provider_info.get('Carbon savings', 0),
#                                     'total_cost': provider_info.get('Total-Cost_with_peak_and_off-peak', 0),
#                                     'peak_cost': provider_info.get('Peak Cost', 0),
#                                     'off_peak_cost': provider_info.get('Off-Peak Cost', 0),
#                                 }
#                             )

#                             print("\nOur Recommendations: ")
#                             company_name = our_recommendation.get('company', '')
#                             plan_name = our_recommendation.get('plan_name', 'Default Plan')
#                             print("company: ",company_name)
#                             print("plan_name: ", plan_name)
#                             provider = Providers.objects.filter(providers_name=company_name).first()
#                             print("\nProvider: ",provider)
#                             if provider:
#                                 plan = Plans.objects.filter(plan_name=plan_name, provider=provider).first()
#                             print("\nPlan: ", plan)

#                         if plan and isinstance(plan, Plans):
#                             print("\n Entering ScopeSteps, Plan present............")
#                             # Save ScopeSteps after Providers and Plans
#                             ScopeSteps.objects.create(
#                                 company=company,
#                                 plan=plan,
#                                 year=year,
#                                 quarter=quarter,
#                                 scope_type=scope_id,
#                                 description=step_data.get('description', ''),
#                                 difficulty=step_data.get('difficulty', 0),
#                                 transition_percentage=step_data.get('transition_percentage', 0),
#                             )
#                         else:
#                             return JsonResponse({"error": "Invalid plan assigned."}, status=400)

#     return JsonResponse({"success": "Data successfully added."}, status=200)





# @csrf_exempt
# def load_json_data(output_data, yearly_steps):
#     if yearly_steps and output_data:
#         with transaction.atomic():
#             # Extract and save company data
#             company_id = output_data.get('company_id')
#             scope_total = output_data.get('scope_total', {})
#             if not company_id:
#                 return JsonResponse({"error": "Company ID missing in data."}, status=400)

#             company, _ = Companys.objects.get_or_create(company_id=company_id)

#             ScopeTotals.objects.update_or_create(
#                 company=company,
#                 defaults={
#                     'scope_1_total': scope_total.get('scope_1_total', 0),
#                     'scope_2_total': scope_total.get('scope_2_total', 0),
#                     'scope_3_total': scope_total.get('scope_3_total', 0),
#                     'scope_total': scope_total.get('scope_total', 0),
#                     'scope_1_target': scope_total.get('scope_1_target', 0),
#                     'scope_2_target': scope_total.get('scope_2_target', 0),
#                     'scope_3_target': scope_total.get('scope_3_target', 0),
#                     'target_timeframe': scope_total.get('target_timeframe', 0),
#                 },
#             )
#             print("CARBON")
#             # Save ScopeSteps and related data
#             for yearly_data in yearly_steps:
#                 print(yearly_data)
#                 # If yearly_data is a dictionary
#                 if isinstance(yearly_data, dict):
#                     year = yearly_data.get('year')
#                     quarter = yearly_data.get('quarter')
#                     print("Statement 1:", year, quarter)
#                 else:
#                     # Access attributes directly for objects
#                     year = getattr(yearly_data, 'year', None)
#                     quarter = getattr(yearly_data, 'quarter', None)
#                     print("Statement 2:", year, quarter)

#                 for scope_type, scope_id in [('scope1_steps', 1), ('scope2_steps', 2), ('scope3_steps', 3)]:
#                     if scope_id != 3:
#                         steps = (
#                             yearly_data.get(scope_type, [])
#                             if isinstance(yearly_data, dict)
#                             else getattr(yearly_data, scope_type, [])
#                         )
#                         print("Statement 3:", steps)
#                         for step_data in steps:
#                             # Handle both dictionaries and objects
#                             if isinstance(step_data, dict):
#                                 recommendation = step_data.get('recommendation', {})
#                                 description = step_data.get('description', '')
#                                 difficulty = step_data.get('difficulty', 0)
#                                 transition_percentage = step_data.get('transition_percentage', 0)
#                             else:
#                                 recommendation = getattr(step_data, 'recommendation', {})
#                                 description = getattr(step_data, 'description', '')
#                                 difficulty = getattr(step_data, 'difficulty', 0)
#                                 transition_percentage = getattr(step_data, 'transition_percentage', 0)

#                             provider_info_list = recommendation.get('provider_info', [])
#                             plan = None

#                             for provider_info in provider_info_list:
#                                 provider, _ = Providers.objects.get_or_create(
#                                     providers_name=provider_info.get('company', 'Unknown'),
#                                     defaults={
#                                         'phone_number': provider_info.get('phone_number', ''),
#                                         'website_link': provider_info.get('website_link', ''),
#                                         'description': provider_info.get('description of the company', ''),
#                                     },
#                                 )
#                                 print("Statement 4:", provider)
#                                 plan, _ = Plans.objects.get_or_create(
#                                     provider=provider,
#                                     plan_name=provider_info.get('plan_name', 'Default Plan'),
#                                     defaults={
#                                         'carbon_cost': provider_info.get('Carbon savings', 0),
#                                         'total_cost': provider_info.get('Total-Cost_with_peak_and_off-peak', 0),
#                                         'peak_cost': provider_info.get('Peak Cost', 0),
#                                         'off_peak_cost': provider_info.get('Off-Peak Cost', 0),
#                                     },
#                                 )

#                             if plan and isinstance(plan, Plans):
#                                 ScopeSteps.objects.create(
#                                     company=company,
#                                     plan=plan,
#                                     year=year,
#                                     quarter=quarter,
#                                     scope_type=scope_id,
#                                     description=description,
#                                     difficulty=difficulty,
#                                     transition_percentage=transition_percentage,
#                                 )
#                                 print("Statement 4:",plan)
#                             else:
#                                 return JsonResponse({"error": "Invalid plan assigned."}, status=400)

#         return JsonResponse({"success": "Data successfully added."}, status=200)





    
        


# @csrf_exempt
# def load_json_data(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

#     try:
#         json_path = '../../decarbFrontEnd/src/assets/yearly_quarterly_steps.json'

#         with open(json_path, 'r') as file:
#             data = json.load(file)

#         with transaction.atomic():
#             # Extract and save company data
#             company_data = data.get('cs_backend_data', {})
#             company_id = company_data.get('company_id')
#             if not company_id:
#                 return JsonResponse({"error": "Company ID missing in data."}, status=400)

#             company, _ = Companys.objects.get_or_create(company_id=company_id)

#             # Save ScopeTotals
#             scope_total_data = company_data.get('scope_total', {})
#             ScopeTotals.objects.update_or_create(
#                 company=company,
#                 defaults={
#                     'scope_1_total': scope_total_data.get('scope_1_total', 0),
#                     'scope_2_total': scope_total_data.get('scope_2_total', 0),
#                     'scope_3_total': scope_total_data.get('scope_3_total', 0),
#                     'scope_total': scope_total_data.get('scope_total', 0),
#                     'scope_1_target': scope_total_data.get('scope_1_target', 0),
#                     'scope_2_target': scope_total_data.get('scope_2_target', 0),
#                     'scope_3_target': scope_total_data.get('scope_3_target', 0),
#                     'target_timeframe': scope_total_data.get('target_timeframe', 0),
#                 },
#             )

#             # Save ScopeSteps and related data
#             for yearly_data in data.get('yearly_steps', []):
#                 year = yearly_data.get('year')
#                 quarter = yearly_data.get('quarter')

#                 for scope_type, scope_id in [('scope1_steps', 1), ('scope2_steps', 2), ('scope3_steps', 3)]:
                    
#                     if scope_id != 3:
#                         print("\nScope: ", scope_id)
#                         for step_data in yearly_data.get(scope_type, []):
#                             recommendation = step_data.get('recommendation', {})
#                             our_recommendation = recommendation.get('our recommendation', {})
#                             provider_info_list = recommendation.get('provider_info', [])
#                             plan = None

#                             # Check 'our_recommendation' first
#                             #if our_recommendation:


#                             # Fallback to 'provider_info_list' if no plan found from 'our_recommendation'
#                             #if not plan:
#                                 #print("\nFallback......")
#                             for provider_info in provider_info_list:
#                                 # Create Providers first
#                                 provider, _ = Providers.objects.get_or_create(
#                                     providers_name=provider_info.get('company', 'Unknown'),
#                                     defaults={
#                                         'phone_number': provider_info.get('phone_number', ''),
#                                         'website_link': provider_info.get('website_link', ''),
#                                         'description': provider_info.get('description of the company', ''),
#                                     }
#                                 )

#                                 # Create Plans after Providers
#                                 plan, _ = Plans.objects.get_or_create(
#                                     provider=provider,
#                                     plan_name=provider_info.get('plan_name', 'Default Plan'),
#                                     defaults={
#                                         'carbon_cost': provider_info.get('Carbon savings', 0),
#                                         'total_cost': provider_info.get('Total-Cost_with_peak_and_off-peak', 0),
#                                         'peak_cost': provider_info.get('Peak Cost', 0),
#                                         'off_peak_cost': provider_info.get('Off-Peak Cost', 0),
#                                     }
#                                 )

#                                 print("\nOur Recommendations: ")
#                                 company_name = our_recommendation.get('company', '')
#                                 plan_name = our_recommendation.get('plan_name', 'Default Plan')
#                                 print("company: ",company_name)
#                                 print("plan_name: ", plan_name)
#                                 provider = Providers.objects.filter(providers_name=company_name).first()
#                                 print("\nProvider: ",provider)
#                                 if provider:
#                                     plan = Plans.objects.filter(plan_name=plan_name, provider=provider).first()
#                                 print("\nPlan: ", plan)

#                             if plan and isinstance(plan, Plans):
#                                 # Save ScopeSteps after Providers and Plans
#                                 ScopeSteps.objects.create(
#                                     company=company,
#                                     plan=plan,
#                                     year=year,
#                                     quarter=quarter,
#                                     scope_type=scope_id,
#                                     description=step_data.get('description', ''),
#                                     difficulty=step_data.get('difficulty', 0),
#                                     transition_percentage=step_data.get('transition_percentage', 0),
#                                 )
#                             else:
#                                 return JsonResponse({"error": "Invalid plan assigned."}, status=400)

#         return JsonResponse({"success": "Data successfully added."}, status=200)

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)



