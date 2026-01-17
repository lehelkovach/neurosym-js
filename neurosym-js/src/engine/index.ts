import { compileProgram } from '../compiler/compile';
import { runSampler } from './sampler';
import type {
  InferenceOptions,
  InferenceSummary,
  NeuroJSONProgram,
  ProgramIR
} from '../types';

const isProgramIR = (input: unknown): input is ProgramIR => {
  if (!input || typeof input !== 'object') {
    return false;
  }
  const obj = input as ProgramIR;
  return Array.isArray(obj.variables) && Array.isArray(obj.factors) && !!obj.indexByName;
};

export const infer = (
  programOrIr: NeuroJSONProgram | ProgramIR | unknown,
  evidence?: Record<string, 0 | 1>,
  options: InferenceOptions = {}
): InferenceSummary => {
  const isIr = isProgramIR(programOrIr);
  const ir = isIr ? programOrIr : compileProgram(programOrIr);

  const programEvidence = !isIr && (programOrIr as NeuroJSONProgram).evidence;
  const mergedEvidence = { ...(programEvidence ?? {}), ...(evidence ?? {}) };

  const result = runSampler(ir, mergedEvidence, options);

  if (!isIr && Array.isArray((programOrIr as NeuroJSONProgram).queries)) {
    const querySet = new Set((programOrIr as NeuroJSONProgram).queries);
    const filteredPosteriors: Record<string, number> = {};
    const filteredExplanations: Record<string, NonNullable<InferenceSummary['explanations']>[string]> = {};

    Object.entries(result.posteriors).forEach(([name, value]) => {
      if (querySet.has(name)) {
        filteredPosteriors[name] = value;
        const explanation = result.explanations?.[name];
        if (explanation) {
          filteredExplanations[name] = explanation;
        }
      }
    });

    return {
      ...result,
      posteriors: filteredPosteriors,
      explanations: result.explanations ? filteredExplanations : undefined
    };
  }

  return result;
};
