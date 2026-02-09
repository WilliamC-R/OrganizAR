import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../core/config';

export interface Category {
  id: number;
  name: string;
  kind: 'income' | 'expense';
}

export interface Entry {
  id: number;
  category_id: number;
  kind: 'income' | 'expense';
  amount: string;
  description?: string;
  date: string;
}

@Injectable({ providedIn: 'root' })
export class FinanceService {
  constructor(private http: HttpClient) {}

  listCategories(kind?: string): Observable<{ categories: Category[] }> {
    const params = kind ? `?kind=${kind}` : '';
    return this.http.get<{ categories: Category[] }>(`${environment.apiUrl}/categories${params}`);
  }

  createCategory(payload: Partial<Category>): Observable<{ category: Category }> {
    return this.http.post<{ category: Category }>(`${environment.apiUrl}/categories`, payload);
  }

  listEntries(): Observable<{ entries: Entry[] }> {
    return this.http.get<{ entries: Entry[] }>(`${environment.apiUrl}/entries`);
  }

  createEntry(payload: Partial<Entry>): Observable<{ entry: Entry }> {
    return this.http.post<{ entry: Entry }>(`${environment.apiUrl}/entries`, payload);
  }
}
