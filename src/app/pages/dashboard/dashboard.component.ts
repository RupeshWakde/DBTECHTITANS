import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  styleUrl : './dashboard.component.css',
  imports: [CommonModule],  
  templateUrl: "./dashboard.component.html"
})
export class DashboardComponent {
  constructor(private auth: AuthService, private router: Router) {}
  users = [
    { name: 'Alice Johnson', email: 'alice@example.com', status: 'Active' },
    { name: 'Bob Smith', email: 'bob@example.com', status: 'Inactive' },
    { name: 'Charlie Brown', email: 'charlie@example.com', status: 'Active' },
  ];

  logout() {
    this.auth.logout();
  }
}
