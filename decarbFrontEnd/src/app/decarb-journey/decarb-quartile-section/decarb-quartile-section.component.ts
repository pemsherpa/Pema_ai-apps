import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Component({
  selector: 'cs-decarb-quartile-section',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './decarb-quartile-section.component.html',
  styleUrls: ['./decarb-quartile-section.component.css'],
})
export class DecarbQuartileSectionComponent implements OnInit {
  quartileData: any[] = [];
  selectedYear = 2024;  // Default year to filter by
  selectedQuarter = 4;  // Default quarter to filter by

  @Output() itemChecked = new EventEmitter<{
    name: string;
    costSavings: number;
    co2Savings: number;
    transition: number;
    isChecked: boolean;
  }>();

  isDropdownOpen: { [key: string]: boolean } = {};
  quartileSelected: boolean[] = [false, false, false, false];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchQuartileData().subscribe({
      next: (data: any) => {
        // Filter and map the JSON data for the selected year and quarter
        const yearData = data.yearly_steps.find(
          (step: any) => step.year === this.selectedYear && step.quarter === this.selectedQuarter
        );

        if (yearData) {
          this.quartileData = [
            {
              title: 'Scope 1 Actions',
              scopeDescription: 'Steps to reduce scope 1 emissions.',
              dropdowns: yearData.scope1_steps || []
            },
            {
              title: 'Scope 2 Actions',
              scopeDescription: 'Steps to reduce scope 2 emissions.',
              dropdowns: yearData.scope2_steps.map((step: any) => ({
                ...step,
                title: step.recommendation.message,  // Use plan name as title
                description: step.recommendation.recommended_plan,      // Use recommendation message
                providerInfo: step.recommendation.provider_info,  // Map provider information if needed
              })) || []
            },
            {
              title: 'Scope 3 Actions',
              scopeDescription: 'Steps to reduce scope 3 emissions.',
              dropdowns: yearData.scope3_steps || []
            }
          ];
        } else {
          console.error('Data not found for selected year and quarter.');
        }
      },
      error: (error) => {
        console.error('Error loading quartile data:', error);
      }
    });
  }

  fetchQuartileData(): Observable<any> {
    return this.http.get<any>('/yearly_quarterly_steps.json');
  }

  toggleDropdown(dropdownId: string): void {
    this.isDropdownOpen[dropdownId] = !this.isDropdownOpen[dropdownId];
  }

  toggleCompletion(quartileIndex: number, dropdownIndex: number): void {
    const selectedDropdown = this.quartileData[quartileIndex].dropdowns[dropdownIndex];
    selectedDropdown.isCompleted = !selectedDropdown.isCompleted;

    this.itemChecked.emit({
      name: selectedDropdown.title,
      costSavings: selectedDropdown.savings || 0,
      co2Savings: -selectedDropdown.emissions_savings || 0,
      transition: selectedDropdown.difficulty || 0,
      isChecked: selectedDropdown.isCompleted,
    });
  }

  toggleQuartileButton(index: number): void {
    this.quartileSelected[index] = !this.quartileSelected[index];
  }
}

