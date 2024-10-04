import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [RouterOutlet, RouterModule]
})
export class AppComponent {
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


