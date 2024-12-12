import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet, Router } from '@angular/router';
import { DecarbShoppingCartComponent } from './decarb-shopping-cart/decarb-shopping-cart.component';
import { DecarbQuartileSectionComponent } from './decarb-quartile-section/decarb-quartile-section.component';

@Component({
  selector: 'app-decarb-journey',
  standalone: true,
  imports: [RouterOutlet, RouterModule, DecarbShoppingCartComponent, DecarbQuartileSectionComponent, CommonModule],
  templateUrl: './decarb-journey.component.html',
  styleUrls: ['./decarb-journey.component.css'],
})
export class DecarbJourneyComponent implements AfterViewInit {
  title = 'decarbonization-journey';

  @ViewChild(DecarbShoppingCartComponent) shoppingcartComponent!: DecarbShoppingCartComponent;
  @ViewChild(DecarbQuartileSectionComponent) quartileSectionComponent!: DecarbQuartileSectionComponent;

  constructor(private router: Router) {}

  ngAfterViewInit(): void {
    // Restore cart items from sessionStorage
    const storedCartItems = sessionStorage.getItem('cartItems');
    if (storedCartItems && this.shoppingcartComponent) {
      this.shoppingcartComponent.cartItems = JSON.parse(storedCartItems);
      this.shoppingcartComponent.updateProgress();
    }

    // Restore selected years from sessionStorage
    const storedYears = sessionStorage.getItem('selectedYears');
    if (storedYears && this.quartileSectionComponent) {
      const years = JSON.parse(storedYears);
      this.quartileSectionComponent.selectedYears = { ...years }; // Directly assign the restored state
      this.quartileSectionComponent.loadDataForYearAndQuarter(); // Reload data based on restored years
    }

    // Fetch scope data if needed
    if (this.shoppingcartComponent) {
      this.shoppingcartComponent.fetchScopeData();
    }
  }

  onItemChecked(event: {company_id:number, name: string; costSavings: number; co2Savings: number; transition: number; isChecked: boolean }) {
    const {company_id, name, costSavings, co2Savings, isChecked } = event;
    const transition = event.transition || 0;

    if (isChecked) {
      this.shoppingcartComponent.cartItems.push({ company_id, name, costSavings, co2Savings, transition });
      this.shoppingcartComponent.updateProgress();
    } else {
      // Remove item from cart
      const index = this.shoppingcartComponent.cartItems.findIndex(item => item.name === name);
      if (index !== -1) {
        this.shoppingcartComponent.cartItems.splice(index, 1); // Directly remove from array
      }
    }

    // Save updated cart items to sessionStorage
    sessionStorage.setItem('cartItems', JSON.stringify(this.shoppingcartComponent.cartItems));
    this.shoppingcartComponent.updateProgress(); // Update UI
  }

  goBack(): void {
    this.router.navigate(['/decarbonization']);
  }
}
