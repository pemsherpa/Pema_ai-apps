import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DecarbShoppingCartComponent } from './decarb-shopping-cart.component';

describe('DecarbShoppingCartComponent', () => {
  let component: DecarbShoppingCartComponent;
  let fixture: ComponentFixture<DecarbShoppingCartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DecarbShoppingCartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DecarbShoppingCartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
