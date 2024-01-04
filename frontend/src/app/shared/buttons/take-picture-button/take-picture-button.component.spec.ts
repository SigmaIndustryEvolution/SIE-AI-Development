import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TakePictureButtonComponent } from './take-picture-button.component';

describe('TakePictureButtonComponent', () => {
  let component: TakePictureButtonComponent;
  let fixture: ComponentFixture<TakePictureButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TakePictureButtonComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TakePictureButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
