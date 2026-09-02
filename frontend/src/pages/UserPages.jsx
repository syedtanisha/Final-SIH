import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { competencyApi, progressApi, authApi, analyticsApi, learningSourcesApi } from '../services/api';
import { RadarChartComp, GapCard } from '../components/UIComponents';
import { 
  BarChart3, 
  BrainCircuit, 
  Compass, 
  Sparkles, 
  TrendingUp, 
  Award, 
  ArrowRight, 
  CheckCircle2, 
  BookOpen, 
  Save, 
  ShieldCheck, 
  Users,
  RefreshCw,
  AlertTriangle,
  FileCheck,
  TrendingDown,
  Info
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line
} from 'recharts';

/* ==========================================================================
   1. DashboardPage Component
   ========================================================================== */
export const DashboardPage = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [gapAnalysis, setGapAnalysis] = useState(null);
  const [progressSummary, setProgressSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [profileRes, gapRes, progressRes] = await Promise.all([
          competencyApi.getProfile(),
          competencyApi.getGapAnalysis(),
          progressApi.getSummary()
        ]);
        setProfile(profileRes.data);
        setGapAnalysis(gapRes.data);
        setProgressSummary(progressRes.data);
      } catch (err) {
        console.error("Dashboard data load error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-[#78716C] text-xs font-mono">
        Loading official competency telemetry...
      </div>
    );
  }

  const criticalGaps = gapAnalysis?.gaps?.filter(g => g.gap > 0).slice(0, 3) || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-5">
      {/* Summary Header */}
      <div className="bg-white rounded-lg p-5 border border-[#E7E5E4] border-t-4 border-t-[#991B1B] shadow-2xs flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-[#FEF3C7] border border-[#D97706] text-[#1C1917] text-[10px] font-bold uppercase font-mono">
              {user?.department || 'MoSPI'}
            </span>
            <span className="text-xs text-[#78716C] font-medium font-mono">
              {user?.designation || 'Statistical Cadre'}
            </span>
          </div>
          <h1 className="text-xl font-bold text-[#1C1917]">
            Dashboard: {user?.full_name}
          </h1>
          <p className="text-xs text-[#78716C]">
            Real-time competency tracking calibrated with MoSPI and NSSTA standards.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Link
            to="/assessment"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded text-xs font-bold shadow-2xs transition"
          >
            <span>Baseline Assessment</span>
            <ArrowRight className="w-3.5 h-3.5 text-[#FEF3C7]" />
          </Link>
          <Link
            to="/studio"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-[#FEF3C7] hover:bg-[#D97706]/20 text-[#1C1917] rounded text-xs font-bold border border-[#D97706] transition"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#991B1B]" />
            <span>AI Quiz Studio</span>
          </Link>
        </div>
      </div>

      {/* 4 Summary Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-4 shadow-2xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-[#78716C] text-xs font-medium font-mono">Readiness Index</span>
            <span className="w-6 h-6 rounded bg-[#FEF3C7] text-[#1C1917] font-bold flex items-center justify-center text-xs border border-[#D97706] font-mono">%</span>
          </div>
          <p className="text-2xl font-bold text-[#1C1917]">{profile?.overall_readiness_score || 0}%</p>
          <span className="text-[10px] text-[#78716C]">Assessed Proficiency</span>
        </div>

        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#D97706] p-4 shadow-2xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-[#78716C] text-xs font-medium font-mono">Competencies Tracked</span>
            <span className="w-6 h-6 rounded bg-[#FEF3C7] text-[#1C1917] font-bold flex items-center justify-center text-xs border border-[#D97706] font-mono">#</span>
          </div>
          <p className="text-2xl font-bold text-[#1C1917]">{profile?.competencies?.length || 0}</p>
          <span className="text-[10px] text-[#78716C]">Framework Matrix</span>
        </div>

        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#FCA5A5] p-4 shadow-2xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-[#78716C] text-xs font-medium font-mono">Total Verified Gain</span>
            <span className="w-6 h-6 rounded bg-[#FEE2E2] text-[#991B1B] font-bold flex items-center justify-center text-xs border border-[#FCA5A5] font-mono">+</span>
          </div>
          <p className="text-2xl font-bold text-[#991B1B]">+{progressSummary?.total_learning_gain || 0}%</p>
          <span className="text-[10px] text-[#78716C]">Quantified Gain</span>
        </div>

        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-4 shadow-2xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-[#78716C] text-xs font-medium font-mono">Active Focus Domain</span>
            <span className="w-6 h-6 rounded bg-[#FEF3C7] text-[#1C1917] font-bold flex items-center justify-center text-xs border border-[#D97706] font-mono">★</span>
          </div>
          <p className="text-sm font-bold text-[#1C1917] truncate mt-1">{gapAnalysis?.primary_focus_domain || 'Survey Methodology'}</p>
          <span className="text-[10px] text-[#78716C]">Primary Priority</span>
        </div>
      </div>

      {/* Charts & Priority Gaps Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Radar Chart Panel */}
        <div className="lg:col-span-6 bg-white rounded-lg border border-[#E7E5E4] p-5 shadow-2xs space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-[#1C1917]">Competency Benchmark Radar</h2>
            <Link to="/competencies" className="text-xs font-bold text-[#991B1B] hover:underline font-mono">
              View Matrix →
            </Link>
          </div>
          <RadarChartComp competencies={profile?.competencies || []} />
        </div>

        {/* Priority Gaps Panel */}
        <div className="lg:col-span-6 bg-white rounded-lg border border-[#E7E5E4] p-5 shadow-2xs space-y-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-sm font-bold text-[#1C1917]">Priority Competency Gaps</h2>
              <Link to="/gap-analysis" className="text-xs font-bold text-[#991B1B] hover:underline font-mono">
                View All Gaps →
              </Link>
            </div>
            {criticalGaps.length > 0 ? (
              <div className="space-y-3">
                {criticalGaps.map((gap) => (
                  <GapCard key={gap.competency_id} gapItem={gap} />
                ))}
              </div>
            ) : (
              <p className="text-xs text-[#78716C] py-8 text-center">
                All competency benchmarks currently met!
              </p>
            )}
          </div>

          <div className="pt-2 border-t border-[#E7E5E4] flex items-center justify-between text-xs">
            <span className="text-[#78716C]">Need tailored training resources?</span>
            <Link
              to="/recommendations"
              className="font-bold text-[#991B1B] hover:underline flex items-center gap-1 font-mono"
            >
              <span>Explore Training</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

/* ==========================================================================
   2. ProfilePage Component
   ========================================================================== */
export const ProfilePage = () => {
  const { user, refreshUser } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [designation, setDesignation] = useState(user?.designation || '');
  const [department, setDepartment] = useState(user?.department || '');
  const [organization, setOrganization] = useState(user?.organization || 'Government of India');
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaved(false);
    try {
      await authApi.updateProfile({
        full_name: fullName,
        designation,
        department,
        organization,
      });
      await refreshUser();
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error("Profile update error:", err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
      {/* Header */}
      <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-5 shadow-2xs flex items-center gap-3.5 text-xs">
        <div className="w-10 h-10 rounded bg-[#FEF3C7] text-[#1C1917] font-bold text-base flex items-center justify-center border border-[#D97706] font-mono">
          {user?.full_name?.charAt(0) || 'O'}
        </div>
        <div>
          <h1 className="text-base font-bold text-[#1C1917]">{user?.full_name}</h1>
          <p className="text-[#78716C]">{user?.designation} • {user?.department}</p>
          <span className="inline-block mt-0.5 text-[10px] text-[#78716C] font-mono">
            {user?.email}
          </span>
        </div>
      </div>

      {/* Form */}
      <div className="bg-white rounded-lg border border-[#E7E5E4] p-5 sm:p-6 shadow-2xs space-y-3">
        <h2 className="text-sm font-bold text-[#1C1917]">Officer Profile Settings</h2>

        {saved && (
          <div className="p-2.5 bg-[#FEF3C7] border border-[#D97706] text-[#1C1917] text-xs rounded flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#991B1B]" />
            <span>Profile details updated successfully!</span>
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-3 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-[#1C1917] mb-1">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-3 py-2 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917]"
              />
            </div>

            <div>
              <label className="block font-semibold text-[#1C1917] mb-1">Official Designation</label>
              <input
                type="text"
                value={designation}
                onChange={(e) => setDesignation(e.target.value)}
                className="w-full px-3 py-2 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917]"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-[#1C1917] mb-1">Department / Division</label>
              <input
                type="text"
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="w-full px-3 py-2 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917]"
              />
            </div>

            <div>
              <label className="block font-semibold text-[#1C1917] mb-1">Organization</label>
              <input
                type="text"
                value={organization}
                onChange={(e) => setOrganization(e.target.value)}
                className="w-full px-3 py-2 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917]"
              />
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center gap-1.5 px-4 py-2 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded text-xs font-bold transition disabled:opacity-50 shadow-2xs"
            >
              <Save className="w-3.5 h-3.5 text-[#FEF3C7]" />
              <span>{saving ? 'Saving...' : 'Save Profile Changes'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

/* ==========================================================================
   3. AdminPage Component (Phase 6 & 7 Workforce Intelligence Dashboard)
   ========================================================================== */
export const AdminPage = () => {
  const [overview, setOverview] = useState(null);
  const [competencies, setCompetencies] = useState(null);
  const [departments, setDepartments] = useState(null);
  const [effectiveness, setEffectiveness] = useState(null);
  const [skillGaps, setSkillGaps] = useState(null);
  const [emergingSkills, setEmergingSkills] = useState(null);
  const [forecast, setForecast] = useState(null);

  const [syncing, setSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllAnalytics();
  }, []);

  const fetchAllAnalytics = async () => {
    setLoading(true);
    try {
      const [ovRes, compRes, deptRes, effRes, gapRes, emRes, fcRes] = await Promise.all([
        analyticsApi.getOverview(),
        analyticsApi.getCompetencies(),
        analyticsApi.getDepartments(),
        analyticsApi.getTrainingEffectiveness(),
        analyticsApi.getSkillGaps(),
        analyticsApi.getEmergingSkills(),
        analyticsApi.getCapacityForecast()
      ]);
      setOverview(ovRes.data);
      setCompetencies(compRes.data);
      setDepartments(deptRes.data);
      setEffectiveness(effRes.data);
      setSkillGaps(gapRes.data);
      setEmergingSkills(emRes.data);
      setForecast(fcRes.data);
    } catch (err) {
      console.error("Admin workforce analytics error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshProvider = async (providerId = 'all') => {
    setSyncing(true);
    setSyncMessage('');
    try {
      const res = await learningSourcesApi.refreshSource(providerId);
      setSyncMessage(res.data.message || `Successfully synchronized provider '${providerId}'.`);
      await fetchAllAnalytics();
    } catch (err) {
      console.error("Sync provider error:", err);
      setSyncMessage(err.response?.data?.detail || "Failed to synchronize learning provider.");
    } finally {
      setSyncing(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center text-[#78716C] text-xs font-mono">
        Aggregating organization workforce analytics & predictive intelligence...
      </div>
    );
  }

  const deptDataChart = Object.entries(departments?.departments || {}).map(([dept, score]) => ({
    name: dept.length > 20 ? `${dept.substring(0, 18)}...` : dept,
    Readiness: score
  }));

  const forecastDataChart = [
    { period: 'Current', Score: forecast?.current_organizational_readiness || 0 },
    { period: '60 Days Proj.', Score: forecast?.projected_readiness_60d || 0 },
    { period: '90 Days Proj.', Score: forecast?.projected_readiness_90d || 0 }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Header & Source Sync Action */}
      <div className="bg-white rounded-lg p-5 border border-[#E7E5E4] border-t-4 border-t-[#991B1B] shadow-2xs flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-[#FEF3C7] border border-[#D97706] text-[#1C1917] text-[10px] font-bold uppercase font-mono">
              System Administrator
            </span>
            <span className="text-xs text-[#78716C] font-mono">
              Status: {overview?.system_status || 'Operational'}
            </span>
          </div>
          <h1 className="text-xl font-bold text-[#1C1917]">
            Workforce Intelligence & Capacity Analytics
          </h1>
          <p className="text-xs text-[#78716C]">
            Enterprise capacity building analytics across MoSPI, NSSTA, and State DES cadres.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => handleRefreshProvider('all')}
            disabled={syncing}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded text-xs font-bold shadow-2xs transition disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-[#FEF3C7] ${syncing ? 'animate-spin' : ''}`} />
            <span>{syncing ? 'Synchronizing Providers...' : 'Refresh Provider Sources'}</span>
          </button>
        </div>
      </div>

      {syncMessage && (
        <div className="p-3 bg-[#FEF3C7] border border-[#D97706] text-[#1C1917] text-xs rounded flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Info className="w-4 h-4 text-[#991B1B]" />
            <span>{syncMessage}</span>
          </div>
          <button onClick={() => setSyncMessage('')} className="text-[10px] font-bold text-[#991B1B]">
            Dismiss
          </button>
        </div>
      )}

      {/* 4 Key Summary Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-4 shadow-2xs space-y-1">
          <span className="text-[#78716C] text-xs font-medium font-mono">Total Officers Analyzed</span>
          <p className="text-2xl font-bold text-[#1C1917]">{overview?.total_officers || 0}</p>
          <span className="text-[10px] text-[#78716C]">Active Cadre Workforce</span>
        </div>

        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#D97706] p-4 shadow-2xs space-y-1">
          <span className="text-[#78716C] text-xs font-medium font-mono">Org. Readiness Score</span>
          <p className="text-2xl font-bold text-[#1C1917]">{overview?.organization_readiness_score || 0}%</p>
          <span className="text-[10px] text-[#78716C]">Confidence: {overview?.evidence_level || 'HIGH_EVIDENCE'}</span>
        </div>

        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#FCA5A5] p-4 shadow-2xs space-y-1">
          <span className="text-[#78716C] text-xs font-medium font-mono">Highest Gap Discipline</span>
          <p className="text-base font-bold text-[#991B1B] truncate">{competencies?.highest_gap_competency || 'STAT_PRICE_IND'}</p>
          <span className="text-[10px] text-[#78716C]">Critical Focus Target</span>
        </div>

        <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-4 shadow-2xs space-y-1">
          <span className="text-[#78716C] text-xs font-medium font-mono">Training Completion Rate</span>
          <p className="text-2xl font-bold text-[#1C1917]">{effectiveness?.completion_rate_pct || 0}%</p>
          <span className="text-[10px] text-[#78716C]">Avg Gain: +{effectiveness?.average_competency_gain || 0}%</span>
        </div>
      </div>

      {/* Row 2: Department Readiness Chart & Top Critical Gaps */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <div className="lg:col-span-7 bg-white rounded-lg border border-[#E7E5E4] p-5 shadow-2xs space-y-3">
          <h2 className="text-sm font-bold text-[#1C1917]">Departmental Readiness Distribution</h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={deptDataChart} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E7E5E4" />
                <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#78716C' }} interval={0} angle={-20} textAnchor="end" />
                <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: '#78716C' }} />
                <Tooltip contentStyle={{ fontSize: '11px', background: '#FAFAF9', borderColor: '#E7E5E4' }} />
                <Bar dataKey="Readiness" fill="#991B1B" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-5 bg-white rounded-lg border border-[#E7E5E4] p-5 shadow-2xs space-y-3">
          <h2 className="text-sm font-bold text-[#1C1917]">Ranked Skill Gap Priorities</h2>
          <p className="text-[11px] text-[#78716C] font-mono">
            {skillGaps?.priority_formula}
          </p>

          <div className="space-y-2.5">
            {skillGaps?.top_critical_gaps?.map((gap, idx) => (
              <div key={gap.code} className="p-3 bg-[#FAFAF9] border border-[#E7E5E4] rounded flex items-center justify-between text-xs">
                <div>
                  <span className="font-mono text-[10px] text-[#991B1B] font-bold">#{idx + 1} {gap.code}</span>
                  <h4 className="font-bold text-[#1C1917]">{gap.name}</h4>
                  <span className="text-[10px] text-[#78716C]">{gap.affected_officer_count} Officers Affected • Avg Gap: {gap.avg_gap}%</span>
                </div>
                <div className="text-right font-mono">
                  <span className="px-2 py-1 bg-[#FEF3C7] text-[#1C1917] border border-[#D97706] rounded text-[10px] font-bold">
                    P-Score: {gap.priority_score}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Row 3: Emerging Skill Signals & Capacity Forecast */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <div className="lg:col-span-6 bg-white rounded-lg border border-[#E7E5E4] p-5 shadow-2xs space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-[#1C1917]">Emerging Skill Signals</h2>
            <span className="text-[10px] text-[#78716C] font-mono">Rule-Based Signal Detection</span>
          </div>

          <div className="space-y-2 text-xs">
            {emergingSkills?.signals?.map((sig) => (
              <div key={sig.code} className="p-3 bg-white border border-[#E7E5E4] rounded flex items-center justify-between">
                <div>
                  <span className="font-mono text-[10px] text-[#78716C]">{sig.code}</span>
                  <h4 className="font-bold text-[#1C1917]">{sig.name}</h4>
                  <p className="text-[10px] text-[#78716C]">{sig.rationale}</p>
                </div>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono border ${
                  sig.signal === 'EMERGING' ? 'bg-[#FEE2E2] text-[#991B1B] border-[#FCA5A5]' :
                  sig.signal === 'GROWING' ? 'bg-[#FEF3C7] text-[#1C1917] border-[#D97706]' :
                  'bg-[#F5F5F4] text-[#78716C] border-[#E7E5E4]'
                }`}>
                  {sig.signal}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-6 bg-white rounded-lg border border-[#E7E5E4] p-5 shadow-2xs space-y-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-sm font-bold text-[#1C1917]">Capacity-Building Forecast</h2>
              <span className="text-[10px] font-bold text-[#991B1B] font-mono">
                {forecast?.forecast_status}
              </span>
            </div>

            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={forecastDataChart} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E7E5E4" />
                  <XAxis dataKey="period" tick={{ fontSize: 10, fill: '#78716C' }} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: '#78716C' }} />
                  <Tooltip contentStyle={{ fontSize: '11px', background: '#FAFAF9' }} />
                  <Line type="monotone" dataKey="Score" stroke="#991B1B" strokeWidth={2} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-3 space-y-1 bg-[#FAFAF9] p-3 rounded border border-[#E7E5E4] text-[11px] text-[#78716C]">
              <span className="font-bold text-[#1C1917] block">Model Assumptions & Capping Disclaimers:</span>
              <ul className="list-disc list-inside space-y-0.5 text-[10px]">
                {forecast?.assumptions?.map((asm, i) => (
                  <li key={i}>{asm}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="pt-2 border-t border-[#E7E5E4] flex items-center justify-between text-[11px] text-[#78716C]">
            <span>Method: {forecast?.forecast_method}</span>
            <span className="font-mono font-bold text-[#991B1B]">Historical Delta: +{forecast?.historical_gain_rate_per_activity}%</span>
          </div>
        </div>
      </div>
    </div>
  );
};
