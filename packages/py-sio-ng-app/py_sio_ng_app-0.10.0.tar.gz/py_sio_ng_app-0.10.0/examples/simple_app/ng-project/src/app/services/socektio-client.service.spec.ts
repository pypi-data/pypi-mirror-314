import { TestBed } from '@angular/core/testing';

import { SocektioClientService } from './socektio-client.service';

describe('SocektioClientService', () => {
  let service: SocektioClientService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SocektioClientService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
