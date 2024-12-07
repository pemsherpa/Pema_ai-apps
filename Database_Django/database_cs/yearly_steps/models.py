from django.db import models
from pgvector.django import VectorField

# Yearly quarterly steps, from JSON 
class Company(models.Model):
    company_id = models.IntegerField(unique=True)  # This is now the unique identifier for referencing


class ScopeTotal(models.Model):
    company = models.ForeignKey(Company, to_field='company_id', on_delete=models.CASCADE)
    scope_1_total = models.FloatField()
    scope_2_total = models.FloatField()
    scope_3_total = models.FloatField()
    scope_total = models.FloatField()
    scope_1_target = models.FloatField()
    scope_2_target = models.FloatField()
    scope_3_target = models.FloatField()
    target_timeframe = models.CharField(max_length=100)

class YearlyStep(models.Model):
    company = models.ForeignKey(Company, to_field='company_id', on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.IntegerField()

class ScopeStep(models.Model):
    yearly_step = models.ForeignKey(YearlyStep, on_delete=models.CASCADE)
    scope_type = models.CharField(max_length=20)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    savings = models.FloatField()
    emissions_savings = models.FloatField()

class Recommendation(models.Model):
    scope_step = models.ForeignKey(ScopeStep, on_delete=models.CASCADE)
    recommended_plan = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    carbon_emission_savings = models.FloatField(blank=True, null=True)
    cost_savings = models.FloatField(blank=True, null=True)
    peak_cost = models.FloatField(blank=True, null=True)
    off_peak_cost = models.FloatField(blank=True, null=True)

class ScopeVector(models.Model):
    year = models.IntegerField()
    quarter = models.IntegerField()
    scope_name = models.CharField(max_length=20)  # 'scope1', 'scope2', 'scope3'
    vector = VectorField(dimensions=6)  # pgvector with 6 dimensions

    class Meta:
        db_table = 'scope_vector'


# class Total_CO2e(models.Model):
#     comp = models.IntegerField()
#     scope = models.IntegerField()
#     subcategory = models.FloatField()
#     year = models.IntegerField()
#     total_co2e = models.FloatField()


# class Total_CO2eVector(models.Model):
#     co2e_vector = VectorField(dimensions=1)
#     total_co2e = models.ForeignKey('yearly_steps.Total_CO2e', on_delete=models.CASCADE, db_column='parent_id')

#     class Meta:
#         managed = True
#         db_table = 'total_co2e_vector'


# Shopping cart 
class ShoppingCartContent(models.Model):
    company_id = models.IntegerField(default=1)
    name=models.TextField()
    transition= models.FloatField()
    costSavings = models.FloatField()
    co2savings = models.FloatField()

    class Meta:
        managed = True
        db_table = 'ShoppingCartContent'


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

class VectorTotalCO2e(models.Model):
    co2e_vector = VectorField(dimensions=4)
    total_co2e = models.ForeignKey('yearly_steps.Total_CO2e', on_delete=models.CASCADE, db_column='parent_id')

    class Meta:
        managed = True
        db_table = 'vector_total_co2e'
