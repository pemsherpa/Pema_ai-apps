import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Scope1StepsComponent } from '../quartile-steps/scope1-steps/scope1-steps.component';
import { Scope2StepsComponent } from '../quartile-steps/scope2-steps/scope2-steps.component';
import { Scope3StepsComponent } from '../quartile-steps/scope3-steps/scope3-steps.component';

@Component({
  selector: 'cs-decarb-quartile-section',
  standalone: true,
  imports: [CommonModule, FormsModule, Scope1StepsComponent, Scope2StepsComponent, Scope3StepsComponent],
  templateUrl: './decarb-quartile-section.component.html',
  styleUrls: ['./decarb-quartile-section.component.css'],
})
export class DecarbQuartileSectionComponent implements OnInit {
  quartileData: any[] = [];
  availableYears: number[] = [];
  selectedYears: { [year: number]: boolean } = {};
  selectedQuarter = 4;

  @Output() itemChecked = new EventEmitter<{
    name: string;
    costSavings: number;
    co2Savings: number;
    transition: number;
    providerInfo: any[];
    isChecked: boolean;
  }>();

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.availableYears = Array.from({ length: 5}, (_, i) => 2024 + i);
    this.availableYears.forEach(year => this.selectedYears[year] = true);
    this.loadDataForYearAndQuarter();
  }

  toggleYearSelection(year: number): void {
    this.selectedYears[year] = !this.selectedYears[year];
    this.loadDataForYearAndQuarter();
  }

  loadDataForYearAndQuarter(): void {
    this.fetchQuartileData().subscribe({
      next: (data: any) => {
        this.quartileData = [];

        // Only load data for selected years
        this.availableYears.forEach(year => {
          if (this.selectedYears[year]) {
            const yearData = data.yearly_steps.find(
              (step: any) => step.year === year && step.quarter === this.selectedQuarter
            );
            if (yearData) {
              this.quartileData.push(...this.mapYearData(yearData));
            }
          }
        });
        console.log(this.quartileData); // Verify the data structure
      },
      error: (error) => {
        console.error('Error loading quartile data:', error);
      },
    });
  }

  private mapYearData(yearData: any): any[] {
    return [
      ...yearData.scope1_steps.map((step: any) => ({
        ...step,
        scope: 'scope1',
        isExpanded: false,
      })),
      ...yearData.scope2_steps.map((step: any) => ({
        title: step.recommendation?.recommended_plan,
        description: step.description,
        costSavings: step.savings,
        co2Savings: step.emissions_savings,
        transition: step.difficulty,
        isCompleted: false,
        providerInfo: step.recommendation?.provider_info.map((provider: any) => ({
          name: provider.company,
          details: provider['description of the company'],
          renewablePercentage: provider['renewable percent provided'],
          phone: provider.phone_number,
          website: provider.website_link,
        })) || [],
        scope: 'scope2',
        isExpanded: false,
      })),
      ...yearData.scope3_steps.map((step: any) => ({
        title: step.description || 'Scope 3 Step',
        costSavings: step.savings,
        co2Savings: step.emissions_savings,
        transition: step.difficulty,
        isCompleted: false,
        providerInfo: step.recommendation?.provider_info || [],
        scope: 'scope3',
        isExpanded: false,
      })),
    ];
  }

  fetchQuartileData(): Observable<any> {
    return this.http.get<any>('../../assets/yearly_quarterly_steps.json');
  }

  toggleStep(index: number): void {
    this.quartileData[index].isExpanded = !this.quartileData[index].isExpanded;
  }

  onStepToggled(step: any): void {
    this.itemChecked.emit({
      name: step.title,
      costSavings: step.costSavings,
      co2Savings: -step.co2Savings,
      transition: step.transition,
      providerInfo: step.providerInfo,
      isChecked: step.isCompleted,
    });
  }
}
