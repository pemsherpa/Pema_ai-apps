import { Routes } from '@angular/router';
import { AppComponent } from './app.component';  // Ensure AppComponent is imported
import { DecarbjourneyComponent } from './decarbjourney/decarbjourney.component';
import { ClassifymapComponent } from './classifymap/classifymap.component';
import { DecarbJourneyComponent } from './decarb-journey/decarb-journey.component';
import { MakeSwitchComponent } from './decarb-journey/quartile-steps/make-switch/make-switch.component';
import { RenewableSwitchComponent } from './decarb-journey/quartile-steps/make-switch/renewable-switch/renewable-switch.component';
import { AnomalyDetectionComponent } from './anomaly-detection/anomaly-detection.component';
import { CarpoolComponent } from './decarb-journey/quartile-steps/make-switch/carpool/carpool.component';
import { CruComponent } from './decarb-journey/quartile-steps/make-switch/cru/cru.component';
import { Flights1Component } from './decarb-journey/quartile-steps/make-switch/flights1/flights1.component';


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
  children: [
    {path: 'renewable', component: RenewableSwitchComponent},
    {path: 'carpool', component: CarpoolComponent},
    {path: 'cru', component: CruComponent},
    {path: 'flights1', component: Flights1Component}
    //{ path: '', redirectTo: 'renewable', pathMatch: 'full' }
  ],
  title: 'Make-the-switch'
},{
  path:'anomaly-detection',
  component:AnomalyDetectionComponent,
  title:'Detect-anomalies'
}

]; 
export default routes;



