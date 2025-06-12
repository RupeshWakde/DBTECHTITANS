import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-login',
  standalone: true,
  styleUrl: './login.component.css',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
  ],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  username = '';
  password = '';
  loginFailed = false;

  constructor(private auth: AuthService, private router: Router) {}

  onLogin() {
    if (this.auth.login(this.username, this.password)) {
      this.router.navigate(['/kyc-dashboard']);
    } else {
      this.router.navigate(['/user-upload']);
      //  this.loginFailed = true;
    }
  }
}
