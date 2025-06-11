import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatIconModule, MatIconRegistry  } from '@angular/material/icon';

@Component({
  selector: 'app-kyc-success',
  standalone: true,
  imports: [CommonModule, MatIconModule],
  templateUrl: './kyc-success.component.html',
  styleUrls: ['./kyc-success.component.css']
})
export class KycSuccessComponent {
  constructor(private router: Router) {}

  goBack() {
   this.router.navigate(['/kyc-dashboard']);
  }
}
