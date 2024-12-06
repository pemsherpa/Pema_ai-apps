import { Routes } from '@angular/router';
import { AppComponent } from './app.component';  // Ensure AppComponent is imported
import { DecarbjourneyComponent } from './decarbjourney/decarbjourney.component';
import { ClassifymapComponent } from './classifymap/classifymap.component';
import { DecarbJourneyComponent } from './decarb-journey/decarb-journey.component';
import { MakeSwitchComponent } from './decarb-journey/quartile-steps/make-switch/make-switch.component';
import { AnomalyDetectionComponent } from './anomaly-detection/anomaly-detection.component';


const routes: Routes = [
  { path: '', redirectTo: 'decarbonization', pathMatch: 'full' },
  {
    path: 'decarbonization',
    component: DecarbjourneyComponent,
    title: 'Decarb Journey'
}, 
{
    path: 'map',
    component: ClassifymapComponent,
    title: 'Classify Map'
},
{
  path: 'journey',
  component: DecarbJourneyComponent,
  title: 'Decarb-journey'
},
{
  path: 'make-switch',
  component: MakeSwitchComponent,
  title: 'Make-the-switch'
},{
  path:'anomaly-detection',
  component:AnomalyDetectionComponent,
  title:'Detect-anomalies'
}

]; 
export default routes;



