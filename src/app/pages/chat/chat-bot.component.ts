import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { ChatbotService } from '../../services/chat.service';


@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule
  ],
  templateUrl: './chat-bot.component.html',
  styleUrls: ['./chat-bot.component.css']
})
export class ChatbotComponent {
  messages: { from: 'user' | 'bot', text: string }[] = [];
  userInput = '';
  isLoading = false;

  constructor(private chatbotService: ChatbotService) {}

  sendMessage() {
    const message = this.userInput.trim();
    if (!message) return;

    this.messages.push({ from: 'user', text: message });
    this.userInput = '';
    this.isLoading = true;

    this.chatbotService.sendMessage(message).subscribe({
      next: (res) => {
        this.messages.push({ from: 'bot', text: res.reply });
        this.isLoading = false;
      },
      error: (err) => {
        this.messages.push({ from: 'bot', text: '❌ Error getting reply.' });
        this.isLoading = false;
      }
    });
  }
}
