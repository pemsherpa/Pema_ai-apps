import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet } from '@angular/router';
import { DecarbShoppingCartComponent } from './decarb-shopping-cart/decarb-shopping-cart.component';

@Component({
  selector: 'app-decarb-journey',
  standalone: true,
  imports: [RouterOutlet, RouterModule,DecarbShoppingCartComponent, CommonModule],
  templateUrl: './decarb-journey.component.html',
  styleUrl: './decarb-journey.component.css'
})
export class DecarbJourneyComponent {
  title = 'decarbonization-journey';

  isDropdownOpen: { [key: string]: boolean } = {};

  // Define the quartile data with unique dropdowns for each quartile
  quartileData = [
    {
      title: 'First Quartile',
      scopeDescription: 'Following steps focus on reducing scope 1 emissions.',
      dropdowns: [
        { title: 'Change Electricity Provider', content: 'Switch to a provider offering more renewable energy.' },
        { title: 'Reduce First Class Travel', content: 'Switching from first class to business class reduces emissions.' },
        { title: 'Introduce Fuel-Efficient Vehicles', content: 'Implement fuel-efficient vehicles to cut emissions.' }
      ]
    },
    {
      title: 'Second Quartile',
      scopeDescription: 'Following steps focus on reducing scope 2 emissions.',
      dropdowns: [
        { title: 'Engage in Sustainability Initiatives', content: 'Involve employees in sustainability programs.' },
        { title: 'Implement Carbon Capture', content: 'Deploy carbon capture technologies to reduce emissions.' },
        { title: 'Introduce Hybrid Vehicles', content: 'Consider introducing hybrid vehicles for your fleet.' }
      ]
    },
    {
      title: 'Third Quartile',
      scopeDescription: 'Following steps focus on reducing scope 3 emissions.',
      dropdowns: [
        { title: 'Carbon Offsetting', content: 'Offset emissions through certified carbon credits.' },
        { title: 'Optimize Supply Chain', content: 'Reduce emissions by optimizing supply chain processes.' },
        { title: 'Carbon Capture and Storage', content: 'Invest in carbon capture and storage technologies.' }
      ]
    }
  ];

  // Function to toggle dropdown visibility
  toggleDropdown(dropdownId: string): void {
    this.isDropdownOpen[dropdownId] = !this.isDropdownOpen[dropdownId];
  }

}
