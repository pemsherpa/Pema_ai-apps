import { Component, OnInit } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Import FormsModule for ngModel
import { HttpClient } from '@angular/common/http';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-make-switch',
  templateUrl: './make-switch.component.html',
  styleUrls: ['./make-switch.component.css'],
  imports: [CommonModule, FormsModule, RouterOutlet], // Add FormsModule here
  standalone: true
})
export class MakeSwitchComponent {

  constructor(public location: Location) {}

}


