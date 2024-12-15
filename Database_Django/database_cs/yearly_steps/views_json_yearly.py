import json
import os
from django.db import transaction
from pathlib import Path
from .models import *
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def load_json_data(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

    try:
        json_path = '../../decarbFrontEnd/src/assets/yearly_quarterly_steps.json'

        with open(json_path, 'r') as file:
            data = json.load(file)

        with transaction.atomic():
            # Extract and save company data
            company_data = data.get('cs_backend_data', {})
            company_id = company_data.get('company_id')
            if not company_id:
                return JsonResponse({"error": "Company ID missing in data."}, status=400)

            company, _ = Companys.objects.get_or_create(company_id=company_id)

            # Save ScopeTotals
            scope_total_data = company_data.get('scope_total', {})
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
                year = yearly_data.get('year')
                quarter = yearly_data.get('quarter')

                for scope_type, scope_id in [('scope1_steps', 1), ('scope2_steps', 2), ('scope3_steps', 3)]:
                    for step_data in yearly_data.get(scope_type, []):
                        scope_step = ScopeSteps.objects.create(
                            company=company,
                            year=year,
                            quarter=quarter,
                            scope_type=scope_id,
                            description=step_data.get('description', ''),
                            difficulty=step_data.get('difficulty', 0),
                            cost_savings=step_data.get('cost_savings', 0.0),
                            emissions_savings=step_data.get('co2_savings', 0.0),
                            total_cost=step_data.get('total_cost', 0.0),
                            total_emissions=step_data.get('total_emissions', 0.0),
                            transition_percentage=step_data.get('transition_percentage', 0),
                        )

                        # Save Recommendations
                        recommendation_data = step_data.get('recommendation')
                        if recommendation_data and scope_id in [1, 2]:  # Only Scope 1 and 2
                            provider_info = recommendation_data.get('provider_info', [])
                            for provider_data in provider_info:
                                provider, _ = Providers.objects.get_or_create(
                                    company_name=provider_data.get('company', ''),
                                    defaults={
                                        'renewable_percent': provider_data.get('renewable percent provided', 0),
                                        'phone_number': provider_data.get('phone_number', ''),
                                        'website_link': provider_data.get('website_link', ''),
                                        'description': provider_data.get('description of the company', ''),
                                    },
                                )
                                plan = Plans.objects.get_or_create(
                                    plan_name=provider_data.get('plan_name', ''),
                                    company=provider,
                                    defaults={
                                        'carbon_savings': provider_data.get('Carbon savings', 0.0),
                                        'cost_savings': provider_data.get('Cost savings', 0.0),
                                        'peak_cost': provider_data.get('Peak Cost', 0.0),
                                        'off_peak_cost': provider_data.get('Off-Peak Cost', 0.0),
                                        'total_cost': provider_data.get('Total-Cost_with_peak_and_off-peak', 0.0),
                                    },
                                )

                            if provider_info:
                                    first_provider=provider_info[0]
                                    plans=Plans.objects.filter(plan_name=first_provider.get('plan_name',''))
                                    if plans.exists():
                                        plan=plans.filter(company=provider).first()
                                        Recommendations.objects.create(
                                        scope_step=scope_step,
                                        plan=plan,
                                        provider_name = recommendation_data.get('recommended_plan', ''),
                                        message=recommendation_data.get('message', ''),
                                        plan_name=first_provider.get('plan_name', ''),
                                        company=first_provider.get('company', ''),
                                        phone_number=first_provider.get('phone_number', ''),
                                        website_link=first_provider.get('website_link', ''),
                                        description=first_provider.get('description of the company', ''),
                                        #location=first_provider.get('location', ''),
                                        carbon_savings=first_provider.get('Carbon savings', 0.0),
                                        cost_savings=first_provider.get('Cost savings', 0.0),
                                        peak_cost=first_provider.get('Peak Cost', 0.0),
                                        off_peak_cost=first_provider.get('Off-Peak Cost', 0.0),
                                        total_cost=first_provider.get('Total-Cost_with_peak_and_off-peak', 0.0),
                                )

        return JsonResponse({"message": "Data successfully loaded."}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
