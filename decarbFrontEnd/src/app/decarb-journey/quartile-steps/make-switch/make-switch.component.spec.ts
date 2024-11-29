import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MakeSwitchComponent } from './make-switch.component';

describe('MakeSwitchComponent', () => {
  let component: MakeSwitchComponent;
  let fixture: ComponentFixture<MakeSwitchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MakeSwitchComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MakeSwitchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
