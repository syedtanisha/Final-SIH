import client from './client';

export const assessmentApi = {
  getBaseline: () => client.get('/assessments/baseline'),
  submitBaseline: (answers) => client.post('/assessments/baseline/submit', { answers }),
  generateQuiz: (params) => client.post('/assessments/generate', params),
  getAllQuizzes: () => client.get('/assessments'),
  getQuizById: (quizId) => client.get(`/assessments/${quizId}`),
  startQuizAttempt: (quizId) => client.post(`/assessments/${quizId}/start`),
  submitQuizAttempt: (quizId, attemptId, answers) =>
    client.post(`/assessments/${quizId}/submit`, { attempt_id: attemptId, answers }),
  getProgressSummary: () => client.get('/assessments/progress/summary'),
  getFinalInterviewReadiness: () => client.get('/assessments/final-interview/readiness').catch(() => client.get('/final-interview/readiness')),
  evaluateInterviewAnswer: (data) => client.post('/assessments/final-interview/evaluate-answer', data).catch(() => client.post('/final-interview/evaluate-answer', data)),
  generateInterviewReport: (data) => client.post('/assessments/final-interview/generate-report', data).catch(() => client.post('/assessments/final-interview/report', data)).catch(() => client.post('/final-interview/report', data)),
};

export default assessmentApi;
