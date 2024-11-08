import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassifymapComponent } from './classifymap.component';

describe('ClassifymapComponent', () => {
  let component: ClassifymapComponent;
  let fixture: ComponentFixture<ClassifymapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassifymapComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClassifymapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
