import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { AuthService } from './auth.service';
import { environment } from './config';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should login and set user', () => {
    service.login('user@example.com', 'password').subscribe((response) => {
      expect(response.user.email).toBe('user@example.com');
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    req.flush({ user: { id: '1', email: 'user@example.com' } });
    httpMock.verify();
  });
});
