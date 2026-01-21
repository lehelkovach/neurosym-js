import { compileProgram } from '../src';
import type { NeuroJSONProgram } from '../src/types';

describe('compileProgram (NeuroJSON v0.1)', () => {
  test('fills default prior when omitted', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean' }
      },
      factors: []
    };

    const ir = compileProgram(program);
    expect(ir.variables[0]?.prior).toBe(0.5);
  });

  test('rejects invalid arity', () => {
    const invalid: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 },
        b: { type: 'boolean', prior: 0.3 }
      },
      factors: [
        { inputs: ['a', 'b'], output: 'a', op: 'IF_THEN', weight: 0.9, mode: 'support' }
      ]
    };

    expect(() => compileProgram(invalid)).toThrow();
  });

  test('rejects undefined factor variables', () => {
    const invalid: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 }
      },
      factors: [
        { inputs: ['a'], output: 'missing', op: 'IF_THEN', weight: 0.9, mode: 'support' }
      ]
    };

    expect(() => compileProgram(invalid)).toThrow(/defined variable/);
  });

  test('warns on cycles and unknown evidence/queries', () => {
    const program: NeuroJSONProgram = {
      version: '0.1',
      variables: {
        a: { type: 'boolean', prior: 0.2 },
        b: { type: 'boolean', prior: 0.3 }
      },
      factors: [
        { inputs: ['a'], output: 'b', op: 'IF_THEN', weight: 0.7, mode: 'support' },
        { inputs: ['b'], output: 'a', op: 'IF_THEN', weight: 0.6, mode: 'support' }
      ],
      evidence: { a: 1, ghost: 1 },
      queries: ['a', 'ghost']
    };

    const ir = compileProgram(program);
    const warnings = ir.warnings ?? [];
    expect(warnings.some((warning) => warning.includes('Cycle detected'))).toBe(true);
    expect(warnings.some((warning) => warning.includes('Unknown evidence'))).toBe(true);
    expect(warnings.some((warning) => warning.includes('Unknown query'))).toBe(true);
  });
});
