import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-data-modal',
  standalone: true,
  templateUrl: './data-modal.component.html',
  styleUrls: ['./data-modal.component.css'],
  imports: [CommonModule, MatButtonModule, MatIconModule]  // ✅ Add it here

})
export class DataModalComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private dialogRef: MatDialogRef<DataModalComponent>
  ) {}

  dataArray() {
    console.log(this.data)
    return Object.entries(this.data).map(([key, value]) => ({ key, value }));
  }

  close() {
    this.dialogRef.close();
  }
}
