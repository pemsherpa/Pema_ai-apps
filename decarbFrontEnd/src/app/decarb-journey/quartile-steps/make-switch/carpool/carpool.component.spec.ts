import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CarpoolComponent } from './carpool.component';

describe('CarpoolComponent', () => {
  let component: CarpoolComponent;
  let fixture: ComponentFixture<CarpoolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CarpoolComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CarpoolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
