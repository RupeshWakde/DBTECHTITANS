import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-kyc-admin-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  styleUrl: './kyc-user-upload.component.css',
  templateUrl: './kyc-user-upload.component.html',
})
export class KycUserUploadComponent {
  form: any = {
    name: '',
    rm: '',
    pan: null,
    aadhaar: null,
    audio: null,
    video: null,
  };
  isPanCardSelected = false;
  isAadhardSelected = false;

  imageFile: File | null = null;
  pdfFile: File | null = null;
  videoFile: File | null = null;

  submitted = false;
  constructor(private router: Router, private http: HttpClient) {}

  handleFile(event: any, type: string) {
    const file = event.target.files[0];
    if (file) {
      this.form[type] = file;
    }
  }

  uploadVideo() {
    this.router.navigate(['/kyc-video']);
  }

  isFormValid(): boolean {
    return (
      this.form.name.trim() !== '' &&
      this.form.rm !== null &&
      this.isPanCardSelected &&
      this.isAadhardSelected
    );
  }

  onImageSelected(event: any): void {
    const file = event.target.files[0];
    if (
      file &&
      (file.type.startsWith('image/jpeg') ||
        file.type.startsWith('image/jpg') ||
        file.type.startsWith('image/png'))
    ) {
      this.imageFile = file;
      this.isPanCardSelected = true;
      this.form.pan = file;
    } else {
      this.isPanCardSelected = false;
    }
  }

  onPdfSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.pdfFile = file;
      this.isAadhardSelected = true;
    } else {
      this.isAadhardSelected = false;
      alert('Only PDF files are allowed');
    }
  }

  btnCancel() {
    this.router.navigate(['/login']);
  }

  onVideoSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type.startsWith('video/')) this.videoFile = file;
    else alert('Only video files are allowed');
  }

  submit() {
    let formData = new FormData();

    if (this.imageFile) formData.append('panCard', this.imageFile);

    // if (this.videoFile) formData.append('video', this.videoFile);
    formData.append('name', this.form.name);
    formData.append('rm', this.form.rm);
    const headers = new HttpHeaders({ 'Content-Type': 'multipart/form-data' });

    this.http
      .post(
        'https://4gv6vfzcq4.execute-api.us-west-2.amazonaws.com/uploadKYCFiles',
        formData
      )
      .subscribe({
        next: (res) => alert('panCard uploaded successfully!'),
        error: () => alert('Upload failed!'),
      });

    formData = new FormData();
    if (this.pdfFile) formData.append('aadharCard', this.pdfFile);
    // if (this.videoFile) formData.append('video', this.videoFile);
    formData.append('name', this.form.name);
    formData.append('rm', this.form.rm);

    this.http
      .post(
        'https://4gv6vfzcq4.execute-api.us-west-2.amazonaws.com/uploadKYCFiles',
        formData
      )
      .subscribe({
        next: (res) => alert('aadhar Files uploaded successfully!'),
        error: () => alert('Upload failed!'),
      });
    // Normally, here you'd send form data to the backend
  }
}
