import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { ChatbotComponent } from './pages/chat/chat-bot.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, ChatbotComponent, CommonModule], // ✅ Import RouterModule here
  template: `<router-outlet></router-outlet><app-chatbot *ngIf='showChatbot()'></app-chatbot>`,
})
export class AppComponent {
  chatVisible = false;
  constructor(public router: Router) {}

  showChatbot(): boolean {
    // Add the routes where chatbot should be visible
    const allowedRoutes = ['/user-upload', '/admin-upload'];
    return allowedRoutes.includes(this.router.url);
  }

  toggleChat() {
    this.chatVisible = !this.chatVisible;
  }
}
