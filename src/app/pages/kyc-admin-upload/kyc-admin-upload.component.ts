import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { MatDialog } from '@angular/material/dialog';
import { DataModalComponent } from '../model/data-modal.component';
import { PhotoDataModalComponent } from '../model/photo-data-modal.component';

@Component({
  selector: 'app-kyc-admin-upload',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule, MatProgressSpinnerModule],
  styleUrl: './kyc-admin-upload.component.css',
  templateUrl: './kyc-admin-upload.component.html',
})
export class KycAdminUploadComponent implements OnInit {
  form: any = {
    name: '',
    rm: '',
    pan: null,
    aadhaar: null,
    audio: null,
    video: null,
  };

  imageFile: File | null = null;
  pdfFile: File | null = null;
  videoFile: File | null = null;
  audioFile: File | null = null;
  photoFile: File | null = null;
  splitArray: string[] = [];
  passportPhotoMsg: string = '';

  isPanCardSelected: boolean = false;
  isAadhardSelected: boolean = false;
  isAudioFileSelected: boolean = true;
  isPassportPhotoSelected: boolean = false;

  isphotoUploading: boolean = false;
  showPhotoViewIcon: boolean = false;

  isDlUploading: boolean = false;
  showDlViewIcon: boolean = false;

  isAudiolUploading: boolean = false;
  showAudioViewIcon: boolean = false;

  isAadharUploading: boolean = false;
  showAadharViewIcon: boolean = false;

  phoneUploadResponseData: any = null;

  userData: any = null;
  submitted: boolean = false;
  constructor(
    private router: Router,
    private http: HttpClient,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    this.userData = history.state.user;
    console.log(this.userData);

    // You can now call an API to fetch full user detail using this.userId
  }

  handleFile(event: any, type: string) {
    const file = event.target.files[0];
    if (file) {
      this.form[type] = file;
    }
  }

  isFormValid(): boolean {
    return (
      this.userData.name.trim() !== '' &&
      this.userData.rm !== null &&
      this.isPanCardSelected &&
      this.isAadhardSelected &&
      this.isAudioFileSelected &&
      this.isPassportPhotoSelected
    );
  }

  onAudioFileSelected(event: Event): void {
    this.isAudiolUploading = true;
    this.showAudioViewIcon = false;

    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      if (file.type !== 'audio/mpeg') {
        alert('Only MP3 files are allowed.');
        this.isAudioFileSelected = false;
        return;
      }

      this.audioFile = file;
      let formData = new FormData();

      if (this.imageFile) formData.append('audio', this.audioFile);

      // if (this.videoFile) formData.append('video', this.videoFile);
      formData.append('audio', this.audioFile);
      //formData.append('rm', this.userData.rm);
      const headers = new HttpHeaders({
        'Content-Type': 'multipart/form-data',
      });

      this.http
        .post(
          'https://8g9i5dxsl7.execute-api.us-west-2.amazonaws.com/default/uploadAudioFiles',
          formData
        )
        .subscribe({
          next: (res) => {
            this.isAudiolUploading = false;
            this.showAudioViewIcon = true;
            alert('Audio Files uploaded successfully!');
          },
          error: () => {
            this.isAudiolUploading = false;
            this.showAudioViewIcon = true;
          },
        });
    }
  }

  onVideoSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      if (!file.type.startsWith('video/')) {
        alert('Please select a valid video file (mp4/webm/ogg)');
        this.isPassportPhotoSelected = false;
        return;
      }

      this.isPassportPhotoSelected = true;

      this.videoFile = file;
    }
  }

  fetchAndOpenFile(): void {
    console.log(' After click ');
    console.log(this.phoneUploadResponseData);

    // Convert to array format for table:

    this.dialog.open(PhotoDataModalComponent, {
      data: this.phoneUploadResponseData,
      width: '600px',
    });

    // const payload = {
    //   processing_method: 'DetectDocumentText', // or 'AnalyzeDocument' for forms
    //   Records: [
    //     {
    //       s3: {
    //         bucket: { name: 'dbdtcckyctextract' },
    //         object: { key: this.photoFile?.name },
    //       },
    //     },
    //   ],
    // };

    // this.http
    //   .post(
    //     'https://hx2lvepxw7.execute-api.us-west-2.amazonaws.com/textract-prod/extract-form',
    //     payload
    //   )
    //   .subscribe({
    //     next: (res) => console.log('Response:', res),
    //     error: (err) => console.error('Error:', err),
    //   });
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

  fetchAudioOpenFile(): void {
    // console.log(audioSampleData.body.results.transcripts);

    const payload = {
      processing_method: 'DetectDocumentText', // or 'AnalyzeDocument' for forms
      Records: [
        {
          s3: {
            bucket: { name: 'dbdtcckyctextract' },
            object: { key: this.audioFile?.name },
          },
        },
      ],
    };

    this.http
      .get(
        'https://1r9wm6v7mf.execute-api.us-west-2.amazonaws.com/audiototxt4/audioToTxt2?audio=' +
          this.audioFile?.name
      )
      .subscribe({
        next: (res) => {
          console.log(typeof res);
          console.log(res);
          const audionJSon = JSON.parse(res as string);
          console.log(audionJSon);

          const transscriptData = audionJSon?.results?.transcripts?.[0];
          const noTranscriptMessage = 'No transcript available.';
          if (transscriptData?.transcript?.trim()) {
            this.dialog.open(DataModalComponent, {
              data: transscriptData,
              width: '600px',
            });
          } else {
            this.dialog.open(DataModalComponent, {
              data: { noTranscriptMessage },
              width: '600px',
            });
          }
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

  closeAadharModal(): void {}

  btnCancel() {
    this.router.navigate(['/kyc-dashboard']);
  }

  submit() {
    //different API will be call
    // Normally, here you'd send form data to the backend
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

  onFileChange(event: any): void {
    console.log('validating file change');
    this.isphotoUploading = true;
    this.showPhotoViewIcon = false;
    const file = event.target.files[0];
    this.photoFile = file;
    if (file) {
      console.log('file correct');
      const reader = new FileReader();
      reader.onload = () => {
        const base64String = (reader.result as string).split(',')[1]; // remove data:image/jpeg;base64,
        //   const base64String = reader.result as string; // keep the full data URL
        //    console.log('Base64 String:', base64String);
        const paddedBase64 = this.padBase64(base64String); // ensure correct length
        //  console.log(paddedBase64); // send this to your API
        this.uploadToApi(paddedBase64);
      };
      reader.readAsDataURL(file);
    }
  }

  uploadToApi(base64Image: string): void {
    const payload = {
      photo: base64Image,
    };

    this.http
      .post(
        'https://6xwvmbv78k.execute-api.us-west-2.amazonaws.com/kyc/PassportPhoto',
        payload
      )
      .subscribe({
        next: (res) => {
          //   console.log('Upload success', res)

          this.processResponse(res);
        },
        error: (err) => console.error('Upload failed', err),
      });
  }
  padBase64(base64: string): string {
    const remainder = base64.length % 4;
    if (remainder > 0) {
      return base64 + '='.repeat(4 - remainder);
    }
    return base64;
  }
  processResponse(response: any) {
    if (response && response.body) {
      try {
        //   const jsonString = response.body.replace(/'/g, '"');
        // Replace single quotes around keys
        //let      jsonstr = response.body.replace(/'([^']+)':/g, '$1:');
        //  console.log('##################### Response Body:', response.body);

        this.phoneUploadResponseData = response.body;

        // Convert Python-style booleans and single quotes to JS-style
        const sanitized = this.phoneUploadResponseData
          .replace(/'/g, '"') // single to double quotes
          .replace(/\bTrue\b/g, 'true') // Python True to JS true
          .replace(/\bFalse\b/g, 'false'); // Python False to JS false

        // Parse to object
        const result =
          sanitized.indexOf('Invalid image') == -1
            ? JSON.parse(sanitized)
            : sanitized;

        // console.log('result);
        this.phoneUploadResponseData = result;

        // this.phoneUploadResponseData = "{'FaceDetected': 'True', 'Sharpness': '89.85481262207031', 'Brightness': '92.2479019165039', 'IsBlurry': 'False', 'IsTooDarkOrBright': 'False'}";

        this.splitArray = response.body.split(',');
        let factDetectedArr = this.splitArray[0].split(':');

        console.log(this.splitArray);
        // console.log('Split Array:', this.splitArray[0]);
        //    console.log('Split Array:', this.splitArray[1]);
        if (
          factDetectedArr[0].includes('FaceDetected') &&
          factDetectedArr[1].includes('True')
        ) {
          this.isPassportPhotoSelected = true;
          this.isphotoUploading = false;
          this.showPhotoViewIcon = true;
          this.passportPhotoMsg = 'Passport photo uploaded successfully!';
          return;
        } else {
          this.isPassportPhotoSelected = false;
          this.isphotoUploading = false;
          //this.passportPhotoMsg = 'Passport photo upload failed!';
          this.passportPhotoMsg = this.splitArray[0];
        }

        //  let modifiedString = response.body.replace(/'([^']+)'(?=:)/g, '"$1"');
        // Replace single quotes around values
        //     console.log('##################### Response Body:', modifiedString);
        //  modifiedString = modifiedString.replace(/'([^']+)'/g, '"$1"');
        //const jsonString = jsonstr.replace(/(\w+)/g, '"$1"');
        // console.log('Response Body:', jsonString);
        // const parsedBody = JSON.parse(jsonString);
        //console.log('Parsed Body:', parsedBody);
      } catch (e) {
        console.error('Error parsing JSON:', e);
      }
    }
  }

  fnSubmitKYC() {
    this.router.navigate(['/kyc-success']);
  }
}
