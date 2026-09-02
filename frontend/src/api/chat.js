import client from './client';

export const chatApi = {
  createSession: (title) => client.post('/chat/sessions', { title }),
  getSessions: () => client.get('/chat/sessions'),
  getSessionDetail: (sessionId) => client.get(`/chat/sessions/${sessionId}`),
  sendMessage: (sessionId, message) => client.post(`/chat/sessions/${sessionId}/messages`, { message }),
  deleteSession: (sessionId) => client.delete(`/chat/sessions/${sessionId}`),
};

export default chatApi;
