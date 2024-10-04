import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DecarbJourneyComponent } from './decarb-journey.component';

describe('DecarbJourneyComponent', () => {
  let component: DecarbJourneyComponent;
  let fixture: ComponentFixture<DecarbJourneyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DecarbJourneyComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DecarbJourneyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
