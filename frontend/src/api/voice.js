import client from './client';

export const voiceApi = {
  transcribeAudio: (file, language = 'en') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    return client.post('/voice/transcribe', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  synthesizeText: (text, language = 'en') => {
    return client.post('/voice/synthesize', { text, language });
  },

  sendVoiceChat: (sessionId, file, language = 'en') => {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('language', language);
    formData.append('file', file);
    return client.post('/voice/chat', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export default voiceApi;
