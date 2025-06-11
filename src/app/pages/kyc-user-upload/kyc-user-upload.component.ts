import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { DataModalComponent } from '../model/data-modal.component';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-kyc-admin-upload',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule, MatProgressSpinnerModule],
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

  isDlUploading: boolean = false;
  showDlViewIcon: boolean = false;

  isAadharUploading: boolean = false;
  showAadharViewIcon: boolean = false;

  submitted = false;
  constructor(
    private router: Router,
    private http: HttpClient,
    private dialog: MatDialog
  ) {}

  handleFile(event: any, type: string) {
    const file = event.target.files[0];
    if (file) {
      this.form[type] = file;
    }
  }

  fetchAadharOpenFile(): void {
    const payload = {
      processing_method: 'DetectDocumentText', // or 'AnalyzeDocument' for forms
      Records: [
        {
          s3: {
            bucket: { name: 'dbdtcckyctextract' },
            object: { key: this.pdfFile?.name },
          },
        },
      ],
    };

    this.http
      .post(
        'https://hx2lvepxw7.execute-api.us-west-2.amazonaws.com/textract-prod/extract-form',
        payload
      )
      .subscribe({
        next: (res) => {
          console.log(res);

          // const parsedBody = JSON.parse(res.body);

          // Convert to array format for table:
          const tableData = Object.entries(res).map(([key, value]) => ({
            key,
            value,
          }));

          // console.log(tableData);

          let diplayData;
          for (const [key, value] of Object.entries(res)) {
            if (key == 'body') {
              // console.log('Key:', key, 'Value:', value);
              diplayData = JSON.parse(value);
            }
          }

          for (const [key, value] of Object.entries(diplayData)) {
            // if(key == 'body') {
            console.log(value);
            //   diplayData =value;
            // }
          }

          // console.log(diplayData)
          console.log(' Coming start ');

          this.dialog.open(DataModalComponent, {
            data: diplayData,
            width: '600px',
          });
          console.log(' Coming end ');
        },
        error: (err) => console.error('Error:', err),
      });
  }

  fetchDLAndOpenFile(): void {
    const payload = {
      processing_method: 'DetectDocumentText', // or 'AnalyzeDocument' for forms
      Records: [
        {
          s3: {
            bucket: { name: 'dbdtcckyctextract' },
            object: { key: this.imageFile?.name },
          },
        },
      ],
    };

    this.http
      .post(
        'https://hx2lvepxw7.execute-api.us-west-2.amazonaws.com/textract-prod/extract-form',
        payload
      )
      .subscribe({
        next: (res) => {
          console.log(res);

          // const parsedBody = JSON.parse(res.body);

          // Convert to array format for table:
          const tableData = Object.entries(res).map(([key, value]) => ({
            key,
            value,
          }));

          // console.log(tableData);

          let diplayData;
          for (const [key, value] of Object.entries(res)) {
            if (key == 'body') {
              // console.log('Key:', key, 'Value:', value);
              diplayData = JSON.parse(value);
            }
          }

          for (const [key, value] of Object.entries(diplayData)) {
            // if(key == 'body') {
            console.log(value);
            //   diplayData =value;
            // }
          }

          // console.log(diplayData)
          console.log(' Coming start ');

          this.dialog.open(DataModalComponent, {
            data: diplayData,
            width: '600px',
          });
          console.log(' Coming end ');
        },
        error: (err) => console.error('Error:', err),
      });
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
    this.isDlUploading = true;
    this.showDlViewIcon = false;
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
      let formData = new FormData();

      if (this.imageFile) formData.append('dl', this.imageFile);

      // if (this.videoFile) formData.append('video', this.videoFile);
      //formData.append('name', this.userData.name);
      //formData.append('rm', this.userData.rm);
      const headers = new HttpHeaders({
        'Content-Type': 'multipart/form-data',
      });

      this.http
        .post(
          'https://4gv6vfzcq4.execute-api.us-west-2.amazonaws.com/kyc/uploadKYCFiles',
          formData
        )
        .subscribe({
          next: (res) => alert('Driving license uploaded successfully!'),
          error: () => alert('Driving license uploaded successfully!'),
        });

      this.http
        .post(
          'https://4gv6vfzcq4.execute-api.us-west-2.amazonaws.com/kyc/uploadKYCFiles',
          formData
        )
        .subscribe({
          next: (res) => {
            this.isDlUploading = false;
            this.showDlViewIcon = true;
            alert('panCard uploaded successfully!');
          },
          error: () => {
            this.showDlViewIcon = true;
            this.isDlUploading = false;
            // alert('Upload failed!')
          },
        });
    } else {
      this.isPanCardSelected = false;
    }
  }

  onPdfSelected(event: any): void {
    this.isAadharUploading = true;
    this.showAadharViewIcon = false;
    const file = event.target.files[0];
    if (
      (file && file.type === 'application/pdf') ||
      file.type.startsWith('image/jpeg') ||
      file.type.startsWith('image/jpg') ||
      file.type.startsWith('image/png')
    ) {
      this.pdfFile = file;
      this.isAadhardSelected = true;

      let formData = new FormData();
      formData = new FormData();
      if (this.pdfFile) formData.append('ad', this.pdfFile);
      // if (this.videoFile) formData.append('video', this.videoFile);
      // formData.append('name', this.userData.name);
      // formData.append('rm', this.userData.rm);

      this.http
        .post(
          'https://4gv6vfzcq4.execute-api.us-west-2.amazonaws.com/uploadKYCFiles',
          formData
        )
        .subscribe({
          next: (res) => {
            this.isAadharUploading = false;
            this.showAadharViewIcon = true;
            alert('aadhar Files uploaded successfully!');
          },
          error: () => {
            this.isAadharUploading = false;
            this.showAadharViewIcon = true;
          },
        });
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
