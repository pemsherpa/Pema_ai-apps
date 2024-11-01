import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Scope3StepsComponent } from './scope3-steps.component';

describe('Scope3StepsComponent', () => {
  let component: Scope3StepsComponent;
  let fixture: ComponentFixture<Scope3StepsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Scope3StepsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Scope3StepsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
