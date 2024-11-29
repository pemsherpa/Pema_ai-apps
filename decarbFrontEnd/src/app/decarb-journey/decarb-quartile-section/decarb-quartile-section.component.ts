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
  selectedQuarters: { [quarter: number]: boolean } = { 3: true, 4: true }; // Default selected quarters: 3 and 4

  @Output() itemChecked = new EventEmitter<{
    name: string;
    costSavings: number;
    co2Savings: number;
    transition: number;
    providerInfo: any[];
    isChecked: boolean;
  }>();
  @Output() makeSwitchClicked = new EventEmitter<string>();

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    const currentYear = new Date().getFullYear();
    this.availableYears = Array.from({ length: 5 }, (_, i) => currentYear + i);
    this.availableYears.forEach((year) => (this.selectedYears[year] = true));
    this.loadDataForYearAndQuarter();
  }

  toggleYearSelection(year: number): void {
    this.selectedYears[year] = !this.selectedYears[year];
    this.loadDataForYearAndQuarter();
  }

  toggleQuarterSelection(quarter: number): void {
    this.selectedQuarters[quarter] = !this.selectedQuarters[quarter];
    this.loadDataForYearAndQuarter();
  }
  onMakeSwitchClick(scope: string): void {
    this.makeSwitchClicked.emit(scope);
  }

  loadDataForYearAndQuarter(): void {
    this.fetchQuartileData().subscribe({
      next: (data: any) => {
        this.quartileData = [];

        this.availableYears.forEach((year) => {
          if (this.selectedYears[year]) {
            const filteredData = data.yearly_steps.filter(
              (step: any) =>
                step.year === year &&
                this.selectedQuarters[step.quarter] // Check if the quarter is selected
            );

            filteredData.forEach((yearData: any) => {
              this.quartileData.push(...this.mapYearData(yearData, year, yearData.quarter));
            });
          }
        });

        console.log(this.quartileData);
      },
      error: (error) => {
        console.error('Error loading quartile data:', error);
      },
    });
  }

  private mapYearData(yearData: any, year: number, quarter: number): any[] {
    return [
      ...yearData.scope1_steps.map((step: any) => ({
        title: step.recommendation?.message,
        ...step,
        scope: 'Scope1',
        year: year, // Add year
        quarter: quarter,
      })),
      ...yearData.scope2_steps.map((step: any) => ({
        title: step.recommendation?.message,
        description: step.description,
        costSavings: step.savings,
        co2Savings: step.emissions_savings,
        transition: step.transition_percentage,
        difficulty:step.difficulty,
        isCompleted: false,
        providerInfo:
          step.recommendation?.provider_info.map((provider: any) => ({
            name: provider.company,
            details: provider['description of the company'],
            renewablePercentage: provider['renewable percent provided'],
            phone: provider.phone_number,
            website: provider.website_link,
          })) || [],
        scope: 'Scope2',
        year: year, // Add year
        quarter: quarter,
      })),
      ...yearData.scope3_steps.map((step: any) => ({
        title: step.description,
        costSavings: step.savings,
        co2Savings: step.emissions_savings,
        transition: step.transition_percentage,
        difficulty:step.difficulty,
        isCompleted: false,
        providerInfo:
          step.recommendation?.recommendations?.flatMap((rec: any) =>
            rec.provider_info?.map((provider: any) => ({
              name: provider.company,
              details: provider.company_description,
              type: provider.type,
              location: provider.location,
              carbonSavings: -provider.carbon_savings,
              costSavings: provider.cost_savings,
              phone: provider.phone_number,
              website: provider.website_link,
            }))
          ) || [],
        scope: 'Scope3',
        year: year, // Add year
        quarter: quarter,
      })),
    ];
  }

  fetchQuartileData(): Observable<any> {
    return this.http.get<any>('../../assets/yearly_quarterly_steps.json');
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

