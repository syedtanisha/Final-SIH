import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Award, 
  BrainCircuit, 
  Sparkles, 
  Building2, 
  ArrowRight, 
  CheckCircle2, 
  ShieldCheck, 
  FileSpreadsheet, 
  Layers 
} from 'lucide-react';

export const LandingPage = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="space-y-8 sm:space-y-12 pb-8">
      {/* Hero Section (Academic Journal Theme) */}
      <section className="bg-[#FAFAF9] text-[#1C1917] border-b border-[#E7E5E4] py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-4">
          <span className="inline-block px-3 py-1 rounded bg-[#FEF3C7] text-[#1C1917] border border-[#D97706] text-xs font-extrabold uppercase tracking-wider font-mono">
            Ministry of Statistics and Programme Implementation (MoSPI)
          </span>

          <h1 className="text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-[#1C1917] max-w-4xl mx-auto leading-tight">
            StatLearn AI — Official Capacity Building & Competency Diagnostics
          </h1>

          <p className="text-xs sm:text-sm md:text-base text-[#78716C] max-w-2xl mx-auto leading-relaxed">
            Calibrated with NSSTA curricula and Indian Statistical Service (ISS) competency frameworks. Diagnose skill gaps, generate grounded AI study quizzes, and verify learning progression.
          </p>

          <div className="pt-4 flex flex-wrap items-center justify-center gap-3">
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#991B1B] hover:bg-[#7F1D1D] text-white font-bold rounded text-xs shadow-2xs transition"
              >
                <span>Go to Officer Dashboard</span>
                <ArrowRight className="w-4 h-4 text-[#FEF3C7]" />
              </Link>
            ) : (
              <>
                <Link
                  to="/login"
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#991B1B] hover:bg-[#7F1D1D] text-white font-bold rounded text-xs shadow-2xs transition"
                >
                  <span>Officer Sign In</span>
                  <ArrowRight className="w-4 h-4 text-[#FEF3C7]" />
                </Link>
                <Link
                  to="/register"
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#FEF3C7] hover:bg-[#FEF3C7]/80 text-[#1C1917] font-bold rounded text-xs border border-[#D97706] transition"
                >
                  Register Cadre
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* 4 Core Pillars Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4">
        <div className="text-center space-y-1">
          <h2 className="text-lg sm:text-xl font-bold text-[#1C1917]">
            Capacity Building Pillars
          </h2>
          <p className="text-xs text-[#78716C]">
            Four pillars powering statistical cadre development in India.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-5 shadow-2xs space-y-2">
            <div className="w-8 h-8 rounded bg-[#FEE2E2] text-[#991B1B] flex items-center justify-center font-bold border border-[#FCA5A5]">
              <Award className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-[#1C1917] text-sm">Competency Matrix</h3>
            <p className="text-[#78716C] leading-relaxed">
              Mapped against 9 statistical domains (PLFS, CPI, National Accounts, ASI) with required baseline benchmarks.
            </p>
          </div>

          <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#D97706] p-5 shadow-2xs space-y-2">
            <div className="w-8 h-8 rounded bg-[#FEF3C7] text-[#1C1917] flex items-center justify-center font-bold border border-[#D97706]">
              <BrainCircuit className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-[#1C1917] text-sm">AI Gap Diagnosis</h3>
            <p className="text-[#78716C] leading-relaxed">
              Identifies priority gaps through baseline testing and computes personalized training recommendations.
            </p>
          </div>

          <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-5 shadow-2xs space-y-2">
            <div className="w-8 h-8 rounded bg-[#FEE2E2] text-[#991B1B] flex items-center justify-center font-bold border border-[#FCA5A5]">
              <Sparkles className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-[#1C1917] text-sm">Document Quiz Studio</h3>
            <p className="text-[#78716C] leading-relaxed">
              Upload official PDF reports and survey manuals to generate grounded verification MCQs.
            </p>
          </div>

          <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#D97706] p-5 shadow-2xs space-y-2">
            <div className="w-8 h-8 rounded bg-[#FEF3C7] text-[#1C1917] flex items-center justify-center font-bold border border-[#D97706]">
              <Building2 className="w-4 h-4 text-[#991B1B]" />
            </div>
            <h3 className="font-bold text-[#1C1917] text-sm">NSSTA & MoSPI Hub</h3>
            <p className="text-[#78716C] leading-relaxed">
              Access verified academy modules, eSankhyiki data assets, and official survey manuals.
            </p>
          </div>
        </div>
      </section>

      {/* Standards Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg border border-[#E7E5E4] p-6 shadow-2xs flex flex-col md:flex-row items-center justify-between gap-4 text-xs">
          <div className="space-y-1">
            <h3 className="font-bold text-[#1C1917] text-sm">Aligned with Government of India Frameworks</h3>
            <p className="text-[#78716C]">
              Supporting Indian Statistical Service (ISS), Subordinate Statistical Service (SSS), and State DES officers.
            </p>
          </div>
          <Link
            to={isAuthenticated ? "/dashboard" : "/login"}
            className="px-4 py-2 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded font-bold transition shadow-2xs whitespace-nowrap"
          >
            Access Portal
          </Link>
        </div>
      </section>
    </div>
  );
};
