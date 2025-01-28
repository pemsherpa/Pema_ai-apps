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
    yearly_data = data.get("yearly_data")

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
                
        elif scope_id == 3 and quarter == 4:
            print("\nScope: ", scope_id)
            for step_data in yearly_data.get(scope_type, []):
                print("\nStep data: ", step_data)
                recommendation = step_data.get('recommendation', [])
                print("Recommendation",recommendation)
                our_recommendation = []
                provider_info_list = []
                
                for item in recommendation:
                    if isinstance(item, dict):
                        our_recommendation.append(item.get('our_recommendation', {}))
                        print("our_rec",our_recommendation)
                    else:
                        print("Item is not a dictionary:", item)
                
                for item in recommendation:
                    if isinstance(item, dict):
                        provider_info_list.extend(item.get('provider_info', []))
                    else:
                        print("Item is not a dictionary:", item)
                
                print("\nStep Data:", step_data)
                company_name = []  # Initialize as a list

                for item in our_recommendation:
                    if isinstance(item, dict):
                        name = item.get('company', 'Not Provided').strip()
                        if name:
                            company_name.append(name)
                            print("company",company_name)
                    else:
                        print("Unexpected item type in our_recommendation:", type(item))
                provider=None
                plan=None
                company_name=company_name[0]
                print(company_name)
                if company_name:
                # Look for plans via 'our_recommendation' first
                    for provider_info in provider_info_list:
                        if isinstance(provider_info, dict) and 'plan_name' in provider_info:
                            plan_name = provider_info['plan_name']
                            provider = Providers.objects.filter(providers_name=provider_info.get('company', 'Not Provided')).first()
                            print(provider)
                            if provider:
                                plan = Plans.objects.filter(
                                    plan_name=plan_name, 
                                    provider=provider
                                    ).first()
                                print("Plan found:", plan)
                    
                # Fallback to 'provider_info_list'
                if not plan:
                    for provider_info in provider_info_list:
                        if isinstance(provider_info, dict):
                            # Replace null values with 'Not Provided'
                            provider, _ = Providers.objects.get_or_create(
                                providers_name=provider_info.get('company', 'Not Provided'),
                                defaults={
                                    'phone_number': provider_info.get('phone_number', 'Not'),
                                    'website_link': provider_info.get('website_link', 'Not Provided'),
                                    'description': provider_info.get('description of the company', 'Not Provided'),
                                },
                            )

                            # Safely get or create the plan associated with the provider
                            plan_name = provider_info.get('plan_name', 'Not Provided')
                            plan, _ = Plans.objects.get_or_create(
                                provider=provider,
                                plan_name=plan_name,
                                defaults={
                                    'carbon_cost': provider_info.get('Carbon savings', 0),
                                    'total_cost': provider_info.get('Total-Cost', 0),
                                    'peak_cost': provider_info.get('Peak Cost', 0),
                                    'off_peak_cost': provider_info.get('Off-Peak Cost', 0),
                                },
                            )
                        else:
                            print(f"Invalid provider_info entry: {provider_info}")
                if plan and isinstance(plan, Plans):
                    print("\nEntering ScopeSteps, Adding CRU")
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
            print(f"Final Provider: {provider}")
            print(f"Final Plan: {plan}")

        elif scope_id == 3:
            print("\nScope: ", scope_id)
            for step_data in yearly_data.get(scope_type, []):
                data = step_data.get('data', {})
                plan = None
                print("\nStep Data:", step_data)

                description = step_data.get('description', 'No description provided')
                difficulty = step_data.get('difficulty', 0)
                transition_percentage = step_data.get('transition_percentage', 0.0)
                total_cost = step_data.get('total_cost', 0.0)
                total_emissions = step_data.get('total_emissions', 0.0)

                stops = step_data.get('stops', 0)
                commute_step_recommendations = step_data.get('commute_step_recommendations', [])

                # Determine the type of step and assign appropriate data
                
                if stops:
                    data_to_save = stops
                    plan_name = "Flight Plan"
                elif commute_step_recommendations:
                    data_to_save = commute_step_recommendations
                    plan_name = f"Commute Plan for the company{company_id}"
                else:
                    data_to_save = {}
                    plan_name = "Default Plan"

                provider, _ = Providers.objects.get_or_create(
                    providers_name="Default Provider",
                    defaults={
                        "phone_number": "000-000-0000",
                        "website_link": "http://example.com",
                        "description": "Default provider for plans"
                    }
                )

                plan, _ = Plans.objects.get_or_create(
                    provider=provider,
                    plan_name=plan_name,
                    defaults={
                        "carbon_cost": total_emissions,
                        "total_cost": total_cost,
                        "peak_cost": 0,
                        "off_peak_cost": 0,
                        "data": data_to_save
                    }
                )
                if plan and isinstance(plan, Plans):
                    print("\nEntering ScopeSteps, Plan present for scope 3 steps except cru")
                    ScopeSteps.objects.create(
                        company=company,
                        plan=plan,
                        year=year,
                        quarter=quarter,
                        scope_type=scope_id,
                        description=description,
                        difficulty=difficulty,
                        transition_percentage=transition_percentage)
                else:
                    return JsonResponse({"error": f"Invalid plan assigned for year {year}, quarter {quarter}."}, status=400)

    return JsonResponse({"success": "Data successfully added."}, status=200)