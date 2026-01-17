import { infer } from '../src';
import type { NeuroJSONProgram } from '../src/types';

const program: NeuroJSONProgram = {
  version: '0.1',
  variables: {
    flu: { type: 'boolean', prior: 0.1 },
    allergy: { type: 'boolean', prior: 0.2 },
    cough_suppressant: { type: 'boolean', prior: 0.1 },
    cough: { type: 'boolean', prior: 0.05 }
  },
  factors: [
    { id: 'flu_causes_cough', inputs: ['flu'], output: 'cough', op: 'IF_THEN', weight: 0.7, mode: 'support' },
    { id: 'allergy_causes_cough', inputs: ['allergy'], output: 'cough', op: 'IF_THEN', weight: 0.5, mode: 'support' },
    { id: 'suppressant_inhibits', inputs: ['cough_suppressant'], output: 'cough', op: 'IF_THEN', weight: 0.6, mode: 'inhibit' }
  ],
  evidence: { flu: 1, allergy: 1, cough_suppressant: 1 },
  queries: ['cough']
};

const result = infer(program, undefined, { iterations: 5000, seed: 99 });

console.log('Posteriors:', result.posteriors);
console.log('Support vs inhibit for cough:');
console.log('Support:', result.explanations?.cough?.supportingFactors);
console.log('Inhibit:', result.explanations?.cough?.inhibitingFactors);
