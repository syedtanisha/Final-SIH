import client from './client';

export const quizApi = {
  generate: (params) => client.post('/assessments/generate', params),
  getAll: () => client.get('/assessments'),
  getById: (id) => client.get(`/assessments/${id}`),
  startAttempt: (id) => client.post(`/assessments/${id}/start`),
  submitAttempt: (id, attemptId, answers) =>
    client.post(`/assessments/${id}/submit`, { attempt_id: attemptId, answers }),
};

export default quizApi;
