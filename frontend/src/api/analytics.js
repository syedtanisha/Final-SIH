import client from './client';

export const analyticsApi = {
  getOverview: () => client.get('/admin/analytics/overview'),
  getCompetencies: () => client.get('/admin/analytics/competencies'),
  getDepartments: () => client.get('/admin/analytics/departments'),
  getTrainingEffectiveness: () => client.get('/admin/analytics/training-effectiveness'),
  getSkillGaps: () => client.get('/admin/analytics/skill-gaps'),
  getEmergingSkills: () => client.get('/admin/analytics/emerging-skills'),
  getCapacityForecast: () => client.get('/admin/analytics/capacity-forecast'),
};

export default analyticsApi;
