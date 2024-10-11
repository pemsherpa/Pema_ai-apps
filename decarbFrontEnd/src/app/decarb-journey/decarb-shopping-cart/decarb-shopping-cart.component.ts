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
  targetGoal: number = 40000;   //fake
  currentSavings: number = 15200; //fake

  // Shopping cart items hardcoded
  cartItems: CartItem[] = [
    { name: 'Change Electricity Provider', costSavings: 6000, co2Savings: -100, transition: 50 },
    { name: 'Switch to Business class travel', costSavings: 2500, co2Savings: -45, transition: 25 }
  ];

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
  // Remove item from the list
  removeItem(index: number) {
    this.cartItems.splice(index, 1);
  }

  // Add a new item to the list (you can modify this to accept custom input)
  addItem() {
    this.cartItems.push({ name: 'New Journey Item', costSavings: 3000, co2Savings: -60, transition: 0 });
  }

}
