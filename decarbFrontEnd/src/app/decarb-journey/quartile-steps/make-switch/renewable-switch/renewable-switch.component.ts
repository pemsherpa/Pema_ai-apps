import { Component, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule, Location } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Chart, ArcElement, DoughnutController, Tooltip, Legend, Title, CategoryScale, LinearScale } from 'chart.js';

@Component({
  selector: 'app-renewable-switch',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './renewable-switch.component.html',
  styleUrls: ['./renewable-switch.component.css']
})
export class RenewableSwitchComponent implements AfterViewInit {
  stepData: any;
  userDetails = {
    name: '',
    email: '',
    dob: '',
    phone: '',
    isInterested: false,
  };
  currentDetails = {
    currentProvider: '',
    currentPlan: '',
    currentCost: '',
    currentEmissions: ''
  };

  activeIndex = 0

  costData!: number;
  co2Data!: number;

  constructor(private http: HttpClient, public location: Location) {}

  ngOnInit(): void {
    // Retrieve the passed data from navigation state
    const state = history.state;
    this.stepData = state.data || null;

    this.co2Data = this.stepData.carbon_cost
    this.costData = this.stepData.total_cost

    //console.log(this.stepData);
    this.http.get<any>('assets/yearly_quarterly_steps.json').subscribe(data => {
      // Assign the current details from the fetched data
      if (data && data.cs_backend_data.current_details) {
        this.currentDetails = {
          currentProvider: data.cs_backend_data.current_details.current_provider,
          currentPlan: data.cs_backend_data.current_details.current_plan,
          currentCost: data.cs_backend_data.current_details.current_cost,
          currentEmissions: data.cs_backend_data.current_details.current_emissions
        };
      }
    });
  }

  ngAfterViewInit(): void {
    
    this.RenderChart(0);
     // Ensure the chart is rendered after the view is initialized
  }

  RenderChart(index: number) {
    const costChartID = `cost-chart-${index}`
    const co2ChartID = `co2-chart-${index}`

    if (Chart.getChart(costChartID)) Chart.getChart(costChartID)?.destroy()
    if (Chart.getChart(co2ChartID)) Chart.getChart(co2ChartID)?.destroy()
    Chart.register(ArcElement, DoughnutController, Tooltip, Legend, Title, CategoryScale, LinearScale);
    const costChart = new Chart(costChartID, {
      type: 'doughnut',
      data: {
        labels: ['Cost Savings', 'Remaining'],
        datasets: [{
          label: 'Total Cost Savings',
          data: [this.costData, this.costData*4], // Assuming 100000 is the max
          backgroundColor: ['#6739E9', '#e0e0e0'],
          borderColor: 'white',
          borderWidth: 3,
          borderRadius: 5
        }]
      },
      options: {
        cutout: 50,
        aspectRatio: 2
      }
    });


    const co2Chart = new Chart(co2ChartID, {
      type: 'doughnut',
      data: {
        labels: ['CO2 Emissions', 'Remaining'],
        datasets: [{
          label: 'Total CO2 Emissions',
          data: [this.co2Data, 100-this.co2Data], // Assuming 100000 is the max
          backgroundColor: ['teal', '#e0e0e0'],
          borderColor: 'white',
          borderWidth: 3,
          borderRadius: 5,
        }]
      },
      options: {
        cutout: 50,
        aspectRatio: 2
      }
    });
  }

  onSubmit() {
    //console.log('User Details Submitted:', this.userDetails);
    alert('Thank you! Your details have been submitted.');
  }

  previousCard() {
    this.activeIndex = (this.activeIndex > 0) ? this.activeIndex - 1 : this.stepData.providerInfo.length - 1;
    this.RenderChart(this.activeIndex)
    //console.log(this.activeIndex);
  }

  nextCard() {
    this.activeIndex = (this.activeIndex < this.stepData.providerInfo.length - 1) ? this.activeIndex + 1 : 0;
    this.RenderChart(this.activeIndex);
    //console.log(this.activeIndex);
  }

  getImagePath(providerName: string): string {
    const imageMap: { [key: string]: string } = {
      'Ava': 'assets/ava-energy-logo.png',
      'SJCE': 'assets/SJCELogo.png',
      'MCE': 'assets/MCELogo.png',
      'PG&E': 'assets/PGELogo.png'
    };

    for (let key in imageMap) {
      if (providerName.includes(key)) {
        return imageMap[key];
      }
    }
    return 'assets/MCELogo.png';
  }
}
