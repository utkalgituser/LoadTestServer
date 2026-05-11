import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { Counter, Trend } from 'k6/metrics';

const BASE = __ENV.BASE_URL || 'http://localhost:8000';

const payloads = new SharedArray('payloads', () => {
  try { return JSON.parse(open('../../data/payloads.json')); }
  catch (e) { return [{ transactionId: 'TXN-DEMO', amount: 100, currency: 'USD' }]; }
});

const errors = new Counter('mock_errors');
const mockLatency = new Trend('mock_latency_ms');

export const options = {
  scenarios: {
    smoke:    { executor: 'constant-vus', vus: 5,   duration: '30s', startTime: '0s' },
    sanity:   { executor: 'constant-vus', vus: 25,  duration: '1m',  startTime: '35s' },
    light:    { executor: 'constant-vus', vus: 50,  duration: '2m',  startTime: '1m40s' },
    moderate: { executor: 'constant-vus', vus: 100, duration: '2m',  startTime: '3m45s' },
  },
  thresholds: {
    http_req_failed:   ['rate<0.05'],
    http_req_duration: ['p(95)<200'],
  },
};

const headers = { 'Content-Type': 'application/json', 'X-Scenario': 'success' };

export default function () {
  const p = payloads[Math.floor(Math.random() * payloads.length)];

  const r1 = http.get(`${BASE}/health`);
  check(r1, { 'health 200': (r) => r.status === 200 });

  const r2 = http.post(`${BASE}/mock/payment`, JSON.stringify(p), { headers });
  mockLatency.add(r2.timings.duration);
  if (!check(r2, { 'mock 200': (r) => r.status === 200 })) errors.add(1);

  const r3 = http.get(`${BASE}/mock/users`);
  check(r3, { 'users 200': (r) => r.status === 200 });

  sleep(0.1);
}
