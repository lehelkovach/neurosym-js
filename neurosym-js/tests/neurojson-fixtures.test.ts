import fs from 'fs';
import path from 'path';
import { infer } from '../src';
import type { NeuroJSONProgram } from '../src/types';

interface FixtureExpectations {
  meta: {
    iterations: number;
    seed: number;
  };
  programs: Record<
    string,
    {
      posteriors: Record<string, number>;
    }
  >;
}

const fixturesRoot = path.resolve(__dirname, '../../neurojson');
const expectationsPath = path.join(fixturesRoot, 'fixtures/v0.1/expectations.json');
const expectations = JSON.parse(fs.readFileSync(expectationsPath, 'utf8')) as FixtureExpectations;

const loadProgram = (name: string): NeuroJSONProgram => {
  const programPath = path.join(fixturesRoot, 'examples', `${name}.json`);
  return JSON.parse(fs.readFileSync(programPath, 'utf8')) as NeuroJSONProgram;
};

describe('NeuroJSON v0.1 fixture parity', () => {
  const { iterations, seed } = expectations.meta;

  Object.entries(expectations.programs).forEach(([name, expected]) => {
    test(`matches fixture: ${name}`, () => {
      const program = loadProgram(name);
      const result = infer(program, undefined, { iterations, seed });

      Object.entries(expected.posteriors).forEach(([key, value]) => {
        const actual = result.posteriors[key] ?? 0;
        expect(actual).toBeCloseTo(value, 3);
      });
    });
  });
});
