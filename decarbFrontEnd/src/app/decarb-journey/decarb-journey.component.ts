// decarb-journey.ts
import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet } from '@angular/router';
import { DecarbShoppingCartComponent } from './decarb-shopping-cart/decarb-shopping-cart.component';
import { DecarbQuartileSectionComponent } from './decarb-quartile-section/decarb-quartile-section.component';

@Component({
  selector: 'app-decarb-journey',
  standalone: true,
  imports: [RouterOutlet, RouterModule, DecarbShoppingCartComponent, DecarbQuartileSectionComponent, CommonModule],
  templateUrl: './decarb-journey.component.html',
  styleUrls: ['./decarb-journey.component.css']
})
export class DecarbJourneyComponent implements AfterViewInit {
  title = 'decarbonization-journey';
  @ViewChild(DecarbShoppingCartComponent) shoppingcartComponent!: DecarbShoppingCartComponent;

  ngAfterViewInit(): void {
    console.log("PRINT 1");
    if (this.shoppingcartComponent) { 
      this.shoppingcartComponent.fetchScopeData(); 
      console.log("Print");
    }
  }

  // Update this method to handle the new structure of emitted data
  onItemChecked(event: { name: string; costSavings: number; co2Savings: number; transition: number; isChecked: boolean; }) {
    const { name, costSavings, co2Savings, transition, isChecked } = event;
    if (isChecked) {
      this.shoppingcartComponent.cartItems.push({ name, costSavings, co2Savings, transition });
      this.shoppingcartComponent.updateProgress();
    } else {
      const index = this.shoppingcartComponent.cartItems.findIndex(item => item.name === name);
      if (index !== -1) {
        this.shoppingcartComponent.removeItem(index);
      }
    }
  }
}



