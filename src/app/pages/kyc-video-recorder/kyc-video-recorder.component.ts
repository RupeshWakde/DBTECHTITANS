import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-kyc-video-recorder',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './kyc-video-recorder.component.html',
  styleUrl: './kyc-video-recorder.component.css',
})
export class KycVideoRecorderComponent implements AfterViewInit {
  @ViewChild('video', { static: false })
  videoRef!: ElementRef<HTMLVideoElement>;
  capturedImage: string | null = null;

  ngAfterViewInit() {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        const video = this.videoRef.nativeElement;
        video.srcObject = stream;
      })
      .catch((err) => {
        console.error('Camera access denied:', err);
      });
  }

  capture() {
    const video = this.videoRef.nativeElement;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 400;
    canvas.height = video.videoHeight || 300;
    canvas
      .getContext('2d')
      ?.drawImage(video, 0, 0, canvas.width, canvas.height);
    this.capturedImage = canvas.toDataURL('image/png');
  }

  downloadImage() {
    if (!this.capturedImage) return;
    const a = document.createElement('a');
    a.href = this.capturedImage;
    a.download = 'captured-image.png';
    a.click();
  }
}
