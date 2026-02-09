import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, catchError, switchMap, throwError } from 'rxjs';

import { AuthService } from './auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private refreshInFlight = false;

  constructor(private auth: AuthService) {}

  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const cloned = req.clone({ withCredentials: true });
    return next.handle(cloned).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status !== 401 || this.refreshInFlight) {
          return throwError(() => error);
        }
        this.refreshInFlight = true;
        return this.auth.refresh().pipe(
          switchMap(() => {
            this.refreshInFlight = false;
            return next.handle(cloned);
          }),
          catchError((refreshError) => {
            this.refreshInFlight = false;
            return throwError(() => refreshError);
          })
        );
      })
    );
  }
}
