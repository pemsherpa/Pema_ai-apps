import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RenewableSwitchComponent } from './renewable-switch.component';

describe('RenewableSwitchComponent', () => {
  let component: RenewableSwitchComponent;
  let fixture: ComponentFixture<RenewableSwitchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RenewableSwitchComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RenewableSwitchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
