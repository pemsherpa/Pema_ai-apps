import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter, ElementRef, AfterViewInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-scope2-step',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './scope2-steps.component.html',
  styleUrls: ['./scope2-steps.component.css']
})
export class Scope2StepsComponent implements AfterViewInit {
  @Input() stepData!: {
    title: string;
    description: string;
    cost_savings: number;
    co2_savings: number;
    transition_percentage: number;
    difficulty: number;
    isCompleted: boolean;
    recommenedProvider: any[];
    provider_name: any[];
    provider_description: string;
    phone_number: string;
    website_link: string;
  };

  @Input() totalSteps = 4;
  @Output() stepToggled = new EventEmitter<any>();
  @Output() makeSwitchClicked = new EventEmitter<string>();

  isExpanded = false;
  private lastKnownHeight = 0;

  constructor(private router: Router, private elementRef: ElementRef) { }

  handleClick(): void {
    //console.log('Step clicked, toggling completion and expansion...');
    this.toggleCompletion();
    this.toggleExpansion();
    //console.log("I am here",this.stepData.transition_percentage)
  }

  toggleCompletion(): void {
    this.stepData.isCompleted = !this.stepData.isCompleted;
    this.stepToggled.emit(this.stepData);
    //console.log('Step completion toggled:', this.stepData.isCompleted);
  }

  toggleExpansion(): void {
    this.isExpanded = !this.isExpanded;
    //console.log('Step expansion toggled:', this.isExpanded);
    setTimeout(() => {
      this.updateLineHeight();
    }, 50);
  }
  onMakeSwitchClick(stepData: any) {
    this.router.navigate(['/make-switch/renewable'], { state: { data: stepData } });
  }

  private updateLineHeight() {
    const currentCheckbox = this.elementRef.nativeElement.querySelector('.check-box-container');
    const stepContent = this.elementRef.nativeElement.querySelector('.step-content');
    const nextCheckbox = this.findNextCheckbox(currentCheckbox);
    
    if (currentCheckbox) {
      const currentRect = currentCheckbox.getBoundingClientRect();
      let distanceToNext = 0;
      let contentHeight = 0;
      if (nextCheckbox) {
        const nextRect = nextCheckbox.getBoundingClientRect();
        distanceToNext = nextRect.top - currentRect.bottom;
      }
      if (this.isExpanded && stepContent) {
        const contentRect = stepContent.getBoundingClientRect();
        contentHeight = contentRect.height;
      }
      this.lastKnownHeight = Math.max(distanceToNext, contentHeight);
    }
  }

  calculateLineHeight(): number {
    const currentCheckbox = this.elementRef.nativeElement.querySelector('.check-box-container');
    const stepContent = this.elementRef.nativeElement.querySelector('.step-content');
    const nextCheckbox = this.findNextCheckbox(currentCheckbox);
    
    if (currentCheckbox) {
      const currentRect = currentCheckbox.getBoundingClientRect();
      let height = 0;
      if (nextCheckbox) {
        const nextRect = nextCheckbox.getBoundingClientRect();
        height = nextRect.top - currentRect.bottom;
      }
      if (this.isExpanded && stepContent) {
        const contentRect = stepContent.getBoundingClientRect();
        const contentHeight = contentRect.height;
        height = Math.max(height, contentHeight);
      }
      return height + 22;
    }

    return 22;
  }

  private findNextCheckbox(currentCheckbox: Element): Element | null {
    const allCheckboxes = document.querySelectorAll('.check-box-container');
    let found = false;
    
    for (let i = 0; i < allCheckboxes.length; i++) {
      if (found) {
        return allCheckboxes[i];
      }
      if (allCheckboxes[i] === currentCheckbox) {
        found = true;
      }
    }
    return null;
  }

  ngAfterViewInit() {
    this.updateLineHeight();
    const resizeObserver = new ResizeObserver(() => {
      this.updateLineHeight();
    });
    
    const element = this.elementRef.nativeElement;
    resizeObserver.observe(element);
  }


  }
