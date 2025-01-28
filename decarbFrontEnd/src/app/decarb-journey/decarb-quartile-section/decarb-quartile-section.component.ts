import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { HttpClient,HttpParams  } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators'
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Scope1StepsComponent } from '../quartile-steps/scope1-steps/scope1-steps.component';
import { Scope2StepsComponent } from '../quartile-steps/scope2-steps/scope2-steps.component';
import { Scope3StepsComponent } from '../quartile-steps/scope3-steps/scope3-steps.component';
import {ShoppingCartItem} from '../../cart-item.model';
import { tap } from 'rxjs/operators';
import { catchError } from 'rxjs/operators';


interface StepData {
  id: number;
  year: number;
  quarter: number;
  scope_type: number;
  description: string;
  difficulty: number;
  transition_percentage: number;
  company_name: number;
  plan_name: string;
  provider_name: string;
  phone_number: string;
  website_link: string;
  provider_description: string;
  carbon_cost: number;
  total_cost: number;
  peak_cost: number | null;
  off_peak_cost: number | null;
  data?: any;
}


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
    provider_name:string;
    company_id:number;
    plan_name:string;

  }>();
  @Output() makeSwitchClicked = new EventEmitter<string>();
  @Output() items = new EventEmitter<ShoppingCartItem>();

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
      next: (response: any) => {
        if (!response || !Array.isArray(response.yearly_steps)) {
          console.error("Invalid API structure: ", response)
        }
        this.quartileData = [];

        this.availableYears.forEach((year) => {
          if (this.selectedYears[year]) {
            const filteredData = response.yearly_steps.filter(
              (step: any) =>
                step.year === year &&
                this.selectedQuarters[step.quarter] // Check if the quarter is selected
            );

            filteredData.forEach((step: any) => {
              this.quartileData.push(this.mapStepToQuartileData(step));
            });
          }
        });

        //console.log(this.quartileData);
      },
      error: (error) => {
        console.error('Error loading quartile data:', error);
      },
    });
  }

  // old read from json code
  // private mapYearData(yearData: any, year: number, quarter: number): any[] {
  //   return [
  //     ...yearData.scope1_steps.map((step: any) => ({
  //       title: step.recommendation?.message,
  //       ...step,
  //       scope: 'Scope1',
  //       year: year,
  //       quarter: quarter,
  //     })),
  //     ...yearData.scope2_steps.map((step: any) => ({
  //       company_id: yearData.company_id,
  //       title: step.recommendation?.message,
  //       description: step.description,
  //       cost_savings: step.cost_savings,
  //       co2_savings: step.co2_savings,
  //       difficulty: step.difficulty,
  //       our_recommendation: step.ourrecommendation,
  //       isCompleted: false,
  //       providerInfo:
  //         step.recommendation?.provider_info.map((provider: any) => ({
  //           name: provider.company,
  //           details: provider['description of the company'],
  //           renewablePercentage: provider['renewable percent provided'],
  //           phone: provider.phone_number,
  //           website: provider.website_link,
  //         })) || [],
  //       transition: step.transition_percentage,
  //       scope: 'Scope2',
  //       year: year,
  //       quarter: quarter,
  //     })),
  //     ...yearData.scope3_steps.map((step: any) => {
  //       const baseFields = {
  //         company_id: yearData.company_id,
  //         title: step.description,
  //         description: step.description,
  //         cost_savings: step.cost_savings,
  //         co2_savings: step.co2_savings,
  //         total_cost: step.total_cost,
  //         total_emissions: step.total_emissions,
  //         transition: step.transition_percentage,
  //         difficulty: step.difficulty,
  //         isCompleted: false,
  //         scope: 'Scope3',
  //         year: year,
  //         quarter: quarter
  //       };
  
  //       // Handle flight data with stops
  //       if (step.data?.stops !== undefined) {
  //         return {
  //           ...baseFields,
  //           type: 'flight',
  //           stops: step.data.stops
  //         };
  //       }
  
  //       // Handle commute recommendations
  //       else if (step.commute_step_recommendations) {
  //         return {
  //           ...baseFields,
  //           type: 'commute',
  //           commuteData: step.commute_step_recommendations.map((group: any) => ({
  //             group: group.group,
  //             members: group.members.map((member: any) => ({
  //               id: member.ID,
  //               method: member.method,
  //               location: member.locations,
  //               frequency: member.frequency,
  //               costPerKm: member.cost_per_km,
  //               coords: member.coords,
  //               distance: member.distance,
  //               emission: member.emission,
  //               distanceFromFirm: member.distance_from_firm,
  //               cost: member.cost,
  //               carpoolGroup: member.carpool_group
  //             })),
  //             message: group.message,
  //             savings: {
  //               money: group.money_saving,
  //               emission: group.emission_saving,
  //               distance: group.distance_saving
  //             }
  //           }))
  //         };
  //       }
  
  //       // Handle provider recommendations
  //       else if (step.recommendation) {
  //         return {
  //           ...baseFields,
  //           type: 'recommendation',
  //           recommendations: step.recommendation.map((rec: any) => ({
  //             plan: rec.recommended_plan,
  //             message: rec.message,
  //             carbonSavings: rec.carbon_emission_savings,
  //             costSavings: rec.cost_savings,
  //             providers: rec.provider_info.map((provider: any) => ({
  //               name: provider.plan_name,
  //               company: provider.company,
  //               details: provider['description of the company'],
  //               location: provider.location,
  //               phone: provider.phone_number,
  //               website: provider.website_link,
  //               carbonSavings: provider['Carbon savings'],
  //               costSavings: provider['Cost savings'],
  //               totalCost: provider['Total-Cost'],
  //               renewablePercent: provider['renewable percent provided']
  //             })),
  //             recommendedProvider: rec.our_recommendation
  //           }))
  //         };
  //       }
  
  //       else {
  //         console.log("couldn't identify type for scope3")
  //       }
  //       // Default case
  //       console.log("Answer: ", baseFields)
  //       return baseFields;
  //     })
  //   ];
  // }

  private mapStepToQuartileData(step: StepData): any {
    const baseData = {
      id: step.id,
      year: step.year,
      quarter: step.quarter,
      scope_type: step.scope_type,
      description: step.description,
      difficulty: step.difficulty,
      transition_percentage: step.transition_percentage,
      company_name: step.company_name,
      plan_name: step.plan_name,
      provider_name: step.provider_name,
      phone_number: step.phone_number,
      website_link: step.website_link,
      provider_description: step.provider_description,
      carbon_cost: step.carbon_cost,
      total_cost: step.total_cost,
      peak_cost: step.peak_cost,
      off_peak_cost: step.off_peak_cost
    };
  
    // Check for commute groups
    if (step.data && Array.isArray(step.data)) {
      return {
        ...baseData,
        type: 'commute',
        commuteData: step.data.map(group => ({
          group: group.group,
          members: group.members.map((member: { ID: any; method: any; locations: any; frequency: any; distance: any; emission: any; coords: any; carpool_group: any; distance_from_firm: any; cost: any; }) => ({
            id: member.ID,
            method: member.method,
            location: member.locations,
            frequency: member.frequency,
            costPerKm: member.distance,
            emission: member.emission,
            coords: member.coords,
            carpoolGroup: member.carpool_group,
            distanceFromFrim: member.distance_from_firm,
            cost: member.cost
          })),
          money_saving: group.money_saving,
          distance_saving: group.distance_saving,
          emission_saving: group.emission_saving,
          message: group.message
        }))
      }
    }

    if (step.provider_name && step.description !== "Default provider for plans") {
      return {
        ...baseData,
        type: 'recommendation', 
        providerInfo: [{
          name: step.provider_name,
          details: step.provider_description, 
          phone: step.phone_number,
          website: step.website_link,
          carbon_cost: step.carbon_cost,
          total_cost: step.total_cost,
          transition_percentage: step.transition_percentage
        }]
      }
    }

    // come back and add for flights

    return baseData
  }
  

  fetchQuartileData(): Observable<any> {
    return this.http.get<any>('http://127.0.0.1:8000/yearly_steps/query_scope_steps/').pipe(
      map(resposne=> ({
        yearly_steps: resposne.data
      }))
    );
  }
  onItemChecked(CartItem: ShoppingCartItem): void {
    console.log("print",CartItem)
    // this.addItem(CartItem);
  }
  
  
  

  onStepToggled(step: any): void {
   const cartItem = {
      company_id: step.id,
      name: step.description,
      cost_savings: step.total_cost,
     co2_savings: -step.carbon_cost,
      transition: step.transition_percentage,
      providerInfo: step.providerInfo,
      isChecked: step.isCompleted,
    };
  
    const item: ShoppingCartItem = {
      provider_name: step.providerInfo[0]?.name || '',
      company_id: step.company_id,
      plan_name: step.providerInfo[0]?.plan_name || '',
    };
  
    // Emit the combined cart item to the parent
    this.itemChecked.emit(cartItem);
  
    // Emit the additional item for shopping cart
    this.itemCart.emit(item);

    console.log('Payload being sent to the API:', item); // Add this log
  if (!item.provider_name || !item.company_id || !item.plan_name) {
    console.error('Missing required fields in the payload:', item);
  }
  
    // Add the item to the cart
    this.addItem(item).subscribe({
      next: (response) => console.log('API Response:', response),
      error: (error) => console.error('Error while adding item to cart:', error),
    });
  
    // Logs for debugging
    console.log('Cart item emitted:', cartItem);
    console.log('Step', item.company_id);
    console.log('I am correct', item);
  }
  
 



  addItem(item: ShoppingCartItem): Observable<ShoppingCartItem> {
    console.log("shop",item)
    console.log("I am getting called");
    console.log("I am the cart item", item);
    
    // Perform the API call here
    return this.http.post<ShoppingCartItem>('http://127.0.0.1:8000/yearly_steps/add-shopping-cart',  item )
    
      .pipe( 
        
        tap({
          next: (response) => console.log('Item added to cart:', response),
          error: (error) => console.error('Error adding item to cart:', error),
          
        }),
        catchError((error) => {
          console.error('Error in POST request:', error);
          throw error; // rethrow the error after logging
        })
      );
      
      
  }
  
  
  }
  


