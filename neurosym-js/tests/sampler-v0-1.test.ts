import { compileProgram, infer } from '../src';
import type { NeuroJSONProgram } from '../src/types';

describe('sampler (NeuroJSON v0.1)', () => {
  test('runtime evidence overrides program evidence', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 }
      },
      factors: [],
      evidence: { a: 0 },
      queries: ['a']
    };

    const result = infer(program, { a: 1 }, { iterations: 200, seed: 1 });
    expect(result.posteriors.a).toBe(1);
  });

  test('filters posteriors to queries and keeps explanations', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 },
        b: { type: 'boolean', prior: 0.2 },
        out: { type: 'boolean', prior: 0.1 }
      },
      factors: [
        { inputs: ['a'], output: 'out', op: 'IF_THEN', weight: 0.9, mode: 'support' },
        { inputs: ['b'], output: 'out', op: 'IF_THEN', weight: 0.2, mode: 'support' }
      ],
      evidence: { a: 1, b: 1 },
      queries: ['out']
    };

    const result = infer(program, undefined, { iterations: 500, seed: 11 });
    expect(Object.keys(result.posteriors)).toEqual(['out']);
    const explanation = result.explanations?.out;
    expect(explanation?.supportingFactors.length).toBe(2);
    if (explanation) {
      expect(explanation.supportingFactors[0]?.weight).toBeGreaterThan(
        explanation.supportingFactors[1]?.weight ?? 0
      );
    }
  });

  test('reports clamped and ignored evidence', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 }
      },
      factors: []
    };

    const result = infer(program, { a: 1, ghost: 0 }, { iterations: 50, seed: 2 });
    expect(result.evidenceStats?.clamped).toContain('a');
    expect(result.evidenceStats?.ignored).toContain('ghost');
  });

  test('effective sample size equals iterations without evidence', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 }
      },
      factors: []
    };

    const result = infer(program, undefined, { iterations: 250, seed: 3 });
    expect(result.effectiveSampleSize).toBe(250);
    expect(result.evidenceStats?.ignored).toBeUndefined();
  });

  test('IR input bypasses query filtering', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 },
        b: { type: 'boolean', prior: 0.4 }
      },
      factors: [],
      queries: ['a']
    };

    const ir = compileProgram(program);
    const result = infer(ir, undefined, { iterations: 10, seed: 4 });
    expect(result.posteriors).toHaveProperty('a');
    expect(result.posteriors).toHaveProperty('b');
  });
});
