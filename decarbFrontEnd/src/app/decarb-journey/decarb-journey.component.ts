import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet } from '@angular/router';
import { DecarbShoppingCartComponent } from './decarb-shopping-cart/decarb-shopping-cart.component';
import { DecarbQuartileSectionComponent } from './decarb-quartile-section/decarb-quartile-section.component';
//import yearlyQuarterlySteps from '...'

@Component({
  selector: 'app-decarb-journey',
  standalone: true,
  imports: [RouterOutlet, RouterModule,DecarbShoppingCartComponent,DecarbQuartileSectionComponent, CommonModule, /*yearlyQuarterlySteps*/],
  templateUrl: './decarb-journey.component.html',
  styleUrl: './decarb-journey.component.css'
})
export class DecarbJourneyComponent implements AfterViewInit{
  title = 'decarbonization-journey';
  @ViewChild(DecarbShoppingCartComponent) shoppingcartComponent!: DecarbShoppingCartComponent;

  
  ngAfterViewInit(): void { 
    console.log("PRINT 1")
    if (this.shoppingcartComponent) { 
    this.shoppingcartComponent.fetchScopeData(); 
    console.log("Print")}}// Access custom component's methods or properties } }
  // // Data for 2024, quarters 1, 2, and 3
  // quartileData1: any;
  // quartileData2: any;
  // quartileData3: any;

  // constructor() {
  //   // Extract the relevant data for year 2024 and quarters 1, 2, and 3
  //   this.quartileData1 = yearlyQuarterlySteps.find(
  //     (entry: any) => entry.year === 2024 && entry.quarter === 1
  //   );
  //   this.quartileData2 = yearlyQuarterlySteps.find(
  //     (entry: any) => entry.year === 2024 && entry.quarter === 2
  //   );
  //   this.quartileData3 = yearlyQuarterlySteps.find(
  //     (entry: any) => entry.year === 2024 && entry.quarter === 3
  //   );
  //}


  // Define the quartile data with unique dropdowns for each quartile
  

}
