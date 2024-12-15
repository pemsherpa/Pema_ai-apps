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
  imports: [RouterOutlet, CommonModule, FormsModule, HttpClientModule],
  templateUrl: './anomaly-detection.component.html',
  styleUrl: './anomaly-detection.component.css'
})
export class AnomalyDetectionComponent {
  title="anomaly-app"
  CompanyQuery:number = 0;
  YearQuery:number = 0;
  ScopeQuery:number = 0;
  SubCatQuery:number = 0.0;
  //GasQuery:number =0.0
  ResponseDataIQR: any;
  ResponseDataCosine: any;
  ResponseVector: any;



  constructor(private httpClient: HttpClient) {}

  sendRequestIQR() {
    this.httpClient.get('http://127.0.0.1:8000/yearly_steps/detect-iqr-anomalies/', {
      params: {
        company: this.CompanyQuery,
        year: this.YearQuery,
        scope: this.ScopeQuery,
        subcategory: this.SubCatQuery
      }
    }).subscribe((response: any) => {
      if (response.status === 'success') {
        this.ResponseDataIQR = response.iqr_anomalies;
        console.log('IQR anomalies:', this.ResponseDataIQR);
      } else {
        console.error('Error fetching IQR anomalies:', response.message);
      }
    });
  }

 // Send request for Cosine anomalies
 sendRequestCosine() {
  this.httpClient.get('http://127.0.0.1:8000/yearly_steps/detect-cosine-anomalies/', {
    params: {
      company: this.CompanyQuery,
      year: this.YearQuery,
      scope: this.ScopeQuery,
      subcategory: this.SubCatQuery
    }
  }).subscribe((response: any) => {
    if (response.status === 'success') {
      this.ResponseDataCosine = response.cosine_anomalies;
      console.log('Cosine anomalies:', this.ResponseDataCosine);
    } else {
      console.error('Error fetching Cosine anomalies:', response.message);
    }
  });
}

sendRequestVector() {
  this.httpClient.get('http://127.0.0.1:8000/yearly_steps/create-vector-table/', {})
    .subscribe(
      (response: any) => {
        if (response.status === 'success') {
          this.ResponseVector = response;
          console.log('Vector table response:', this.ResponseVector);
        } else {
          this.ResponseVector = { error: 'Failed to fetch vector table: ' + response.message };
        }
      },
      (error) => {
        // Handle the error when the request fails
        this.ResponseVector = { error: 'An error occurred while fetching the vector table.' };
        console.error('Error fetching vector table:', error);
      }
    );
}

}



// sendRequestVector(): void {
 
//   this.httpClient
//   .get('http://127.0.0.1:8000/yearly_steps/create-vector-table/')
//   .pipe(
//     tap((response) => {console.log('Response:', response);
//     this.ResponseVector=response;}),
//     catchError((error) => {
//       console.error('Error:', error);
//       return of({ error: 'Request failed' }); // Return fallback or default response
//     })
//   )
//   .subscribe();

// }

// }
