import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-scope2-step',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './scope2-steps.component.html',
})
export class Scope2StepsComponent {
  @Input() stepData!: { 
    title: string; 
    description: string; 
    costSavings: number; 
    co2Savings: number; 
    transition: number; 
    isCompleted: boolean; 
    providerInfo: any[] 
  };
  
  @Output() stepToggled = new EventEmitter<void>();

  isExpanded = false; // Track dropdown expansion state

  handleClick() {
    this.toggleCompletion();
    this.toggleExpansion();
  }

  toggleCompletion(): void {
    this.stepData.isCompleted = !this.stepData.isCompleted;
    this.stepToggled.emit();
    console.log(this.stepData);
  }

  toggleExpansion(): void {
    this.isExpanded = !this.isExpanded; // Toggle the dropdown state
  }
}




