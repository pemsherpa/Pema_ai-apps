import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { DecarbShoppingCartComponent } from './decarb-shopping-cart/decarb-shopping-cart.component';


@Component({
  selector: 'app-decarb-journey',
  standalone: true,
  imports: [RouterOutlet, RouterModule,DecarbShoppingCartComponent],
  templateUrl: './decarb-journey.component.html',
  styleUrl: './decarb-journey.component.css'
})
export class DecarbJourneyComponent {
  title = 'decarbonization-journey';

    // Explicitly type the dropdown state as a record of strings to booleans
    isDropdownOpen: { [key: string]: boolean } = {
      dropdown1: false,
      dropdown2: false,
      dropdown3: false
    };
  
    // Toggle dropdown function
    toggleDropdown(dropdown: string) {
      this.isDropdownOpen[dropdown] = !this.isDropdownOpen[dropdown];
    }

}
