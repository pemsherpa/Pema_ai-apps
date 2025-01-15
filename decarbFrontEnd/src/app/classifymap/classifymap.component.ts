import { Component, AfterViewInit, OnInit, ViewChild, ChangeDetectorRef, ElementRef } from '@angular/core';
import { ViewChildren, QueryList } from '@angular/core';
import { GoogleMap, GoogleMapsModule, MapInfoWindow, MapMarker } from '@angular/google-maps';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { ActionObject, Company } from '../company.model';
import { companies } from '../companies';

@Component({
  standalone: true,
  imports: [
    CommonModule,
    GoogleMap,
    GoogleMapsModule,
    MatCardModule,
    MatTableModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatSortModule,
    MatButtonModule,
    MapMarker,
  ],
  selector: 'app-map',
  templateUrl: './classifymap.component.html',
  styleUrls: ['./classifymap.component.scss'],
})
export class ClassifymapComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MapInfoWindow) infoWindow: MapInfoWindow | undefined;
  @ViewChild('googleMapContainer', { static: false }) googleMapContainer!: GoogleMap;
  @ViewChildren(MapMarker) mapMarkers!: QueryList<MapMarker>;

  center!: google.maps.LatLngLiteral;
  zoom = 7;
  companies: Company[] = companies;
  selectedCompany: Company | null = null;
  customIcon!: google.maps.Icon;

  displayedColumns: string[] = ['name', 'description', 'date', 'percentageComplete'];
  dataSource = new MatTableDataSource<ActionObject>([]);

  markers = [
    {
      position: { lat: 37.7749, lng: -122.4194 },
      label: { text: '' },
      title: 'Adidas',
      icon: {
        url: 'assets/Adidas-logo.png',
        scaledSize: new google.maps.Size(40, 40),
      },
      info: companies[0], 
    },
    {
      position: { lat: 36.3382, lng: -121.8863 },
      label: { text: '' },
      title: 'Colgate',
      icon: {
        url: 'assets/Colgate-logo.png',
        scaledSize: new google.maps.Size(40, 40),
      },
      info: companies[1], 
    },
    {
      position: { lat: 37.4749, lng: -120.4194 },
      label: { text: '' },
      title: 'CVS Health',
      icon: {
        url: 'assets/CVS_Health-logo.png',
        scaledSize: new google.maps.Size(40, 40),
      },
      info: companies[2], 
    },
    {
      position: { lat: 36.4749, lng: -118.4194 },
      label: { text: '' },
      title: 'AG-Barr',
      icon: {
        url: 'assets/AG-Barr-logo.png',
        scaledSize: new google.maps.Size(40, 40),
      },
      info: companies[3], 
    },
    {
      position: { lat: 38.4749, lng: -119.4194 },
      label: { text: '' },
      title: 'Davita',
      icon: {
        url: 'assets/Davita-logo.png',
        scaledSize: new google.maps.Size(40, 40),
      },
      info: companies[4], 
    }
  ];

  selectedInfo: string = '';

  constructor(private changeDetectorRef: ChangeDetectorRef, private router: Router) {
    console.log('MapComponent Initialized');
  }

  ngOnInit(): void {
    this.waitForGoogleMapsApi().then(() => {
      this.center = { lat: 37.7749, lng: -122.4194 }; // San Francisco
    });
    if (this.companies.length > 0) {
      this.selectedCompany = this.companies[0];
      this.dataSource.data = this.selectedCompany.actions;
      this.changeDetectorRef.detectChanges();
      this.initTable(); 
    }
  }

  

  map!: google.maps.Map;

  ngAfterViewInit(): void {
    if (this.googleMapContainer) {
      this.map = this.googleMapContainer.googleMap!;
    } else {
      console.error('Map element is undefined in ngAfterViewInit');
    }
  }

  initTable(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  async waitForGoogleMapsApi(): Promise<void> {
    return new Promise((resolve) => {
      const interval = setInterval(() => {
        if (typeof google !== 'undefined' && google.maps) {
          clearInterval(interval);
          resolve();
        }
      }, 100); 
    });
  }

  openInfoWindow(markerRef: MapMarker, companyInfo: Company) {
    this.selectedCompany = companyInfo;
    this.dataSource.data = companyInfo.actions;
  
    this.changeDetectorRef.detectChanges(); // Trigger change detection
    this.dataSource.paginator = this.paginator; 
    this.dataSource.sort = this.sort; 
  
    if (this.infoWindow && markerRef) {
      this.infoWindow.open(markerRef);
    } else {
      console.error('MapMarker reference is missing');
    }
  }

  selectCompany(companyName: string): void {
    const selectedMarkerData = this.markers.find(marker => marker.info.name === companyName);

    if (selectedMarkerData) {
      const selectedMarker = this.mapMarkers.find((marker: MapMarker) => {
        const position = marker.getPosition();
        return position?.lat() === selectedMarkerData.position.lat && position?.lng() === selectedMarkerData.position.lng;
      });

      if (selectedMarker) {
        this.openInfoWindow(selectedMarker, selectedMarkerData.info);
      } else {
        console.error(`MapMarker instance not found for company: ${companyName}`);
      }
    } else {
      console.error(`Marker data not found for company: ${companyName}`);
    }
  }

  goBack() {
    this.router.navigate(['/decarbonization']);
  }
}
