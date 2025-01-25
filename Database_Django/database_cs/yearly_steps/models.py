from django.db import models
from pgvector.django import VectorField
from django.db.models import JSONField

# Company model
class Companys(models.Model):
    company_id = models.AutoField(primary_key=True)
    #company_id = models.IntegerField(unique=True)  # Unique identifier for referencing

# ScopeTotal model
class ScopeTotals(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companys, on_delete=models.CASCADE)
    scope_1_total = models.FloatField()
    scope_2_total = models.FloatField()
    scope_3_total = models.FloatField()
    scope_total = models.FloatField()
    scope_1_target = models.FloatField()
    scope_2_target = models.FloatField()
    scope_3_target = models.FloatField()
    target_timeframe = models.IntegerField()

# Providers model
class Providers(models.Model):
    id = models.AutoField(primary_key=True)
    providers_name = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    website_link = models.CharField(max_length=255)
    description = models.TextField()

class Plans(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Providers, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    carbon_cost = models.FloatField()
    total_cost = models.FloatField()
    peak_cost = models.FloatField(null=True, blank=True)
    off_peak_cost = models.FloatField(null=True, blank=True)
    #data=models.TextField(null=True, default="No data is provided")
    data = JSONField(null=True, default=dict)

# ScopeSteps model
class ScopeSteps(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companys, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    year = models.IntegerField()
    quarter = models.IntegerField()
    scope_type = models.IntegerField()  # 1, 2, or 3
    description = models.TextField()
    difficulty = models.IntegerField()
    transition_percentage = models.FloatField()


# Shopping cart 

class ShoppingCartContent(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Companys, on_delete=models.CASCADE)
    scope_step = models.ForeignKey(ScopeSteps, on_delete=models.CASCADE)
     


# Tables for Anomaly detection

class Total_CO2e(models.Model):
    id = models.AutoField(primary_key=True)
    comp = models.IntegerField()
    scope = models.IntegerField()
    subcategory = models.FloatField()
    year = models.IntegerField()
    total_co2e = models.FloatField()
    gas1 = models.FloatField()
    gas2 = models.FloatField()
    gas3 = models.FloatField()


# class VectorTotalCO2e(models.Model):
#     co2e_vector = VectorField(dimensions=3)
#     total_co2e = models.ForeignKey('yearly_steps.Total_CO2e', on_delete=models.CASCADE, db_column='parent_id')

#     class Meta:
#         managed = True
#         db_table = 'vector_total_co2e'
