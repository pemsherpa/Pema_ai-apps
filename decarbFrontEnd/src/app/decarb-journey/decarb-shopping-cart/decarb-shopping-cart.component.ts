import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

interface CartItem {
  company_id: number;
  name: string;
  costSavings: number;
  co2Savings: number;
  transition: number; // percentage of transition
};

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
    
  ];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchScopeData();
  }

  public fetchScopeData(): void {
    this.http.get<{ cs_backend_data: { scope_total: ScopeData } }>('../../assets/yearly_quarterly_steps.json')
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
  getFormattedTotalCostSavings(): string {
    const totalSavingsInK = this.getTotalCostSavings() / 1000;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 2, // Optional: limit decimals to 2
    }).format(totalSavingsInK) + 'K'; // Append 'K' to the formatted value
  }
  
  

  getTotalCO2Savings(): number {
    return this.cartItems.reduce((total, item) => total + item.co2Savings, 0);
  }
  formatCostSavings(value: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
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
    return (scope / this.scopeData.scope_total) * 100 * 100;
  }
  
  // Function to return the appropriate facial expression based on the progress percentage
  getExpression(): string {
    const progressPercentage = this.getProgressPercentage();

    if (progressPercentage <= 25) {
      return '../../assets/red-smily.svg';
    } else if (progressPercentage <= 50) {
      return '../../assets/orange-smily.svg';
    } else if (progressPercentage <= 75) {
      return '../../assets/yellow-smily.svg';
    } else {
      return '../../assets/green-smily.svg';
    }
  }

  removeItem(index: number) {
    this.cartItems.splice(index, 1);
    this.updateProgress();
  }

  addItem(item: CartItem) {
    const existingItem = this.cartItems.find(cartItem => cartItem.company_id === item.company_id);
    if (!existingItem) {
      this.cartItems.push(item);
      //this.saveItemToDatabase(item);
      console.log("I'm adding..... ")
    }
  }

  removeItemByName(itemName: string) {
    this.cartItems = this.cartItems.filter(item => item.name !== itemName);
  }
  saveItemToDatabase(item: CartItem): void {
    const apiUrl = 'http://127.0.0.1:8000/yearly_steps/add-shopping-cart/'; // Replace with actual API URL
    this.http.post(apiUrl, item).subscribe({
      next: () => console.log('Item saved to database successfully!'),
      error: (err) => console.error('Error saving item to database:', err),
    });
  }


  updateProgress() {
    this.getProgressPercentage();
  }
}