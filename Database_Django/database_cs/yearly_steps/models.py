from django.db import models
from pgvector.django import VectorField

# Company model
class Companys(models.Model):
    company_id = models.IntegerField(unique=True)  # Unique identifier for referencing

# ScopeTotal model
class ScopeTotals(models.Model):
    company = models.ForeignKey(Companys, to_field="company_id", on_delete=models.CASCADE)
    scope_1_total = models.FloatField()
    scope_2_total = models.FloatField()
    scope_3_total = models.FloatField()
    scope_total = models.FloatField()
    scope_1_target = models.FloatField()
    scope_2_target = models.FloatField()
    scope_3_target = models.FloatField()
    target_timeframe = models.IntegerField()

# ScopeSteps model
class ScopeSteps(models.Model):
    company = models.ForeignKey(Companys, to_field="company_id", on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.IntegerField()
    scope_type = models.IntegerField()  # 1, 2, or 3
    description = models.TextField()
    difficulty = models.IntegerField()
    cost_savings = models.FloatField()
    emissions_savings = models.FloatField()
    total_cost = models.FloatField()
    total_emissions = models.FloatField()
    transition_percentage = models.IntegerField()

# Providers model
class Providers(models.Model):
    company_name = models.CharField(max_length=255, unique=True)  # Company name
    renewable_percent = models.FloatField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class Plans(models.Model):
    plan_name = models.CharField(max_length=100)
    carbon_savings = models.FloatField()
    cost_savings = models.FloatField()
    peak_cost = models.FloatField()
    off_peak_cost = models.FloatField()
    total_cost = models.FloatField()
    company = models.ForeignKey(Providers, on_delete=models.CASCADE, related_name="plans")  # Foreign key relationship

# Recommendations model
class Recommendations(models.Model):
    scope_step = models.ForeignKey(ScopeSteps, on_delete=models.CASCADE)
    recommended_plan = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    plan_name = models.TextField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    renewable_percent_provided = models.FloatField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    description_of_company = models.TextField(blank=True, null=True)
    carbon_savings = models.FloatField(blank=True, null=True)
    cost_savings = models.FloatField(blank=True, null=True)
    peak_cost = models.FloatField(blank=True, null=True)
    off_peak_cost = models.FloatField(blank=True, null=True)
    total_cost_with_peak_and_off_peak = models.FloatField(blank=True, null=True)
    plan= models.ForeignKey(Plans, on_delete=models.CASCADE, null=True, blank=True)
    
    #carbon_emission_savings = models.FloatField(blank=True, null=True)
    #cost_savings = models.FloatField(blank=True, null=True)

# Shopping cart 

class ShoppingCartContent(models.Model):
    company_id = models.IntegerField(default=1)
    # name=models.TextField()
    # transition= models.FloatField()
    # costSavings = models.FloatField()
    # co2savings = models.FloatField()
    providers=models.ForeignKey(Providers, on_delete=models.CASCADE, null=True, blank=True)
    plan= models.ForeignKey(Plans, on_delete=models.CASCADE, null=True, blank=True)  # Foreign key reference to Plans

    class Meta:
        # unique_together = ('company_id', 'provider') # yet to implement (10.11.2024)
        managed = True
        db_table = 'shopping_cart_content'


# Tables for Anomaly detection

class Total_CO2e(models.Model):
    comp = models.IntegerField()
    scope = models.IntegerField()
    subcategory = models.FloatField()
    year = models.IntegerField()
    total_co2e = models.FloatField()
    gas1 = models.FloatField()
    gas2 = models.FloatField()
    gas3 = models.FloatField()


# class VectorTotalCO2e(models.Model):
#     co2e_vector = VectorField(dimensions=4)
#     total_co2e = models.ForeignKey('yearly_steps.Total_CO2e', on_delete=models.CASCADE, db_column='parent_id')

#     class Meta:
#         managed = True
#         db_table = 'vector_total_co2e'


