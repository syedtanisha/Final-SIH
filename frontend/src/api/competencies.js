import client from './client';

export const competencyApi = {
  getAll: (domain) => client.get('/competencies', { params: { domain } }),
  getProfile: () => client.get('/competencies/profile'),
  getGapAnalysis: () => client.get('/competencies/gap-analysis'),
};

export default competencyApi;
