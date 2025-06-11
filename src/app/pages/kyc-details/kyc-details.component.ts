import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-kyc-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './kyc-details.component.html',
  styleUrl: './kyc-details.component.css',
})
export class KycDetailsComponent implements OnInit {
  userId: string | null = null;
  user: any;

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.userId = this.route.snapshot.paramMap.get('id');

    // Replace this with real data fetch
    this.user = {
      id: this.userId,
      name: 'Rajesh Kannan',
      dob: '1980-10-15',
      pan: 'ABCDE1234F',
      aadhaar: '1234-5678-9012',
      status: 'Pending',
    };
  }

  goToAudioRecorder() {
    this.router.navigate(['/kyc-audio', this.userId]);
  }

  updateStatus(status: string) {
    // You can call backend API here
    this.user.status = status;
    alert(`KYC ${status}`);
  }
}
