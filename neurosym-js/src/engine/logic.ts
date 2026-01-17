import type { FactorOpV01 } from '../types';

export const clampProbability = (value: number): number => {
  if (value < 0) {
    return 0;
  }
  if (value > 1) {
    return 1;
  }
  return value;
};

export const applySupport = (p: number, weight: number): number => {
  return clampProbability(1 - (1 - p) * (1 - weight));
};

export const applyInhibit = (p: number, weight: number): number => {
  return clampProbability(p * (1 - weight));
};

export const activationFromInputs = (
  op: FactorOpV01,
  inputValues: number[]
): number => {
  switch (op) {
    case 'IF_THEN':
      return inputValues[0] ? 1 : 0;
    case 'NOT':
      return inputValues[0] ? 0 : 1;
    case 'AND':
      return inputValues.every((value) => value === 1) ? 1 : 0;
    case 'OR':
      return inputValues.some((value) => value === 1) ? 1 : 0;
    default:
      return 0;
  }
};
