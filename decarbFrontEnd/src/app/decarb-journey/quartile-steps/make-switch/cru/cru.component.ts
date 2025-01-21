import { CommonModule, Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-cru',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cru.component.html',
  styleUrl: './cru.component.css'
})
export class CruComponent {
  stepData: any
  currentDetails = {
    currentProvider: '',
    currentPlan: '',
    currentCost: '',
    currentEmissions: ''
  }
  selectedProvider: any
  isModalOpen = false

  constructor(private http: HttpClient, public location: Location) {}

  ngOnInit(): void {
    const state = history.state;
    this.stepData = state.data || null;

    console.log(this.stepData);

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

  openModal(provider: any) {
    this.selectedProvider = provider
    this.isModalOpen = true
  }

  closeModal() {
    this.isModalOpen = false
    this.selectedProvider = null
  }

  isHighlighted(message: string): boolean {
    return message.includes('Carbon')
  }

  getImagePath(providerName: string): string {
    const imageMap: { [key: string]: string } = {
      'Climeworks': 'assets/env-pic1.jpg',
      'Carbon': 'assets/env-pic2.jpg',
      'MCE': 'assets/MCELogo.png',
      'PG&E': 'assets/PGELogo.png'
    };

    for (let key in imageMap) {
      if (providerName.includes(key)) {
        return imageMap[key];
      }
    }
    return 'assets/env-pic1.jpg';
  }

  trimUrlSpaces(providerUrl: string): string {
    return providerUrl.trim()
  }
}
