import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '../../core/config';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html'
})
export class ReportsComponent {
  summary: any;

  constructor(private http: HttpClient) {
    this.loadSummary();
  }

  loadSummary(): void {
    this.http
      .get<{ summary: any }>(`${environment.apiUrl}/reports/summary`)
      .subscribe((response) => (this.summary = response.summary));
  }
}
