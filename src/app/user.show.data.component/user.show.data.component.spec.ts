import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserShowDataComponent } from './user.show.data.component';

describe('UserShowDataComponent', () => {
  let component: UserShowDataComponent;
  let fixture: ComponentFixture<UserShowDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserShowDataComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserShowDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
