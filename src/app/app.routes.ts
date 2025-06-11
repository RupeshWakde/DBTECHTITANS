import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { KycDashboardComponent } from './pages/kyc-dashboard/kyc-dashboard.component';
import { KycAudioRecorderComponent } from './pages/kyc-audio-recorder/kyc-audio-recorder.component';
import { KycDetailsComponent } from './pages/kyc-details/kyc-details.component';
import { KycVideoRecorderComponent } from './pages/kyc-video-recorder/kyc-video-recorder.component';
import { KycUserUploadComponent } from './pages/kyc-user-upload/kyc-user-upload.component';
import { KycAdminUploadComponent } from './pages/kyc-admin-upload/kyc-admin-upload.component';
import { VideoCaptureComponent } from './pages/kyc-video-capture/video-capture.component';
import { KycSuccessComponent } from './pages/kyc-success.component/kyc-success.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'kyc-dashboard', component: KycDashboardComponent },
  { path: 'kyc-audio', component: KycAudioRecorderComponent },
  { path: 'user-upload', component: KycUserUploadComponent },
  { path: 'admin-upload', component: KycAdminUploadComponent },
  { path: 'kyc-details/:id', component: KycDetailsComponent },
  { path: 'kyc-video', component: KycVideoRecorderComponent },
  { path: 'kyc-video-capture', component: VideoCaptureComponent },
  { path: 'kyc-success', component: KycSuccessComponent },
];
