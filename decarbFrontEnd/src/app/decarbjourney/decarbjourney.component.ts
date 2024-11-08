import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; 

interface Journey {
  title: string;
  scope: string;
  years: number;
  months: number;
  days: number;
  costSavings: number;
  costUnit: string;
  co2Savings: number;
}

@Component({
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  selector: 'app-decarbonization',
  templateUrl: './decarbjourney.component.html',
  styleUrls: ['./decarbjourney.component.scss']
})
export class DecarbjourneyComponent {
  showModal = false;
  scopeOptions = ['Scope 1', 'Scope 2', 'Scope 3'];
  journeys: Journey[] = [];
  newJourney: Journey = {
    title: '',
    scope: '',
    years: 0,
    months: 0,
    days: 0,
    costSavings: 0,
    costUnit: 'K',
    co2Savings: 0
  };
  activeDropdown: number | null = null;
  editingJourneyIndex: number | null = null;

  constructor() {
    console.log('DecarbonizationComponent Initialized');
    
  }

  createJourney() {
    if (this.editingJourneyIndex !== null) {
      this.journeys[this.editingJourneyIndex] = { ...this.newJourney };
    } else {
      this.journeys.push({ ...this.newJourney });
    }

    this.closeModal();
  }

  deleteJourney(index: number) {
    this.journeys.splice(index, 1);
  }

  openModal(isEditing = false, index: number | null = null) {
    this.showModal = true;

    if (isEditing && index !== null) {
      this.editingJourneyIndex = index;
      this.newJourney = { ...this.journeys[index] }; 
    } else {
      // Reset for a new journey
      this.editingJourneyIndex = null;
      this.newJourney = {
        title: '',
        scope: '',
        years: 0,
        months: 0,
        days: 0,
        costSavings: 0,
        costUnit: 'K',
        co2Savings: 0
      };
    }
  }


  closeModal() {
    this.showModal = false;
    this.editingJourneyIndex = null;
  }

  toggleDropdown(index: number) {
    this.activeDropdown = this.activeDropdown === index ? null : index;
  }

  editJourney(index: number) {
    this.openModal(true, index);  
  }
}
