from django.urls import path
from django.shortcuts import render
from yearly_steps.views import *
from yearly_steps.views_anomaly import *
from yearly_steps.views_create_vector import *
from yearly_steps.views_json_yearly import *

urlpatterns = [
    # Other URLs
    path('load-json/', load_json_data, name='load_json'),
    #path('trigger-vector-processing/', trigger_vector_processing, name='trigger_vector_processing'),
    #path('find_anomalies/', find_total_co2e_anomalies, name='find_anomalies'),
    path('create-vector-table/', create_and_update_vector_table, name='create_vector_table'),
    #path('detect_anomalies/', detect_anomalies, name='detect_anomalies'),
    path('', lambda request: render(request, 'yearly_steps/index.html'), name='home'),
    path('add-shopping-cart/', add_shopping_cart, name='add_shopping_cart'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('detect-iqr-anomalies/', detect_iqr_anomalies, name='detect_iqr_anomalies'),
    path('detect-cosine-anomalies/', detect_cosine_anomalies, name='detect_cosine_anomalies'),
]
