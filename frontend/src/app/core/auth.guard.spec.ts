import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { of } from 'rxjs';

import { AuthGuard } from './auth.guard';
import { AuthService } from './auth.service';

describe('AuthGuard', () => {
  it('should allow when user already loaded', () => {
    const authService = { user: { id: '1', email: 'user@example.com' }, me: () => of({ user: { id: '1', email: 'user@example.com' } }) } as AuthService;
    const guard = new AuthGuard(authService, { navigate: () => {} } as Router);
    expect(guard.canActivate()).toBe(true);
  });
});
