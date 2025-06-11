import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-kyc-landing',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './kyc-landing.component.html',
  styleUrl: './kyc-landing.component.css',
})
export class KycLandingComponent {
  constructor(private router: Router) {}

  navigateTo(path: string) {
    this.router.navigate([path]);
  }
}
