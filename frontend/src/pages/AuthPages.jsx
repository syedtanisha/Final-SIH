import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  LogIn, 
  ShieldAlert, 
  ArrowRight, 
  Lock, 
  Mail, 
  User, 
  Building2, 
  Briefcase,
  CheckCircle2,
  TrendingUp,
  BrainCircuit,
  Award,
  BookOpen,
  FileCheck
} from 'lucide-react';
import { SearchableDropdown } from '../components/UIComponents';

/* ==========================================================================
   1. LoginPage Component (Option 3 Academic Theme)
   ========================================================================== */
export const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Invalid email or password. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = () => {
    setEmail('test_iss_officer@gov.in');
    setPassword('SecurePassword123!');
  };

  return (
    <div className="min-h-[calc(100vh-3.5rem-5rem)] flex flex-col justify-center py-6 sm:py-10">
      <div className="max-w-[1250px] w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          
          {/* LEFT COLUMN — Welcome, Portal Summary & Feature Rows */}
          <div className="lg:col-span-7 flex flex-col justify-between space-y-5 bg-white p-6 sm:p-8 rounded-lg border border-[#E7E5E4] shadow-2xs">
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span className="inline-block px-3 py-1 rounded bg-[#FEF3C7] text-[#1C1917] border border-[#D97706] text-xs font-extrabold uppercase tracking-wide font-mono">
                  Official Capacity Building Portal
                </span>
                <span className="text-xs text-[#78716C] font-semibold">MoSPI & NSSTA Standards</span>
              </div>
              <h1 className="text-2xl sm:text-4xl font-extrabold text-[#1C1917] tracking-tight leading-tight">
                Welcome to <span className="text-[#991B1B]">StatLearn AI</span>
              </h1>
              <p className="text-xs sm:text-sm text-[#78716C] leading-relaxed">
                StatLearn AI is a capacity-building and assessment platform designed to support learning, competency development, and skill assessment for officials across the Indian Statistical System.
              </p>
            </div>

            {/* 3 Structured Feature Rows */}
            <div className="space-y-3">
              <div className="p-4 rounded-lg border border-[#E7E5E4] bg-[#FAFAF9] hover:bg-[#FEF3C7]/40 transition flex items-start gap-3.5">
                <div className="w-9 h-9 rounded bg-[#FEF3C7] text-[#1C1917] flex items-center justify-center flex-shrink-0 border border-[#D97706] mt-0.5">
                  <Award className="w-4 h-4 text-[#991B1B]" />
                </div>
                <div className="space-y-0.5">
                  <h3 className="text-xs font-bold text-[#1C1917]">Assessments</h3>
                  <p className="text-[11px] text-[#78716C] leading-relaxed">
                    Evaluate knowledge and competencies through structured diagnostic assessments aligned with NSSTA & MoSPI standards.
                  </p>
                </div>
              </div>

              <div className="p-4 rounded-lg border border-[#E7E5E4] bg-[#FAFAF9] hover:bg-[#FEE2E2]/40 transition flex items-start gap-3.5">
                <div className="w-9 h-9 rounded bg-[#FEE2E2] text-[#991B1B] flex items-center justify-center flex-shrink-0 border border-[#FCA5A5] mt-0.5">
                  <TrendingUp className="w-4 h-4 text-[#991B1B]" />
                </div>
                <div className="space-y-0.5">
                  <h3 className="text-xs font-bold text-[#1C1917]">Learning Progress</h3>
                  <p className="text-[11px] text-[#78716C] leading-relaxed">
                    Track learning progress, completed activities, and verified skill gains over time.
                  </p>
                </div>
              </div>

              <div className="p-4 rounded-lg border border-[#E7E5E4] bg-[#FAFAF9] hover:bg-[#FEF3C7]/40 transition flex items-start gap-3.5">
                <div className="w-9 h-9 rounded bg-[#FEF3C7] text-[#1C1917] flex items-center justify-center flex-shrink-0 border border-[#D97706] mt-0.5">
                  <BrainCircuit className="w-4 h-4 text-[#1C1917]" />
                </div>
                <div className="space-y-0.5">
                  <h3 className="text-xs font-bold text-[#1C1917]">Competency Insights</h3>
                  <p className="text-[11px] text-[#78716C] leading-relaxed">
                    Understand performance, competency gaps, and targeted training development areas.
                  </p>
                </div>
              </div>
            </div>

            {/* Bottom Telemetry Bar */}
            <div className="pt-3 border-t border-[#E7E5E4] flex flex-wrap items-center justify-between text-[11px] text-[#78716C]">
              <span className="flex items-center gap-1 font-semibold text-[#1C1917]">
                <FileCheck className="w-3.5 h-3.5 text-[#991B1B]" /> 9 Core Statistical Framework Domains
              </span>
              <span className="font-mono">Cadres: ISS • SSS • State DES</span>
            </div>
          </div>

          {/* RIGHT COLUMN — Officer Sign In Card */}
          <div className="lg:col-span-5 flex flex-col justify-center">
            <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] shadow-sm p-6 sm:p-8 space-y-5">
              <div className="text-center space-y-1 pb-3 border-b border-[#E7E5E4]">
                <h2 className="text-xl font-extrabold text-[#1C1917]">Officer Sign In</h2>
                <p className="text-xs text-[#78716C]">
                  Enter official credentials to access portal
                </p>
              </div>

              {error && (
                <div className="p-3 rounded bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 flex-shrink-0 text-rose-600" />
                  <span>{error}</span>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4 text-xs">
                <div>
                  <label className="block font-semibold text-[#1C1917] mb-1">
                    Official Email (gov.in / nic.in)
                  </label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="officer.name@gov.in"
                    className="w-full px-3.5 py-2.5 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917] bg-[#FAFAF9]"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-[#1C1917] mb-1">
                    Password
                  </label>
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full px-3.5 py-2.5 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917] bg-[#FAFAF9]"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 px-4 bg-[#991B1B] hover:bg-[#7F1D1D] text-white font-bold rounded shadow-xs transition disabled:opacity-50 text-xs"
                >
                  {loading ? 'Signing in...' : 'Sign In'}
                </button>
              </form>

              <div className="text-center pt-1">
                <p className="text-xs text-[#78716C]">
                  Need an account?{' '}
                  <Link to="/register" className="text-[#1C1917] font-bold hover:underline">
                    Register Cadre
                  </Link>
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

/* ==========================================================================
   2. RegisterPage Component
   ========================================================================== */
export const RegisterPage = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    designation: '',
    department: '',
    organization: 'Government of India',
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const designations = [
    'Indian Statistical Service (ISS) - Director / Dy. Director',
    'Indian Statistical Service (ISS) - Joint Director',
    'Indian Statistical Service (ISS) - Assistant Director',
    'Indian Statistical Service (ISS) - Deputy Director General (DDG)',
    'Subordinate Statistical Service (SSS) - Senior Statistical Officer (SSO)',
    'Subordinate Statistical Service (SSS) - Junior Statistical Officer (JSO)',
    'Statistical Investigator Grade I - MoSPI / FOD',
    'State Directorate of Economics & Statistics (DES) - Director / Joint Director',
    'State Directorate of Economics & Statistics (DES) - Assistant Director / Officer',
    'Data Analyst / Senior Data Scientist - eSankhyiki / Digital Lab',
  ];

  const departments = [
    'MoSPI Field Operations Division (FOD) - Socioeconomic Surveys',
    'MoSPI National Accounts Division (NAD) - Macroeconomic & GDP Statistics',
    'MoSPI Economic Statistics Division (ESD) - CPI, IIP, ASI Indices',
    'MoSPI Survey Design & Research Division (SDRD) - Sampling & Methodology',
    'MoSPI Data Quality & Dissemination Division (DQDD) - eSankhyiki & Open Data',
    'National Statistical Systems Training Academy (NSSTA), Greater Noida',
    'State DES (Directorate of Economics & Statistics) - Delhi (NCT)',
    'State DES (Directorate of Economics & Statistics) - Maharashtra',
    'State DES (Directorate of Economics & Statistics) - Uttar Pradesh',
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!formData.designation.trim()) {
      setError('Please enter or select your Cadre / Designation');
      return;
    }
    if (!formData.department.trim()) {
      setError('Please enter or select your Division / Department');
      return;
    }

    setLoading(true);
    try {
      await register(formData);
      navigate('/onboarding');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Registration failed. Email may already be registered.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-8">
      <div className="max-w-xl w-full bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] shadow-sm p-6 space-y-4">
        <div className="text-center space-y-1">
          <h2 className="text-lg font-bold text-[#1C1917]">Officer Cadre Registration</h2>
          <p className="text-xs text-[#78716C]">
            Create your capacity building profile.
          </p>
        </div>

        {error && (
          <div className="p-3 rounded bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 flex-shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className="block font-semibold text-[#1C1917] mb-1">Full Name & Title</label>
            <input
              type="text"
              name="full_name"
              required
              value={formData.full_name}
              onChange={handleChange}
              placeholder="e.g. Dr. Rajesh Kumar"
              className="w-full px-3 py-2 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917]"
            />
          </div>

          <div>
            <label className="block font-semibold text-[#1C1917] mb-1">Official Email Address</label>
            <input
              type="email"
              name="email"
              required
              value={formData.email}
              onChange={handleChange}
              placeholder="officer@mospi.gov.in"
              className="w-full px-3 py-2 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917]"
            />
          </div>

          <div>
            <label className="block font-semibold text-[#1C1917] mb-1">Password</label>
            <input
              type="password"
              name="password"
              required
              value={formData.password}
              onChange={handleChange}
              placeholder="Minimum 8 characters"
              className="w-full px-3 py-2 border border-[#E7E5E4] rounded focus:border-[#991B1B] outline-none text-[#1C1917]"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <SearchableDropdown
                label="Cadre / Designation"
                name="designation"
                value={formData.designation}
                onChange={handleChange}
                options={designations}
                placeholder="Select designation..."
                required
              />
            </div>

            <div>
              <SearchableDropdown
                label="Division / Department"
                name="department"
                value={formData.department}
                onChange={handleChange}
                options={departments}
                placeholder="Select department..."
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-[#991B1B] hover:bg-[#7F1D1D] text-white font-bold rounded shadow-xs transition disabled:opacity-50 mt-2"
          >
            {loading ? 'Registering...' : 'Complete Registration'}
          </button>
        </form>

        <div className="text-center pt-2">
          <p className="text-xs text-[#78716C]">
            Already registered?{' '}
            <Link to="/login" className="text-[#1C1917] font-bold hover:underline">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
