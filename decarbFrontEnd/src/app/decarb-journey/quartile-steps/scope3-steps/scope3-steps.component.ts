import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter, ElementRef } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

// Interfaces for different types of Scope3 data 
// Scope 3 data: Carpool, Flights, or CRU
interface BaseScope3Data {
  company_id: number;
  title: string;
  description: string;
  cost_savings: number;
  co2_savings: number;
  total_cost: number;
  total_emissions: number;
  transition: number;
  difficulty: number;
  isCompleted: boolean;
  type: 'flight' | 'commute' | 'recommendation';
}

interface FlightData extends BaseScope3Data {
  type: 'flight';
  stops: number;
}

interface CommuteMember {
  id: number;
  method: string;
  location: string;
  frequency: number;
  costPerKm: number;
  coords: [number, number];
  distance: number;
  emission: number;
  distanceFromFirm: number;
  cost: number;
  carpoolGroup: number;
}

interface CommuteGroup {
  group: number;
  members: CommuteMember[];
  message: string | null;
  savings: {
    money: number;
    emission: number;
    distance: number;
  };
}

interface CommuteData extends BaseScope3Data {
  type: 'commute';
  commuteData: CommuteGroup[];
}

interface Provider {
  name: string | null;
  company: string;
  details: string;
  location: string;
  phone: string;
  website: string;
  carbonSavings: number;
  costSavings: number;
  totalCost: number;
  renewablePercent: number | null;
}

interface RecommendationData extends BaseScope3Data {
  type: 'recommendation';
  recommendations: {
    plan: string;
    message: string;
    carbonSavings: number;
    costSavings: number;
    providers: Provider[];
    recommendedProvider: Provider;
  }[];
}

type Scope3StepData = FlightData | CommuteData | RecommendationData;

@Component({
  selector: 'app-scope3-step',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './scope3-steps.component.html',
  styleUrls: ['./scope3-steps.component.css']
})
export class Scope3StepsComponent {
  @Input() stepData!: Scope3StepData;
  @Input() totalSteps = 4;

  @Output() stepToggled = new EventEmitter<any>();
  @Output() makeSwitchClicked = new EventEmitter<string>();

  isExpanded = false;
  private lastKnownHeight = 0;

  constructor(private router: Router, private elementRef: ElementRef) { }

  handleClick(): void {
    console.log('Step clicked, toggling completion and expansion...');
    this.toggleCompletion();
    this.toggleExpansion();
    console.log("I am here", this.stepData.transition);
  }

  toggleCompletion(): void {
    this.stepData.isCompleted = !this.stepData.isCompleted;
    this.stepToggled.emit(this.stepData);
    console.log('Step completion toggled:', this.stepData.isCompleted);
  }

  toggleExpansion(): void {
    this.isExpanded = !this.isExpanded;
    console.log('Step expansion toggled:', this.isExpanded);

    setTimeout(() => {
      this.updateLineHeight();
    }, 50);
  }

  onMakeSwitchClick(stepData: Scope3StepData) {
    let routerPath = ''

    switch (stepData.type) {
      case 'commute':
        routerPath = '/make-switch/carpool'
        break
      case 'flight':
        routerPath = '/make-switch/flights1'
        break
      case 'recommendation':
        routerPath = '/make-switch/cru'
        break
      default:
        routerPath = '/make-switch'
        break
    }
    this.router.navigate([routerPath], { state: { data: stepData } });
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


  // Helper methods to check type
  isFlightStep(): boolean {
    return this.stepData.type === 'flight';
  }

  isCommuteStep(): boolean {
    return this.stepData.type === 'commute';
  }

  isRecommendationStep(): boolean {
    return this.stepData.type === 'recommendation';
  }
}