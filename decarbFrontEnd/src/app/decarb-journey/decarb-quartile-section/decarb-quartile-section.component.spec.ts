import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DecarbQuartileSectionComponent } from './decarb-quartile-section.component';

describe('DecarbQuartileSectionComponent', () => {
  let component: DecarbQuartileSectionComponent;
  let fixture: ComponentFixture<DecarbQuartileSectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DecarbQuartileSectionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DecarbQuartileSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
