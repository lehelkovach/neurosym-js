export interface TopoResult {
  order: number[] | null;
  hasCycle: boolean;
  cyclicNodes: number[];
}

export const buildTopoOrder = (nodeCount: number, edges: Array<[number, number]>): TopoResult => {
  const adjacency: number[][] = Array.from({ length: nodeCount }, () => []);
  const indegree = new Array<number>(nodeCount).fill(0);

  edges.forEach(([from, to]) => {
    adjacency[from]?.push(to);
    indegree[to] = (indegree[to] ?? 0) + 1;
  });

  const queue: number[] = [];
  indegree.forEach((deg, idx) => {
    if (deg === 0) {
      queue.push(idx);
    }
  });

  const order: number[] = [];
  while (queue.length > 0) {
    const node = queue.shift();
    if (node === undefined) {
      break;
    }
    order.push(node);
    adjacency[node]?.forEach((neighbor) => {
      indegree[neighbor] = (indegree[neighbor] ?? 0) - 1;
      if (indegree[neighbor] === 0) {
        queue.push(neighbor);
      }
    });
  }

  if (order.length !== nodeCount) {
    const cyclicNodes = indegree
      .map((deg, idx) => (deg > 0 ? idx : -1))
      .filter((idx) => idx >= 0);
    return { order: null, hasCycle: true, cyclicNodes };
  }

  return { order, hasCycle: false, cyclicNodes: [] };
};
