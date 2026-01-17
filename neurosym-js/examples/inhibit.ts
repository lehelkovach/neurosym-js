import { infer } from '../src';
import type { NeuroJSONProgram } from '../src/types';

const program: NeuroJSONProgram = {
  version: '0.1',
  variables: {
    rain: { type: 'boolean', prior: 0.2 },
    umbrella: { type: 'boolean', prior: 0.3 },
    wet_grass: { type: 'boolean', prior: 0.05 }
  },
  factors: [
    { id: 'rain_wets_grass', inputs: ['rain'], output: 'wet_grass', op: 'IF_THEN', weight: 0.8, mode: 'support' },
    { id: 'umbrella_inhibits', inputs: ['umbrella'], output: 'wet_grass', op: 'IF_THEN', weight: 0.7, mode: 'inhibit' }
  ],
  evidence: { rain: 1, umbrella: 1 },
  queries: ['wet_grass']
};

const result = infer(program, undefined, { iterations: 5000, seed: 7 });

console.log('Posteriors:', result.posteriors);
console.log('Top inhibiting factors for wet_grass:');
const inhibiting = result.explanations?.wet_grass?.inhibitingFactors ?? [];
inhibiting.slice(0, 3).forEach((factor) => {
  console.log(`- ${factor.factorId ?? factor.factorIndex}: contribution=${factor.contribution.toFixed(3)}`);
});
