import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-scope3-step',
  standalone: true,
  imports:[CommonModule],
  templateUrl: './scope3-steps.component.html',
  styleUrl: './scope3-steps.component.css'
})
export class Scope3StepsComponent {
  @Input() stepData!: {
    title: string;
    description: string;
    costSavings: number;
    co2Savings: number;
    transition: number;
    isCompleted: boolean;
    providerInfo?: string;  // Add providerInfo here, with optional typing if needed
  };
  @Output() stepToggled = new EventEmitter<void>();

  toggleCompletion(): void {
    this.stepData.isCompleted = !this.stepData.isCompleted;
    this.stepToggled.emit();
  }
}
