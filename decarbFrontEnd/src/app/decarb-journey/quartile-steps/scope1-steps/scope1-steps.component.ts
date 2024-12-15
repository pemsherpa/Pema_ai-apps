import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-scope1-step',
  standalone: true,
  imports: [CommonModule, RouterModule], // Include RouterModule here
  templateUrl: './scope1-steps.component.html',
  styleUrls: ['./scope1-steps.component.css']
})
export class Scope1StepsComponent {
  @Input() stepData!: { 
    title: string; 
    description: string; 
    cost_savings: number; 
    co2_savings: number; 
    transition: number; 
    isCompleted: boolean; 
    providerInfo: any[] 
  };
  
  @Output() stepToggled = new EventEmitter<void>();
  constructor(private router: Router) {}

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
  onMakeSwitchClick(stepData: any) {
    this.router.navigate(['/make-switch'], { state: { data: stepData } });
  }
}
