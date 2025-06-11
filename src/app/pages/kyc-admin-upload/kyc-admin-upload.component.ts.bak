import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-kyc-admin-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
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
  splitArray: string[] = [];
  passportPhotoMsg: string = '';

  isPanCardSelected: boolean = false;
  isAadhardSelected: boolean = false;
  isAudioFileSelected: boolean = true;
  isPassportPhotoSelected: boolean = false;
  userData: any = null;
  submitted: boolean = false;
  constructor(private router: Router, private http: HttpClient) {}

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
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];

      if (file.type !== 'audio/mpeg') {
        alert('Only MP3 files are allowed.');
        this.isAudioFileSelected = false;
        return;
      }

      this.audioFile = file;
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

  btnCancel() {
    this.router.navigate(['/kyc-dashboard']);
  }

  submit() {
    
    //different API will be call

    // Normally, here you'd send form data to the backend
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
      let formData = new FormData();

    if (this.imageFile) formData.append('dl', this.imageFile);

    // if (this.videoFile) formData.append('video', this.videoFile);
    //formData.append('name', this.userData.name);
    //formData.append('rm', this.userData.rm);
    const headers = new HttpHeaders({ 'Content-Type': 'multipart/form-data' });

    this.http
      .post(
        'https://4gv6vfzcq4.execute-api.us-west-2.amazonaws.com/kyc/uploadKYCFiles',
        formData
      )
      .subscribe({
        next: (res) => alert('Driving license uploaded successfully!'),
        error: () => alert('Driving license uploaded successfully!'),
      });

    } else {
      this.isPanCardSelected = false;
    }
  }

  onPdfSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf' ||
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
        next: (res) => alert('aadhar Files uploaded successfully!'),
        error: () => alert('Upload failed!'),
      });
    } else {
      this.isAadhardSelected = false;
      alert('Only PDF files are allowed');
    }
  }

  onFileChange(event: any): void {
    console.log('validating file change')
  const file = event.target.files[0];
  if (file) {
    console.log('file correct')
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
    photo: base64Image
  };

  this.http.post('https://6xwvmbv78k.execute-api.us-west-2.amazonaws.com/kyc/PassportPhoto', payload).subscribe({
    next: res => {
   //   console.log('Upload success', res)
      
      this.processResponse(res)
    },
    error: err => console.error('Upload failed', err)
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
               this.splitArray =response.body.split(',');
               let factDetectedArr = this.splitArray[0].split(':');
              // console.log('Split Array:', this.splitArray[0]);
              //    console.log('Split Array:', this.splitArray[1]);
               if(factDetectedArr[0].includes('FaceDetected') && factDetectedArr[1].includes('True')) {
                this.isPassportPhotoSelected = true;
                this.passportPhotoMsg = 'Passport photo uploaded successfully!';
                 return;
               }else{
                this.isPassportPhotoSelected = false;
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
}
