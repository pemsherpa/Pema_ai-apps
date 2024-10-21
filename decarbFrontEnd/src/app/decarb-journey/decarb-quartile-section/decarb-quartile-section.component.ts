
import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'cs-decarb-quartile-section',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './decarb-quartile-section.component.html',
  styleUrls: ['./decarb-quartile-section.component.css'],
})
export class DecarbQuartileSectionComponent {
  @Output() itemChecked = new EventEmitter<{
    name: string; 
    costSavings: number; 
    co2Savings: number; 
    transition: number; 
    isChecked: boolean;
  }>();

  isDropdownOpen: { [key: string]: boolean } = {};

  quartileData = [
    {
      title: 'First Quartile',
      scopeDescription: 'Following steps focus on reducing scope 1 emissions.',
      dropdowns: [
        { title: 'Change Electricity Provider', content: 'Switch to a provider offering more renewable energy.', costSavings: 6000, co2Savings: -100, transition: 50, isCompleted: false },
        { title: 'Reduce First Class Travel', content: 'Switching from first class to business class reduces emissions.', costSavings: 2500, co2Savings: -45, transition: 25, isCompleted: false },
        { title: 'Introduce Fuel-Efficient Vehicles', content: 'Implement fuel-efficient vehicles to cut emissions.', costSavings: 5000, co2Savings: -75, transition: 30, isCompleted: false }
      ]
    },
    // ... other quartiles
  ];
  quartileSelected: boolean[] = [false, false, false, false];
  toggleDropdown(dropdownId: string): void {
    this.isDropdownOpen[dropdownId] = !this.isDropdownOpen[dropdownId];
  }

  toggleCompletion(quartileIndex: number, dropdownIndex: number): void {
    const selectedDropdown = this.quartileData[quartileIndex].dropdowns[dropdownIndex];
    selectedDropdown.isCompleted = !selectedDropdown.isCompleted;

    // Emit the name of the task and its completion state along with savings data
    this.itemChecked.emit({
      name: selectedDropdown.title,
      costSavings: selectedDropdown.costSavings,
      co2Savings: selectedDropdown.co2Savings,
      transition: selectedDropdown.transition,
      isChecked: selectedDropdown.isCompleted
    });
  }
  toggleQuartileButton(index: number): void {
    this.quartileSelected[index] = !this.quartileSelected[index];
  }
}


