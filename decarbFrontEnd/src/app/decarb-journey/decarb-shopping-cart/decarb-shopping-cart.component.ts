import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface CartItem {
  name: string;
  costSavings: number;
  co2Savings: number;
  transition: number; // percentage of transition
}

@Component({
  selector: 'cs-decarb-shopping-cart',
  standalone: true,
  imports: [CommonModule], 
  templateUrl: './decarb-shopping-cart.component.html',
  styleUrl: './decarb-shopping-cart.component.css'
})
export class DecarbShoppingCartComponent {
  // Target goal for CO2 reduction
  targetGoal: number = 40000;   // Fake value
  currentSavings: number = 15200; // Fake value

  // Shopping cart items hardcoded
  cartItems: CartItem[] = [
    { name: 'Change Electricity Provider', costSavings: 6000, co2Savings: -100, transition: 50 },
    { name: 'Switch to Business class travel', costSavings: 2500, co2Savings: -45, transition: 25 }
  ];

  showScopeTargets = false; // For controlling the tooltip visibility

  // Hardcoded scope data for the progress bars
  scopeData = {
    scope_1_total: 100,
    scope_2_total: 50,
    scope_3_total: 10,
    scope_total: 160,
    scope_1_target: 0.75,  // 75% for Scope 1
    scope_2_target: 1.0,   // 100% for Scope 2
    scope_3_target: 0.5,   // 50% for Scope 3
    target_timeframe: 5,   // Timeframe in years
  };

  // Calculate the total savings
  getTotalCostSavings(): number {
    return this.cartItems.reduce((total, item) => total + item.costSavings, 0);
  }

  getTotalCO2Savings(): number {
    return this.cartItems.reduce((total, item) => total + item.co2Savings, 0);
  }

  getProgressPercentage(): number {
    return (this.currentSavings / this.targetGoal) * 100;
  }

  // Calculate individual scope percentage
  getScopePercentage(scope: number): number {
    return (scope / this.scopeData.scope_total) * 100;
  }

  // Remove item from the list
  removeItem(index: number) {
    this.cartItems.splice(index, 1);
  }

  // Add a new item to the list (you can modify this to accept custom input)
  addItem() {
    this.cartItems.push({ name: 'New Journey Item', costSavings: 3000, co2Savings: -60, transition: 0 });
  }
}
