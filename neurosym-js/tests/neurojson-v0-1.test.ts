import { infer, validateProgram } from '../src';
import type { NeuroJSONProgram } from '../src/types';

describe('NeuroJSON v0.1 sampler', () => {
  test('wet grass evidence increases P(rain)', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        rain: { type: 'boolean', prior: 0.2 },
        sprinkler: { type: 'boolean', prior: 0.1 },
        wet_grass: { type: 'boolean', prior: 0.05 }
      },
      factors: [
        { inputs: ['rain'], output: 'wet_grass', op: 'IF_THEN', weight: 0.8, mode: 'support' },
        { inputs: ['sprinkler'], output: 'wet_grass', op: 'IF_THEN', weight: 0.6, mode: 'support' }
      ],
      evidence: { wet_grass: 1 },
      queries: ['rain']
    };

    const result = infer(program, undefined, { iterations: 5000, seed: 42 });
    const rainPosterior = result.posteriors.rain ?? 0;
    expect(rainPosterior).toBeGreaterThan(0.2);
  });

  test('inhibit factor reduces P(wet_grass)', () => {
    const base: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        rain: { type: 'boolean', prior: 0.2 },
        umbrella: { type: 'boolean', prior: 0.3 },
        wet_grass: { type: 'boolean', prior: 0.05 }
      },
      factors: [
        { inputs: ['rain'], output: 'wet_grass', op: 'IF_THEN', weight: 0.8, mode: 'support' },
        { inputs: ['umbrella'], output: 'wet_grass', op: 'IF_THEN', weight: 0.7, mode: 'inhibit' }
      ],
      queries: ['wet_grass']
    };

    const noUmbrella = infer(
      { ...base, evidence: { rain: 1, umbrella: 0 } },
      undefined,
      { iterations: 5000, seed: 7 }
    );
    const withUmbrella = infer(
      { ...base, evidence: { rain: 1, umbrella: 1 } },
      undefined,
      { iterations: 5000, seed: 7 }
    );
    const wetNoUmbrella = noUmbrella.posteriors.wet_grass ?? 0;
    const wetWithUmbrella = withUmbrella.posteriors.wet_grass ?? 0;
    expect(wetWithUmbrella).toBeLessThan(wetNoUmbrella);
  });

  test('multiple supports stay within [0,1]', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.1 },
        b: { type: 'boolean', prior: 0.2 },
        c: { type: 'boolean', prior: 0.3 },
        target: { type: 'boolean', prior: 0.05 }
      },
      factors: [
        { inputs: ['a'], output: 'target', op: 'IF_THEN', weight: 0.9, mode: 'support' },
        { inputs: ['b'], output: 'target', op: 'IF_THEN', weight: 0.8, mode: 'support' },
        { inputs: ['c'], output: 'target', op: 'IF_THEN', weight: 0.7, mode: 'support' }
      ],
      evidence: { a: 1, b: 1, c: 1 },
      queries: ['target']
    };

    const result = infer(program, undefined, { iterations: 3000, seed: 9 });
    const targetPosterior = result.posteriors.target ?? 0;
    expect(targetPosterior).toBeGreaterThanOrEqual(0);
    expect(targetPosterior).toBeLessThanOrEqual(1);
  });

  test('unknown evidence and queries are surfaced', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        known: { type: 'boolean', prior: 0.4 }
      },
      factors: [],
      evidence: { known: 1, missing: 1 },
      queries: ['known', 'missing']
    };

    const result = infer(program, undefined, { iterations: 1000, seed: 5 });
    expect(result.evidenceStats?.ignored).toContain('missing');
    expect(result.warnings?.some((warning) => warning.includes('missing'))).toBe(true);
  });
});

describe('NeuroJSON v0.1 validation', () => {
  test('invalid op and weight are rejected', () => {
    const invalid = {
      version: '0.1',
      variables: {
        rain: { type: 'boolean', prior: 0.2 }
      },
      factors: [
        { inputs: ['rain'], output: 'rain', op: 'XOR', weight: 1.2, mode: 'support' }
      ]
    };

    const result = validateProgram(invalid);
    expect(result.valid).toBe(false);
    expect(result.errors.length).toBeGreaterThan(0);
  });

  test('missing variables are rejected', () => {
    const invalid = {
      version: '0.1',
      variables: {},
      factors: []
    };
    const result = validateProgram(invalid);
    expect(result.valid).toBe(false);
  });
});
