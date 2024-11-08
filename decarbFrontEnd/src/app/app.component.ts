import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { DecarbJourneyComponent } from './decarb-journey/decarb-journey.component';
import { DecarbjourneyComponent } from './decarbjourney/decarbjourney.component';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { MatPaginatorModule } from '@angular/material/paginator';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [RouterOutlet, RouterModule, DecarbJourneyComponent,DecarbjourneyComponent, FormsModule, CommonModule, MatPaginatorModule]
})
export class AppComponent {
  title = 'decarbonization-journey';


}


