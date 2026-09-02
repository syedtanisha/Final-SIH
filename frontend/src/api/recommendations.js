import client from './client';

export const recommendationApi = {
  getForYou: () => client.get('/recommendations'),
  getLearningPath: () => client.get('/recommendations/learning-path'),
};

export default recommendationApi;
