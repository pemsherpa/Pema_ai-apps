import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-scope3-step',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './scope3-steps.component.html',
  styleUrls: ['./scope3-steps.component.css']
})
export class Scope3StepsComponent {
  @Input() stepData!: { 
    title: string; 
    description: string; 
    costSavings: number; 
    co2Savings: number; 
    transition: number; 
    isCompleted: boolean; 
    providerInfo: any[]; 
  };

  @Input() totalSteps=4;

  @Output() stepToggled = new EventEmitter<void>();

  isExpanded = false;

  handleClick(): void {
    console.log('Step clicked, toggling completion and expansion...');
    this.toggleCompletion();
    this.toggleExpansion();
  }

  toggleCompletion(): void {
    this.stepData.isCompleted = !this.stepData.isCompleted;
    this.stepToggled.emit();
    console.log('Step completion toggled:', this.stepData.isCompleted);
  }

  toggleExpansion(): void {
    this.isExpanded = !this.isExpanded;
    console.log('Step expansion toggled:', this.isExpanded);
  }


  calculateLineHeight(): number {
    return this.isExpanded ? this.calculateDynamicHeight() : 0;
  }

  calculateDynamicHeight(): number {
    // Base height for the dropdown (e.g., padding, borders)
    const baseHeight = 100;
    const new_scope_height=90;

    // Additional height based on content, e.g., 100px per provider item
    const providerHeight = this.stepData.providerInfo?.length * 175 || 0;
    console.log("NUmber of steps",this.stepData.providerInfo?.length)
    console.log(providerHeight)

    // Additional height for static sections like cost/CO2 savings
    const additionalHeight = this.stepData.costSavings || this.stepData.co2Savings ? 75 : 0;
    console.log("Adiidtin",additionalHeight)

    return baseHeight + providerHeight + additionalHeight+new_scope_height;
  }
}
