import {
  activationFromInputs,
  applyInhibit,
  applySupport,
  clampProbability
} from '../src/engine/logic';
import type { FactorOpV01 } from '../src/types';

describe('engine logic (NeuroJSON v0.1)', () => {
  test('clampProbability clamps below 0', () => {
    expect(clampProbability(-0.2)).toBe(0);
  });

  test('clampProbability clamps above 1', () => {
    expect(clampProbability(1.2)).toBe(1);
  });

  test('clampProbability preserves in-range values', () => {
    expect(clampProbability(0.4)).toBe(0.4);
  });

  test('applySupport increases probability within bounds', () => {
    const boosted = applySupport(0.9, 0.9);
    expect(boosted).toBeLessThanOrEqual(1);
    expect(boosted).toBeGreaterThan(0.9);
  });

  test('applyInhibit decreases probability within bounds', () => {
    const reduced = applyInhibit(0.1, 0.9);
    expect(reduced).toBeGreaterThanOrEqual(0);
    expect(reduced).toBeLessThan(0.1);
  });

  test('activationFromInputs handles IF_THEN', () => {
    expect(activationFromInputs('IF_THEN', [1])).toBe(1);
    expect(activationFromInputs('IF_THEN', [0])).toBe(0);
  });

  test('activationFromInputs handles NOT', () => {
    expect(activationFromInputs('NOT', [1])).toBe(0);
    expect(activationFromInputs('NOT', [0])).toBe(1);
  });

  test('activationFromInputs handles AND', () => {
    expect(activationFromInputs('AND', [1, 1, 1])).toBe(1);
    expect(activationFromInputs('AND', [1, 0, 1])).toBe(0);
  });

  test('activationFromInputs handles OR', () => {
    expect(activationFromInputs('OR', [0, 0, 0])).toBe(0);
    expect(activationFromInputs('OR', [0, 1, 0])).toBe(1);
  });

  test('activationFromInputs returns 0 for unknown op', () => {
    expect(activationFromInputs('XOR' as FactorOpV01, [1, 0])).toBe(0);
  });
});
