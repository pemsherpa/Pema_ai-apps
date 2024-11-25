import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Journey } from '../journey.model';
import dummyJourneys from './dummy-journeys.json';

@Component({
  standalone: true,
  imports: [FormsModule, CommonModule, RouterModule],
  selector: 'app-decarbonization',
  templateUrl: './decarbjourney.component.html',
  styleUrls: ['./decarbjourney.component.scss'],
})
export class DecarbjourneyComponent {
  showModal = false;
  scopeOptions = ['Scope 1', 'Scope 2', 'Scope 3'];
  
  journeys: Journey[] = dummyJourneys.map(
    (data) =>
      new Journey(
        data.title,
        data.scope,
        data.years,
        data.months,
        data.days,
        data.costSavings,
        data.costUnit,
        data.co2Savings
      )
  );

  newJourney: Journey = new Journey('', [], 0, 0, 0, 0, 'K', 0);
  activeDropdown: number | null = null;
  editingJourneyIndex: number | null = null;

  constructor() {
    console.log('DecarbonizationComponent Initialized');
    console.log(this.journeys);
  }

  updateJourney(index: number) {
    const journey = this.journeys[index];
    this.updateDecarbJourneyAPI(journey);
  }

  updateDecarbJourneyAPI(journey: Journey) {
    console.log('API called with:', journey);
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
      this.editingJourneyIndex = null;
      this.newJourney = new Journey('', [], 0, 0, 0, 0, 'K', 0);
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

  toggleScope(option: string) {
    const index = this.newJourney.scope.indexOf(option);
    if (index > -1) {
      this.newJourney.scope.splice(index, 1);
    } else {
      this.newJourney.scope.push(option);
    }
  }
}
