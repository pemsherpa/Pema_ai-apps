import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Scope2StepsComponent } from './scope2-steps.component';

describe('Scope2StepsComponent', () => {
  let component: Scope2StepsComponent;
  let fixture: ComponentFixture<Scope2StepsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Scope2StepsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Scope2StepsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
