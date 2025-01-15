import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Flights1Component } from './flights1.component';

describe('Flights1Component', () => {
  let component: Flights1Component;
  let fixture: ComponentFixture<Flights1Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Flights1Component]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Flights1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
