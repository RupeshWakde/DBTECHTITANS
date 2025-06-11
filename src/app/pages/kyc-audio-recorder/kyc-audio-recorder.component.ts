import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-kyc-audio-recorder',
  standalone: true,
  imports: [CommonModule],
  styleUrl: './kyc-audio-recorder.component.css',
  templateUrl: './kyc-audio-recorder.component.html',
})
export class KycAudioRecorderComponent {
  mediaRecorder: MediaRecorder | null = null;
  recordedChunks: Blob[] = [];
  audioURL: string | null = null;
  isRecording = false;
  errorMessage = '';

  async startRecording() {
    this.errorMessage = '';
    this.recordedChunks = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.recordedChunks.push(event.data);
        }
      };

      this.mediaRecorder.onstop = () => {
        const blob = new Blob(this.recordedChunks, { type: 'audio/webm' });
        this.audioURL = URL.createObjectURL(blob);
      };

      this.mediaRecorder.start();
      this.isRecording = true;
    } catch (err) {
      this.errorMessage = 'Microphone access denied or not available.';
      console.error('Error accessing microphone:', err);
    }
  }

  stopRecording() {
    if (this.mediaRecorder && this.isRecording) {
      this.mediaRecorder.stop();
      this.isRecording = false;
    }
  }
}
