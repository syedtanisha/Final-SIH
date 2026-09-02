import client from './client';

export const learningSourcesApi = {
  refreshSource: (providerId = 'all') => client.post(`/admin/learning-sources/${providerId}/refresh`),
  getSourceStatus: (providerId) => client.get(`/admin/learning-sources/${providerId}/status`),
};

export default learningSourcesApi;
