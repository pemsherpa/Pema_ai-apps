import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-scope1-step',
  standalone: true,
  imports:[CommonModule],
  templateUrl: './scope1-steps.component.html',
})
export class Scope1StepsComponent {
  @Input() stepData!: { title: string; description: string; costSavings: number; co2Savings: number; transition: number; isCompleted: boolean, providerInfo: any[] };
  @Output() stepToggled = new EventEmitter<void>();

  toggleCompletion(): void {
    this.stepData.isCompleted = !this.stepData.isCompleted;
    this.stepToggled.emit();
    console.log("Scope Data"+this.stepData)
  }
}

