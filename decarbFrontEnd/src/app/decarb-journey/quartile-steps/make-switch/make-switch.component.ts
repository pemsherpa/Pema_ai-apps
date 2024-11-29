import { Component, OnInit } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Import FormsModule for ngModel

@Component({
  selector: 'app-make-switch',
  templateUrl: './make-switch.component.html',
  styleUrls: ['./make-switch.component.css'],
  imports: [CommonModule, FormsModule], // Add FormsModule here
  standalone: true
})
export class MakeSwitchComponent implements OnInit {
  stepData: any;
  userDetails = {
    name: '',
    email: '',
    dob: '',
    phone: '',
    isInterested: false,
    company:'',
    currentProvider: '',
    currentPlan: '',
    currentCost: '',
    currentEmissions: ''
  };

  constructor(public location: Location) {}

  ngOnInit(): void {
    // Retrieve the passed data from navigation state
    const state = history.state;
    this.stepData = state.data || null;
  }

  onSubmit() {
    console.log('User Details Submitted:', this.userDetails);
    alert('Thank you! Your details have been submitted.');
  }
}


