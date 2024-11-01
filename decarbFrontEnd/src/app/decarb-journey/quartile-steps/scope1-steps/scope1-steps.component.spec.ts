import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Scope1StepsComponent } from './scope1-steps.component';

describe('Scope1StepsComponent', () => {
  let component: Scope1StepsComponent;
  let fixture: ComponentFixture<Scope1StepsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Scope1StepsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Scope1StepsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
