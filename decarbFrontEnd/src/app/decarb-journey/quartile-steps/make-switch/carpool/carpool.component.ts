import { Component, AfterViewInit, OnInit, ViewChild, ChangeDetectorRef, ElementRef } from '@angular/core';
import { ViewChildren, QueryList } from '@angular/core';
import { GoogleMap, GoogleMapsModule, MapInfoWindow, MapMarker } from '@angular/google-maps';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { CommonModule, Location } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommuteRec, Groups } from '../../../../groups.model';

@Component({
  selector: 'app-carpool',
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
  templateUrl: './carpool.component.html',
  styleUrl: './carpool.component.css'
})
export class CarpoolComponent implements OnInit, AfterViewInit {

  constructor(
    private http: HttpClient,
    public location: Location,
    private changeDetectorRef: ChangeDetectorRef,
    private router: Router) {
    console.log('Map Componenet Initialized')
  }

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MapInfoWindow) infoWindow: MapInfoWindow | undefined;
  @ViewChild('googleMapContainer', { static: false }) googleMapContainer!: GoogleMap;
  @ViewChildren(MapMarker) mapMarkers!: QueryList<MapMarker>;

  stepData: any;
  step_groups: Groups[] = [];
  groups: Groups[] = [];
  markers: any[] = [];
  selectedMarker: any = null

  center!: google.maps.LatLngLiteral
  zoom = 14;
  selectedGroup: Groups | null = null;
  selectedGroupMark: any;
  customIcon!: google.maps.Icon;

  displayedColumns: string[] = ['GroupNo', 'Location', 'MembersCount', 'Frequency', 'Distance', 'MilesSaved', 'MoneySaved', 'EmissionsSaved']
  dataSource = new MatTableDataSource<any>([])

  selectedInfo: string = ''



  map!: google.maps.Map

  ngOnInit(): void {
    const state = history.state;
    this.stepData = state.data || null;

    console.log(this.stepData);

    if (this.stepData && this.stepData.commuteData) {
      this.step_groups = this.stepData.commuteData
      this.groups = [...this.step_groups]
      //console.log("Showing groups: ", this.groups)
      this.createMarkers(this.groups)
    } else {
      console.error("Failed to fetch groups")
    }

    const flattenedData = this.flattenStepData(this.stepData)
      console.log("flattedned data: ", flattenedData)
      this.dataSource.data = flattenedData;
      console.log("data source: ", this.dataSource.data)
      this.initTable();

    this.waitForGoogleMapsApi().then(() => {
      this.center = { lat: this.stepData.commuteData[0].members[0].coords[0], lng: this.stepData.commuteData[0].members[0].coords[1] }
    })
    if (this.groups.length > 0) {


      this.selectedGroupMark = this.groups[0];
      console.log("Selected group mark: ", this.stepData)
      this.changeDetectorRef.detectChanges();
      
    }

    console.log("markers: ", this.markers)

  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;

    if (this.googleMapContainer) {
      this.map = this.googleMapContainer.googleMap!;
    } else {
      console.error('Map element is undefined in ngAfterViewInit');
    }
  }

  flattenStepData(stepData: any[]): any[] {
    const commuteData = this.stepData.commuteData

    const flattedData = commuteData.map((group: { group: any; members: any[]; distance_saving: any; money_saving: any; emission_saving: any; }) => ({
      group: group.group,
      distance: Math.max(...group.members.map(member => member.distanceFromFrim)),
      frequency: Math.max(...group.members.map(member => member.frequency)),
      membersCount: group.members.length,
      location: group.members[0]?.location,
      milesSaved: group.distance_saving,
      moneySaved: group.money_saving,
      emissionSaved: group.emission_saving
    }))
    return flattedData
  }

  createMarkers(commuteData: any[]): void {
    this.markers = []
    const posTracker: { [key: string]: number } = {}

    commuteData.forEach((group: any, index: number) => {
      if (group.members && group.members.length > 0) {
        const lat_long = group.members[0].coords

        const posKey = `${lat_long[0].toFixed(6)},${lat_long[1].toFixed(6)}`;
        let latOffset = 0
        let longOffset = 0

        if (posTracker[posKey]) {
          latOffset =(posTracker[posKey] * 0.0001)
          longOffset =(posTracker[posKey] * 0.001)
          posTracker[posKey]++
        } else {
          posTracker[posKey] = 1
        }

        const newLat = lat_long[0] + latOffset
        const newLong = lat_long[1] + longOffset

        const label = group.members.length ? group.members.length.toString() : '0';
        const customIcon = this.generateIcons(label)
        const marker = {
          position: { lat: newLat, lng: newLong },
          icon: customIcon,
          title: group.group.toString(),
          noOfMembers: group.members.length,
          groupInfo: group,
        }
        this.markers.push(marker)
      }
    })

    // console.log("markers: ",this.markers)
  }

  generateIcons(label: string): google.maps.Icon {
    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    const size = 50
    const borderWidth = 2
    const circleRadius = (size-borderWidth)/2;

    if (!context) {
      console.error("Failed to get canvas context");
      return { url: '', scaledSize: new google.maps.Size(0, 0) };
  }

    canvas.width = size
    canvas.height = size

    context.clearRect(0, 0, size, size)

    // white background
    context.beginPath()
    context.fillStyle = 'white'
    context.arc(size/2, size/2, circleRadius, 0, 2 * Math.PI)
    context.fill()

    // border style
    context.strokeStyle = '#6739E9'
    context.lineWidth = 2
    context.stroke()
    
    // number of members label
    context.fillStyle = '#6739E9'
    context.font = 'bold 14px Karla'
    context.textAlign = 'center'
    context.textBaseline = 'middle'
    context.fillText(`${label}`, size/2, size/2)

    return {
      url: canvas.toDataURL(),
      scaledSize: new google.maps.Size(size, size)
    }
  }

  async waitForGoogleMapsApi(): Promise<void> {
    return new Promise((resolve) => {
      const interval = setInterval(() => {
        if (typeof google !== 'undefined' && google.maps) {
          clearInterval(interval)
          resolve()
        }
      }, 100)
    })
  }

  initTable(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  selectGroup(groupNumber: number): void {
    const selectedMarkerData = this.markers.find(marker => marker.title === groupNumber.toString());

    if (selectedMarkerData) {
      console.log('selected marker data: ', selectedMarkerData)
      const selectedMarker = this.mapMarkers.find((marker: MapMarker) => {
        const position = marker.getPosition();
        return position?.lat() === selectedMarkerData.position.lat && position?.lng() === selectedMarkerData.position.lng;
      });

      if (selectedMarker) {
        // console.log("SelectedMarker: ", selectedMarker)
        //console.log("marker data: ", selectedMarkerData.groupInfo)
        this.openInfoWindow(selectedMarker, selectedMarkerData.groupInfo);
      } else {
        console.error(`MapMarker instance not found for group: ${groupNumber}`);
      }
    } else {
      console.error(`Marker data not found for group: ${groupNumber}`);
    }
  }


  openInfoWindow(markerRef: MapMarker, groupInfo: Groups) {
    this.selectedGroupMark = groupInfo;

    //console.log(this.selectedGroupMark)
    // this.dataSource.data = groupInfo.commute_rec;

    this.changeDetectorRef.detectChanges(); // Trigger change detection
    

    if (this.infoWindow && markerRef) {
      this.infoWindow.open(markerRef);
    } else {
      console.error('MapMarker reference is missing');
    }
  }


  goBack() {
    this.router.navigate(['/decarbonization']);
  }
}
