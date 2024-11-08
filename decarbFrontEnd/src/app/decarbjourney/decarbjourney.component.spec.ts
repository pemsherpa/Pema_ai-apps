import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DecarbjourneyComponent } from './decarbjourney.component';

describe('DecarbjourneyComponent', () => {
  let component: DecarbjourneyComponent;
  let fixture: ComponentFixture<DecarbjourneyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DecarbjourneyComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DecarbjourneyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
