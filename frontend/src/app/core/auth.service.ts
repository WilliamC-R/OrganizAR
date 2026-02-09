import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';

import { environment } from './config';

export interface User {
  id: string;
  email: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private userSubject = new BehaviorSubject<User | null>(null);
  user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<{ user: User }> {
    return this.http
      .post<{ user: User }>(`${environment.apiUrl}/auth/login`, { email, password })
      .pipe(tap((response) => this.userSubject.next(response.user)));
  }

  register(email: string, password: string): Observable<{ user: User }> {
    return this.http.post<{ user: User }>(`${environment.apiUrl}/auth/register`, {
      email,
      password
    });
  }

  me(): Observable<{ user: User }> {
    return this.http
      .get<{ user: User }>(`${environment.apiUrl}/auth/me`)
      .pipe(tap((response) => this.userSubject.next(response.user)));
  }

  refresh(): Observable<{ ok: boolean }> {
    return this.http.post<{ ok: boolean }>(`${environment.apiUrl}/auth/refresh`, {});
  }

  logout(): Observable<{ ok: boolean }> {
    return this.http
      .post<{ ok: boolean }>(`${environment.apiUrl}/auth/logout`, {})
      .pipe(tap(() => this.userSubject.next(null)));
  }

  get user(): User | null {
    return this.userSubject.value;
  }
}
