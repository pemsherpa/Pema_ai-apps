import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { DecarbJourneyComponent } from './decarb-journey/decarb-journey.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  imports: [RouterOutlet, RouterModule, DecarbJourneyComponent]
})
export class AppComponent {
  title = 'decarbonization-journey';


}


