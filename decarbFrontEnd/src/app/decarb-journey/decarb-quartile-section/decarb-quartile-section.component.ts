import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Scope1StepsComponent } from '../quartile-steps/scope1-steps/scope1-steps.component';
import { Scope2StepsComponent } from '../quartile-steps/scope2-steps/scope2-steps.component';
import { Scope3StepsComponent } from '../quartile-steps/scope3-steps/scope3-steps.component';
import {CartItem} from '../../cart-item.model';

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
  selectedQuarters: { [quarter: number]: boolean } = { 1: true, 2: true, 3: true, 4: true }; // Default selected quarters: 3 and 4

  @Output() yearsUpdated = new EventEmitter<{ [year: number]: boolean }>();

  @Output() itemChecked = new EventEmitter<{
    company_id: number;
    name: string;
    cost_savings: number;
    co2_savings: number;
    transition: number;
    providerInfo: any[];
    isChecked: boolean;
  }>();
  @Output() itemCart= new EventEmitter<{
    company_id:number;
    name:string;
    cost_savings:number;
    co2_savings:number;
    transition:number;

  }>();
  @Output() makeSwitchClicked = new EventEmitter<string>();

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    const currentYear = new Date().getFullYear();
    this.availableYears = Array.from({ length: 5 }, (_, i) => currentYear + i);
    this.availableYears.forEach((year) => (this.selectedYears[year] = true));
    this.loadDataForYearAndQuarter();
    const storedYears = sessionStorage.getItem('selectedYears');
    if (storedYears) {
      this.selectedYears = JSON.parse(storedYears);
      console.log(storedYears)
    } else {
      // Default to selecting all years
      this.availableYears.forEach((year) => (this.selectedYears[year] = true));
    }


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
        year: year,
        quarter: quarter,
      })),
      ...yearData.scope2_steps.map((step: any) => ({
        company_id: yearData.company_id,
        title: step.recommendation?.message,
        description: step.description,
        cost_savings: step.cost_savings,
        co2_savings: step.co2_savings,
        difficulty: step.difficulty,
        our_recommendation: step.ourrecommendation,
        isCompleted: false,
        providerInfo:
          step.recommendation?.provider_info.map((provider: any) => ({
            name: provider.company,
            details: provider['description of the company'],
            renewablePercentage: provider['renewable percent provided'],
            phone: provider.phone_number,
            website: provider.website_link,
          })) || [],
        transition: step.transition_percentage,
        scope: 'Scope2',
        year: year,
        quarter: quarter,
      })),
      ...yearData.scope3_steps.map((step: any) => {
        const baseFields = {
          company_id: yearData.company_id,
          title: step.description,
          description: step.description,
          cost_savings: step.cost_savings,
          co2_savings: step.co2_savings,
          total_cost: step.total_cost,
          total_emissions: step.total_emissions,
          transition: step.transition_percentage,
          difficulty: step.difficulty,
          isCompleted: false,
          scope: 'Scope3',
          year: year,
          quarter: quarter
        };
  
        // Handle flight data with stops
        if (step.data?.stops !== undefined) {
          return {
            ...baseFields,
            type: 'flight',
            stops: step.data.stops
          };
        }
  
        // Handle commute recommendations
        else if (step.commute_step_recommendations) {
          return {
            ...baseFields,
            type: 'commute',
            commuteData: step.commute_step_recommendations.map((group: any) => ({
              group: group.group,
              members: group.members.map((member: any) => ({
                id: member.ID,
                method: member.method,
                location: member.locations,
                frequency: member.frequency,
                costPerKm: member.cost_per_km,
                coords: member.coords,
                distance: member.distance,
                emission: member.emission,
                distanceFromFirm: member.distance_from_firm,
                cost: member.cost,
                carpoolGroup: member.carpool_group
              })),
              message: group.message,
              savings: {
                money: group.money_saving,
                emission: group.emission_saving,
                distance: group.distance_saving
              }
            }))
          };
        }
  
        // Handle provider recommendations
        else if (step.recommendation) {
          return {
            ...baseFields,
            type: 'recommendation',
            recommendations: step.recommendation.map((rec: any) => ({
              plan: rec.recommended_plan,
              message: rec.message,
              carbonSavings: rec.carbon_emission_savings,
              costSavings: rec.cost_savings,
              providers: rec.provider_info.map((provider: any) => ({
                name: provider.plan_name,
                company: provider.company,
                details: provider['description of the company'],
                location: provider.location,
                phone: provider.phone_number,
                website: provider.website_link,
                carbonSavings: provider['Carbon savings'],
                costSavings: provider['Cost savings'],
                totalCost: provider['Total-Cost'],
                renewablePercent: provider['renewable percent provided']
              })),
              recommendedProvider: rec.our_recommendation
            }))
          };
        }
  
        else {
          console.log("couldn't identify type for scope3")
        }
        // Default case
        console.log("Answer: ", baseFields)
        return baseFields;
      })
    ];
  }

  fetchQuartileData(): Observable<any> {
    return this.http.get<any>('../../assets/yearly_quarterly_steps.json');
  }
  onItemChecked(CartItem: CartItem): void {
    console.log(CartItem)
    this.addItem(CartItem);
  }
  
  addItem(cartItem: CartItem): void {
    console.log("I am gettting called")
    // Perform the API call here
    console.log(cartItem)
    this.http.post('http://127.0.0.1:8000/yearly_steps/add-shopping-cart/', cartItem).subscribe({
      next: (response) => console.log('Item added to cart:', response),
      error: (error) => console.error('Error adding item to cart:', error),
    });
  }
  

  onStepToggled(step: any): void {
   const cartItem = {
      company_id: step.company_id,
      name: step.title,
      cost_savings: step.cost_savings,
     co2_savings: -step.co2_savings,
      transition: step.transition,
      providerInfo: step.providerInfo,
      isChecked: step.isCompleted,
     };
  
  //   // Emit the cart item to the parent
    this.itemChecked.emit(cartItem);
  
  //   // The API call is no longer triggered here
    console.log('Cart item emitted:', cartItem);
   }
  onStepToggling(step:any):void{
    const item:CartItem={
      company_id:step.company_id,
      name:step.title,
      cost_savings:step.cost_savings,
      co2_savings:step.co2_savings,
      transition:step.transition
};
console.log("Step",item.company_id)
console.log("I am correct",item)
this.itemCart.emit(item);
  }
  }


