import Ajv from 'ajv';
import type { ErrorObject } from 'ajv';
import schema from './neurojson.schema.json';
import type {
  NeuroJSONProgram,
  ProgramValidationIssue,
  ProgramValidationResult
} from '../types';

const ajv = new Ajv({ allErrors: true, allowUnionTypes: true });
const validate = ajv.compile(schema);

const formatPath = (instancePath: string, missingProperty?: string): string => {
  const pointer = instancePath || '';
  const parts = pointer
    .split('/')
    .slice(1)
    .map((segment) => segment.replace(/~1/g, '/').replace(/~0/g, '~'));

  const path = parts
    .map((segment) => (segment.match(/^\d+$/) ? `[${segment}]` : segment))
    .reduce((acc, segment) => {
      if (segment.startsWith('[')) {
        return `${acc}${segment}`;
      }
      return acc ? `${acc}.${segment}` : segment;
    }, '');

  if (missingProperty) {
    return path ? `${path}.${missingProperty}` : missingProperty;
  }

  return path;
};

const formatErrors = (errors: ErrorObject[] | null | undefined): ProgramValidationIssue[] => {
  if (!errors) {
    return [];
  }

  return errors.map((error) => {
    const missingProperty =
      typeof error.params === 'object' && error.params !== null
        ? (error.params as { missingProperty?: string }).missingProperty
        : undefined;
    return {
      path: formatPath(error.instancePath, missingProperty),
      message: error.message ?? 'Invalid value'
    };
  });
};

export const validateProgram = (program: unknown): ProgramValidationResult => {
  const valid = validate(program);
  const errors = formatErrors(validate.errors);
  return { valid: Boolean(valid), errors };
};

export const assertValidProgram = (program: unknown): NeuroJSONProgram => {
  const result = validateProgram(program);
  if (!result.valid) {
    const details = result.errors
      .map((error) => (error.path ? `${error.path}: ${error.message}` : error.message))
      .join('; ');
    throw new Error(`NeuroJSON validation failed: ${details}`);
  }

  return program as NeuroJSONProgram;
};
