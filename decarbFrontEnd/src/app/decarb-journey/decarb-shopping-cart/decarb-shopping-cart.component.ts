import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import * as scopeDataFile from './assets/yearly_quarterly_steps.json'; // Use a relative path


interface CartItem {
  name: string;
  costSavings: number;
  co2Savings: number;
  transition: number; // percentage of transition
}

interface ScopeData {
  company_id: number; 
  scope_1_total: number;
  scope_2_total: number;
  scope_3_total: number;
  scope_total: number;
  scope_1_target: number;
  scope_2_target: number;
  scope_3_target: number;
  target_timeframe: number;
}

@Component({
  selector: 'cs-decarb-shopping-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './decarb-shopping-cart.component.html',
  styleUrls: ['./decarb-shopping-cart.component.css']
})
export class DecarbShoppingCartComponent implements OnInit {
  targetGoal: number = 40000;   // Fake value
  scopeData: ScopeData | null = null; // Initialize scopeData
  showScopeTargets = false;

  // Journey items for the shopping cart
  cartItems: CartItem[] = [
    { name: 'Change Electricity Provider', costSavings: 6000, co2Savings: -100, transition: 50 },
    { name: 'Switch to Business class travel', costSavings: 2500, co2Savings: -45, transition: 25 }
  ];

  constructor() {}

  ngOnInit(): void {
    this.fetchScopeData();
    console.log(this.scopeData);
  }

  fetchScopeData(): void {
    // Directly access the imported JSON data and assign it to scopeData
    this.scopeData = (scopeDataFile as any).cs_backend_data.scope_total;
  }

  // Calculate the total cost savings
  getTotalCostSavings(): number {
    return this.cartItems.reduce((total, item) => total + item.costSavings, 0);
  }

  getTotalCO2Savings(): number {
    return this.cartItems.reduce((total, item) => total + item.co2Savings, 0);
  }

  getProgressPercentage(): number {
    const currentSavings = this.getTotalCO2Savings(); // Calculate current savings dynamically
    return (currentSavings / this.targetGoal) * 100;
  }

  getScopePercentage(scope: number): number {
    return this.scopeData ? (scope / this.scopeData.scope_total) * 100 : 0;
  }

  removeItem(index: number) {
    this.cartItems.splice(index, 1);
  }

  addItem() {
    this.cartItems.push({ name: 'New Journey Item', costSavings: 3000, co2Savings: -60, transition: 0 });
  }
}
