import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CruComponent } from './cru.component';

describe('CruComponent', () => {
  let component: CruComponent;
  let fixture: ComponentFixture<CruComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CruComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CruComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
