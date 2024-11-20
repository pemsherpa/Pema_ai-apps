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
    return this.stepData.isCompleted ? 60 : 0;
  }
}
