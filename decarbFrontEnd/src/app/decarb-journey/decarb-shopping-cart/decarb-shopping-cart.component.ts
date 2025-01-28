import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpParams } from '@angular/common/http';
import {ShoppingCartItem} from '../../cart-item.model';
import { tap } from 'rxjs/operators';
import { catchError } from 'rxjs/operators';
import { Observable } from 'rxjs';

interface CartItem {
  company_id: number;
  name: string;
  cost_savings: number;
  co2_savings: number;
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
  @Input() items: ShoppingCartItem[] = [];

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
    return this.cartItems.reduce((total, item) => total + item.cost_savings, 0);
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
    return this.cartItems.reduce((total, item) => total + item.co2_savings, 0);
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

    const itemToRemove = this.items[index];
    this.items.splice(index, 1);
    this.updateProgress();
    
    
    console.log("GOWRIIIIII",itemToRemove)
    this.deleteItem(itemToRemove).subscribe({
      next: (response) => {
        console.log('Item deleted from backend:', response);
        
      },
      error: (error) => {
        console.error('Error deleting item from backend:', error);
        // Optionally, re-add the item to the cart if the deletion fails
        // this.cartItems.splice(index, 0, itemToRemove);
      }
    });
  }
  deleteItem(item: ShoppingCartItem): Observable<any> {
    // Construct the query parameters for the GET request
    
    const params = new HttpParams()
      .set('provider_name', item.provider_name)
      .set('company_name', item.company_name) // Ensure company_id is a string
      .set('plan_name', item.plan_name);
  
    
  
    return this.http.get<any>(
      'http://127.0.0.1:8000/yearly_steps/delete-shopping-cart', 
      { params }
    ).pipe(
      tap({
        next: (response) => console.log('Item deleted successfully:', response),
        error: (error) => console.error('Error deleting item from cart:', error),
      }),
      catchError((error) => {
        console.error('Error in HTTP GET request:', error);
        throw error; // rethrow the error after logging
      })
    );
  }
  

  addItem(item: CartItem) {
    const existingItem = this.cartItems.find(cartItem => cartItem.company_id === item.company_id)
    if (!existingItem) {
      this.cartItems.push(item);
      //this.saveItemToDatabase(item);
      console.log("I'm adding..... ")
    }
  }

  removeItemByName(itemName: string) {
    this.cartItems = this.cartItems.filter(item => item.name !== itemName);
  }
  

  updateProgress() {
    this.getProgressPercentage();
  }
}