import client from './client';

export const contentApi = {
  upload: (formData) =>
    client.post('/content/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getAll: () => client.get('/content'),
  getStatus: (docId) => client.get(`/content/${docId}/status`),
  overrideCompetency: (docId, competencyId) =>
    client.post(`/content/${docId}/override-competency`, { competency_id: competencyId }),
};

export default contentApi;
