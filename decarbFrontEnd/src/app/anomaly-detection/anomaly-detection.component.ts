import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http'
import { catchError, tap } from 'rxjs/operators';
import { of } from 'rxjs';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-anomaly-detection',
  standalone: true,
  imports: [],
  templateUrl: './anomaly-detection.component.html',
  styleUrl: './anomaly-detection.component.css'
})
export class AnomalyDetectionComponent {
  title="anomaly-app"
  CompanyQuery:number = 0;
  YearQuery:number = 0;
  ScopeQuery:number = 0;
  SubCatQuery:number = 0.0;
  ResponseData:any;
  ResponseVector:any;

  objectKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  constructor(private http: HttpClient) {}

  sendRequestAnomaly(): void {
    const params = {
      comp: this.CompanyQuery,
      year: this.YearQuery,
      scope: this.ScopeQuery,
      subcat: this.SubCatQuery,
    };
    
    this.http
    .get('http://localhost:8000/yearly_steps/detect_anomalies/', { params })
    .pipe(
      tap((response) => {console.log('Response:', response);
      this.ResponseData=response;}),
      catchError((error) => {
        console.error('Error:', error);
        return of({ error: 'Request failed' }); // Return fallback or default response
      })
    )
    .subscribe();

}
sendRequestVector(): void {
 
  this.http
  .get('http://127.0.0.1:8000/yearly_steps/create-vector-table/')
  .pipe(
    tap((response) => {console.log('Response:', response);
    this.ResponseVector=response;}),
    catchError((error) => {
      console.error('Error:', error);
      return of({ error: 'Request failed' }); // Return fallback or default response
    })
  )
  .subscribe();

}

}
