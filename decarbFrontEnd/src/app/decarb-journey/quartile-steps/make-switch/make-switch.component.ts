import { Component, OnInit } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Import FormsModule for ngModel
import { HttpClient } from '@angular/common/http';

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
  };
  currentDetails = {
    currentProvider: '',
    currentPlan: '',
    currentCost: '',
    currentEmissions: ''
  };
  constructor(private http: HttpClient,public location: Location) {}

  ngOnInit(): void {
    // Retrieve the passed data from navigation state
    const state = history.state;
    this.stepData = state.data || null;

    this.http.get<any>('assets/yearly_quarterly_steps.json').subscribe(data => {
      // Assign the current details from the fetched data
      if (data && data.cs_backend_data.current_details) {
        this.currentDetails = {
          currentProvider: data.cs_backend_data.current_details.current_provider,
          currentPlan: data.cs_backend_data.current_details.current_plan,
          currentCost: data.cs_backend_data.current_details.current_cost,
          currentEmissions: data.cs_backend_data.current_details.current_emissions
        };
        
      }
    });
}


  onSubmit() {
    console.log('User Details Submitted:', this.userDetails);
    alert('Thank you! Your details have been submitted.');
  }
}


