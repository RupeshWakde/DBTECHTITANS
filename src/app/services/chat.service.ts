

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = 'https://4i1o5wz778.execute-api.us-west-2.amazonaws.com/prod/chatbotLambda3'; // Replace with your actual endpoint

  constructor(private http: HttpClient) {}

  sendMessage(prompt: string): Observable<{ reply: string }> {
    return this.http.post<{ reply: string }>(this.apiUrl, { prompt });
  }
}

