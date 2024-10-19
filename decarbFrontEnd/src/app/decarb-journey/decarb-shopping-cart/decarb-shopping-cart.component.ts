import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface CartItem {
  name: string;
  costSavings: number;
  co2Savings: number;
  transition: number; // percentage of transition
}

interface ScopeData {
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
  styleUrls: ['./decarb-shopping-cart.component.css'],
})
export class DecarbShoppingCartComponent implements OnInit {
  targetGoal: number = 40000; // Example target goal
  scopeData: ScopeData | null = null;
  showScopeTargets = false;

  cartItems: CartItem[] = [
    { name: 'Change Electricity Provider', costSavings: 6000, co2Savings: -100, transition: 50 },
    { name: 'Switch to Business class travel', costSavings: 2500, co2Savings: -45, transition: 25 }
  ];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchScopeData();
  }

  public fetchScopeData(): void {
    this.http.get<{ cs_backend_data: { scope_total: ScopeData } }>('/yearly_quarterly_steps.json')
      .subscribe({
        next: (data) => {
          this.scopeData = data.cs_backend_data.scope_total;
        },
        error: (err) => {
          console.error('Error fetching scope data:', err);
        }
      });
  }

  getTotalCostSavings(): number {
    return this.cartItems.reduce((total, item) => total + item.costSavings, 0);
  }

  getTotalCO2Savings(): number {
    return this.cartItems.reduce((total, item) => total + item.co2Savings, 0);
  }

  getProgressPercentage(): number {
    const totalCO2Savings = this.getTotalCO2Savings();
    return (Math.abs(totalCO2Savings) / this.targetGoal) * 100;
  }

  getScopePercentage(scope: number): number {
    if (!this.scopeData || this.scopeData.scope_total === 0) {
      console.warn('scope_total is zero or undefined');
      return 0; 
    }
    //console.log('scope:', scope, 'scope_total:', this.scopeData.scope_total);
    return (scope / this.scopeData.scope_total) * 100*100;
  }
  

  removeItem(index: number) {
    this.cartItems.splice(index, 1);
    this.updateProgress();
  }

  addItem() {
    this.cartItems.push({ name: 'New Journey Item', costSavings: 3000, co2Savings: -600, transition: 0 });
    this.updateProgress();
  }

  updateProgress() {
    this.getProgressPercentage();
  }
}
