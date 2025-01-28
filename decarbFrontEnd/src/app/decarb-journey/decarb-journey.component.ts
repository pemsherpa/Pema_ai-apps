import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet, Router } from '@angular/router';
import { DecarbShoppingCartComponent } from './decarb-shopping-cart/decarb-shopping-cart.component';
import { DecarbQuartileSectionComponent } from './decarb-quartile-section/decarb-quartile-section.component';
import { ShoppingCartItem } from '../cart-item.model';

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
    // Ensure the shopping cart and quartile components are initialized
    if (this.shoppingcartComponent) {
      this.shoppingcartComponent.fetchScopeData();
    }
  }

  cart: ShoppingCartItem[] = [];

  onItemAddedToCart(item: ShoppingCartItem): void {
    this.cart.push(item); // Add to the cartItems array
    console.log(item);
  }

  onItemChecked(event: {
    company_id: number;
    name: string;
    cost_savings: number;
    co2_savings: number;
    transition: number;
    isChecked: boolean;
  }) {
    const { company_id, name, cost_savings, co2_savings, isChecked } = event;
    const transition = event.transition || 0;

    if (isChecked) {
      this.shoppingcartComponent.cartItems.push({ company_id, name, cost_savings, co2_savings, transition });
      this.shoppingcartComponent.updateProgress();
    } else {
      // Remove item from cart
      const index = this.shoppingcartComponent.cartItems.findIndex(item => item.name === name);
      if (index !== -1) {
        this.shoppingcartComponent.cartItems.splice(index, 1); // Directly remove from array
      }
    }

    this.shoppingcartComponent.updateProgress(); // Update UI
  }

  goBack(): void {
    this.router.navigate(['/decarbonization']);
  }
}
