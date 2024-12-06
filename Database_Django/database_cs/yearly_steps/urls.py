from django.urls import path
from yearly_steps.views import load_json_data
from yearly_steps.views import *
from django.shortcuts import render

urlpatterns = [
    # Other URLs
    path('load-json/', load_json_data, name='load_json'),
    path('trigger-vector-processing/', trigger_vector_processing, name='trigger_vector_processing'),
    #path('find_anomalies/', find_total_co2e_anomalies, name='find_anomalies'),
    path('create-vector-table/', create_and_update_vector_table, name='create_vector_table'),
    path('detect_anomalies/', detect_anomalies, name='detect_anomalies'),
    path('', lambda request: render(request, 'yearly_steps/index.html'), name='home'),
]
