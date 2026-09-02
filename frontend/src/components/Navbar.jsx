import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  BarChart3, 
  BrainCircuit, 
  BookOpen, 
  Sparkles, 
  Compass, 
  TrendingUp, 
  User, 
  LogOut, 
  Menu, 
  X,
  Building2,
  Layers,
  ShieldCheck
} from 'lucide-react';

/* ==========================================================================
   StatLearn AI Academic Journal Emblem Component
   ========================================================================== */
const StatLearnLogo = ({ className = "w-8 h-8" }) => (
  <svg className={className} viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="40" height="40" rx="6" fill="#1C1917" />
    <rect x="8" y="22" width="5" height="11" rx="1" fill="#FEF3C7" />
    <rect x="16" y="16" width="5" height="17" rx="1" fill="#991B1B" />
    <path d="M8 20L18 12L25 17L33 8" stroke="#FAFAF9" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
    <circle cx="33" cy="8" r="2.5" fill="#D97706" />
  </svg>
);

export const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navGroups = [
    {
      groupTitle: 'CAPACITY NAVIGATION',
      links: [
        { name: 'Dashboard', path: '/dashboard', icon: BarChart3 },
        { name: 'Gap Analysis', path: '/gap-analysis', icon: BrainCircuit },
        { name: 'Recommendations', path: '/recommendations', icon: Compass },
        { name: 'Learning Path', path: '/learning-path', icon: Layers },
      ]
    },
    {
      groupTitle: 'PLATFORM',
      links: [
        { name: 'Govt Hub', path: '/hub', icon: Building2 },
        { name: 'AI Studio', path: '/studio', icon: Sparkles },
      ]
    },
    {
      groupTitle: 'PERSONAL',
      links: [
        { name: 'My Progress', path: '/progress', icon: TrendingUp },
        { name: 'Profile Settings', path: '/profile', icon: User },
      ]
    }
  ];

  const isPublicPage = !isAuthenticated || ['/', '/login', '/register'].includes(location.pathname);

  /* ==========================================================================
     MODE A: Public / Unauthenticated Top Header
     ========================================================================== */
  if (isPublicPage) {
    return (
      <header className="bg-[#FAFAF9] text-[#1C1917] border-b border-[#E7E5E4] sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5">
            <StatLearnLogo className="w-8 h-8" />
            <div className="flex flex-col">
              <span className="text-xs font-bold text-[#1C1917] tracking-tight leading-tight uppercase font-mono">
                StatLearn AI
              </span>
              <span className="text-[10px] text-[#78716C] leading-tight font-medium">
                MoSPI Capacity Building Portal
              </span>
            </div>
          </Link>

          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="px-3.5 py-1.5 rounded bg-[#991B1B] hover:bg-[#7F1D1D] text-white font-bold text-xs shadow-2xs transition"
              >
                Go to Dashboard
              </Link>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className={`px-3 py-1.5 rounded text-xs font-semibold transition ${
                    location.pathname === '/login'
                      ? 'bg-[#FEF3C7] text-[#1C1917] border border-[#D97706]'
                      : 'text-[#78716C] hover:text-[#1C1917] hover:bg-stone-200/50'
                  }`}
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className={`px-3 py-1.5 rounded text-xs font-semibold transition ${
                    location.pathname === '/register'
                      ? 'bg-[#991B1B] text-white font-bold'
                      : 'bg-[#FEF3C7] text-[#1C1917] border border-[#D97706] hover:bg-[#FEF3C7]/80'
                  }`}
                >
                  Register Cadre
                </Link>
              </div>
            )}
          </div>
        </div>
      </header>
    );
  }

  /* ==========================================================================
     MODE B: Authenticated Application Left Sidebar
     ========================================================================== */
  return (
    <>
      {/* Mobile Header */}
      <header className="lg:hidden sticky top-0 z-50 bg-[#FAFAF9] text-[#1C1917] border-b border-[#E7E5E4]">
        <div className="px-4 h-14 flex items-center justify-between">
          <Link to="/dashboard" className="flex items-center gap-2">
            <StatLearnLogo className="w-7 h-7" />
            <span className="text-xs font-bold text-[#1C1917] uppercase tracking-wider">StatLearn AI</span>
          </Link>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-1.5 rounded text-[#78716C] hover:text-[#1C1917] hover:bg-stone-200/50"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {/* Mobile Drawer */}
        {mobileMenuOpen && (
          <div className="bg-[#FAFAF9] px-4 pt-2 pb-4 border-t border-[#E7E5E4] space-y-3 text-xs">
            <div className="py-2 border-b border-[#E7E5E4] flex items-center gap-2">
              <div className="w-7 h-7 rounded bg-[#FEF3C7] text-[#1C1917] flex items-center justify-center font-bold text-xs border border-[#D97706]">
                {user?.full_name?.charAt(0) || 'O'}
              </div>
              <div>
                <p className="font-bold text-[#1C1917] leading-tight">{user?.full_name}</p>
                <p className="text-[10px] text-[#78716C] leading-tight">{user?.designation}</p>
              </div>
            </div>

            {navGroups.map((group, idx) => (
              <div key={idx} className="space-y-1">
                <div className="text-[10px] font-bold uppercase text-[#78716C] tracking-wider px-2 font-mono">
                  {group.groupTitle}
                </div>
                {group.links.map((link) => {
                  const Icon = link.icon;
                  const isActive = location.pathname === link.path;
                  return (
                    <Link
                      key={link.path}
                      to={link.path}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-2.5 px-3 py-1.5 rounded font-medium transition ${
                        isActive
                          ? 'bg-[#FEF3C7] text-[#1C1917] font-bold border-l-4 border-l-[#991B1B]'
                          : 'text-[#78716C] hover:bg-stone-200/50 hover:text-[#1C1917]'
                      }`}
                    >
                      <Icon className={`w-4 h-4 ${isActive ? 'text-[#991B1B]' : 'text-[#78716C]'}`} />
                      <span>{link.name}</span>
                    </Link>
                  );
                })}
              </div>
            ))}

            <div className="pt-2 border-t border-[#E7E5E4]">
              <button
                onClick={() => { setMobileMenuOpen(false); handleLogout(); }}
                className="w-full text-left flex items-center gap-2 px-3 py-1.5 text-[#991B1B] font-semibold"
              >
                <LogOut className="w-4 h-4" /> Sign Out
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Desktop Fixed Left Sidebar Layout (CRISP ACADEMIC JOURNAL THEME) */}
      <aside className="hidden lg:flex flex-col w-64 bg-[#FAFAF9] text-[#1C1917] min-h-screen fixed left-0 top-0 bottom-0 z-40 border-r border-[#E7E5E4] justify-between overflow-y-auto">
        <div className="p-4 space-y-4">
          <Link to="/dashboard" className="flex items-center gap-2.5 pb-2 border-b border-[#E7E5E4]">
            <StatLearnLogo className="w-8 h-8 flex-shrink-0" />
            <div className="flex flex-col">
              <span className="text-sm font-extrabold text-[#1C1917] tracking-tight uppercase font-mono">StatLearn AI</span>
              <span className="text-[10px] text-[#78716C] font-semibold">MoSPI Capacity Portal</span>
            </div>
          </Link>

          <div className="space-y-4">
            {navGroups.map((group, idx) => (
              <div key={idx} className="space-y-1">
                <div className="text-[10px] font-extrabold uppercase text-[#78716C] tracking-wider px-2 mb-1 font-mono">
                  {group.groupTitle}
                </div>
                {group.links.map((link) => {
                  const Icon = link.icon;
                  const isActive = location.pathname === link.path || location.pathname.startsWith(`${link.path}/`);
                  return (
                    <Link
                      key={link.path}
                      to={link.path}
                      className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded text-xs font-semibold transition ${
                        isActive
                          ? 'bg-[#FEF3C7] text-[#1C1917] font-extrabold border-l-4 border-l-[#991B1B] shadow-2xs'
                          : 'text-[#78716C] hover:bg-stone-200/50 hover:text-[#1C1917]'
                      }`}
                    >
                      <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-[#991B1B]' : 'text-[#78716C]'}`} />
                      <span>{link.name}</span>
                    </Link>
                  );
                })}
              </div>
            ))}
          </div>
        </div>

        <div className="p-3 border-t border-[#E7E5E4] bg-[#FAFAF9] space-y-2">
          <div className="flex items-center justify-between bg-white p-2 rounded border border-[#E7E5E4] shadow-2xs">
            <div className="flex items-center gap-2 overflow-hidden">
              <div className="w-7 h-7 rounded-full bg-[#FEF3C7] text-[#1C1917] flex items-center justify-center font-bold text-xs flex-shrink-0 border border-[#D97706]">
                {user?.full_name?.charAt(0) || 'O'}
              </div>
              <div className="truncate">
                <p className="text-xs font-bold text-[#1C1917] truncate">{user?.full_name}</p>
                <p className="text-[10px] text-[#78716C] truncate">{user?.designation || 'Officer'}</p>
              </div>
            </div>

            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-1 text-[#78716C] hover:text-[#991B1B] hover:bg-[#FEE2E2] rounded transition"
            >
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
};
