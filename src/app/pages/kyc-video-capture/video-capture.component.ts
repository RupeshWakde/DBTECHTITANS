import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-video-capture',
  templateUrl: './video-capture.component.html',
  styleUrls: ['./video-capture.component.css'],
})
export class VideoCaptureComponent {
  @ViewChild('videoElement', { static: true })
  videoElement!: ElementRef<HTMLVideoElement>;

  mediaRecorder!: MediaRecorder;
  recordedBlobs: Blob[] = [];
  videoBlob!: Blob;
  isRecording = false;
  isVideoReady = false;

  constructor(private http: HttpClient) {}

  async startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    this.videoElement.nativeElement.srcObject = stream;

    this.recordedBlobs = [];
    this.mediaRecorder = new MediaRecorder(stream);

    this.mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        this.recordedBlobs.push(event.data);
      }
    };

    this.mediaRecorder.onstop = () => {
      console.log(' EEEEEEEEEEEEEEEEEEEEEEEEEEEE');
      this.videoBlob = new Blob(this.recordedBlobs, { type: 'video/webm' });
      this.isVideoReady = true;
      console.log(this.videoBlob)
      console.log(' FFFFF');
    };

    this.mediaRecorder.start();
    this.isRecording = true;

  }

  stopRecording() {
    console.log('!!!!!!!!!!!!!');
    this.mediaRecorder.stop();
    console.log('2222222222222222222222222');
    this.isRecording = false;

    const tracks = (
      this.videoElement.nativeElement.srcObject as MediaStream
    ).getTracks();
    tracks.forEach((track) => track.stop());
     console.log( this.isVideoReady);
     console.log('333333333333');
  }

  uploadVideo() {
    console.log(" Upload  ")
    console.log(this.videoBlob)
    const formData = new FormData();
    formData.append('video', this.videoBlob, 'kyc-video.webm');

    this.http.post('https://your-backend-api.com/upload', formData).subscribe({
      next: () => alert('✅ Video uploaded successfully!'),
      error: () => alert('❌ Upload failed.'),
    });
  }
}
