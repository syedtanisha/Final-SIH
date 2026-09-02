import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  CheckCircle2, 
  BookOpen, 
  Sparkles, 
  ExternalLink, 
  Clock, 
  TrendingUp, 
  X, 
  ChevronDown, 
  Check 
} from 'lucide-react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
  Legend
} from 'recharts';

/* ==========================================================================
   1. SearchableDropdown Component (Option 3 Academic Theme)
   ========================================================================== */
export const SearchableDropdown = ({
  label,
  options = [],
  value = '',
  onChange,
  placeholder = 'Type to search...',
  name,
  icon: Icon,
  required = false,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState(value);
  const dropdownRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    setSearchTerm(value);
  }, [value]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
        if (!searchTerm && value) {
          setSearchTerm(value);
        }
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [searchTerm, value]);

  const filteredOptions = options.filter((opt) =>
    opt.toLowerCase().includes((searchTerm || '').toLowerCase().trim())
  );

  const handleSelect = (option) => {
    setSearchTerm(option);
    onChange({ target: { name, value: option } });
    setIsOpen(false);
  };

  const handleInputChange = (e) => {
    const val = e.target.value;
    setSearchTerm(val);
    onChange({ target: { name, value: val } });
    if (!isOpen) setIsOpen(true);
  };

  const handleClear = (e) => {
    e.stopPropagation();
    setSearchTerm('');
    onChange({ target: { name, value: '' } });
    inputRef.current?.focus();
    setIsOpen(true);
  };

  return (
    <div className="relative space-y-1 text-xs" ref={dropdownRef}>
      {label && (
        <label className="block font-semibold text-[#1C1917]">
          {label} {required && <span className="text-[#991B1B]">*</span>}
        </label>
      )}

      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none text-[#78716C]">
            <Icon className="w-3.5 h-3.5" />
          </div>
        )}

        <input
          ref={inputRef}
          type="text"
          name={name}
          value={searchTerm}
          onChange={handleInputChange}
          onFocus={() => setIsOpen(true)}
          placeholder={placeholder}
          required={required}
          autoComplete="off"
          className={`w-full ${Icon ? 'pl-8' : 'pl-3'} pr-8 py-2 border border-[#E7E5E4] rounded bg-white outline-none focus:border-[#991B1B] text-[#1C1917] ${
            isOpen ? 'border-[#991B1B]' : ''
          }`}
        />

        <div className="absolute inset-y-0 right-0 pr-2 flex items-center gap-1">
          {searchTerm && (
            <button
              type="button"
              onClick={handleClear}
              className="p-0.5 text-[#78716C] hover:text-[#1C1917] rounded"
              title="Clear selection"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className="p-0.5 text-[#78716C] hover:text-[#1C1917] rounded"
          >
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isOpen ? 'rotate-180 text-[#991B1B]' : ''}`} />
          </button>
        </div>
      </div>

      {isOpen && (
        <div className="absolute z-50 mt-1 w-full bg-white border border-[#E7E5E4] rounded shadow-md max-h-56 overflow-y-auto py-1 text-xs divide-y divide-[#E7E5E4]">
          <div className="px-3 py-1 bg-[#FAFAF9] border-b border-[#E7E5E4] text-[10px] text-[#78716C] font-bold uppercase font-mono">
            <span>{filteredOptions.length} option{filteredOptions.length === 1 ? '' : 's'}</span>
          </div>

          {filteredOptions.length > 0 ? (
            filteredOptions.map((option, idx) => {
              const isSelected = option.toLowerCase() === (value || '').toLowerCase();
              return (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelect(option)}
                  className={`w-full text-left px-3 py-1.5 flex items-center justify-between transition hover:bg-[#FEF3C7] hover:text-[#1C1917] ${
                    isSelected ? 'bg-[#FEF3C7] font-bold text-[#1C1917]' : 'text-[#1C1917]'
                  }`}
                >
                  <span className="pr-2">{option}</span>
                  {isSelected && <Check className="w-3.5 h-3.5 text-[#991B1B] flex-shrink-0" />}
                </button>
              );
            })
          ) : (
            <div className="px-3 py-2 text-center text-[#78716C] text-[11px]">
              No exact match found
            </div>
          )}
        </div>
      )}
    </div>
  );
};

/* ==========================================================================
   2. RadarChartComp Component (Academic Theme)
   ========================================================================== */
export const RadarChartComp = ({ competencies }) => {
  if (!competencies || competencies.length === 0) {
    return (
      <div className="h-60 flex items-center justify-center text-[#78716C] text-xs bg-[#FAFAF9] rounded border border-dashed border-[#E7E5E4]">
        No competency assessment data recorded yet.
      </div>
    );
  }

  const data = competencies.map((c) => ({
    subject: c.name.length > 18 ? c.name.substring(0, 16) + '...' : c.name,
    fullName: c.name,
    Current: c.current_level,
    Required: c.required_level,
  }));

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="68%" data={data}>
          <PolarGrid stroke="#E7E5E4" />
          <PolarAngleAxis 
            dataKey="subject" 
            tick={{ fill: '#1C1917', fontSize: 10, fontWeight: 600 }} 
          />
          <PolarRadiusAxis 
            angle={30} 
            domain={[0, 100]} 
            tick={{ fill: '#78716C', fontSize: 9 }} 
          />
          <Tooltip 
            formatter={(value, name) => [`${value}%`, name]}
            labelFormatter={(label, payload) => payload?.[0]?.payload?.fullName || label}
            contentStyle={{ backgroundColor: '#ffffff', borderColor: '#E7E5E4', borderRadius: '0.25rem', fontSize: '11px', color: '#1C1917' }}
          />
          <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
          <Radar
            name="Current Level"
            dataKey="Current"
            stroke="#991B1B"
            fill="#FEE2E2"
            fillOpacity={0.5}
          />
          <Radar
            name="Target Benchmark"
            dataKey="Required"
            stroke="#D97706"
            fill="#FEF3C7"
            fillOpacity={0.3}
            strokeDasharray="3 3"
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

/* ==========================================================================
   3. ModuleReaderModal Component
   ========================================================================== */
export const ModuleReaderModal = ({ resource, isOpen, onClose }) => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('curriculum');

  if (!isOpen || !resource) return null;

  const {
    title,
    description,
    source,
    official_url,
    difficulty,
    estimated_duration_mins,
  } = resource;

  const targetUrl = official_url && official_url.startsWith('http') 
    ? official_url 
    : 'https://www.mospi.gov.in/';

  const handleOpenPortal = (e) => {
    e.preventDefault();
    window.open(targetUrl, '_blank', 'noopener,noreferrer');
  };

  const handleLaunchQuiz = () => {
    onClose();
    navigate(`/studio?topic=${encodeURIComponent(title)}`);
  };

  const getDetailedContent = () => {
    const titleLower = (title || '').toLowerCase();
    
    if (titleLower.includes('python') || titleLower.includes('comput')) {
      return {
        subtitle: 'NSSTA Digital Data Laboratory • Practical Microdata Analytics',
        modules: [
          { title: '1. Microdata Ingestion & Chunking', desc: 'Loading multi-gigabyte survey schedules using pandas chunking, data typing, and memory optimization.' },
          { title: '2. Multiplier Expansion & Estimation', desc: 'Applying sampling weights to unit records to estimate population counts, totals, and ratios.' },
          { title: '3. Automated Quality Validation', desc: 'Writing automated assertion scripts to detect outliers and roster code inconsistencies.' },
          { title: '4. Dissemination & Reporting', desc: 'Generating automated summary bulletins and visualizations with NumPy and Matplotlib.' }
        ],
        formulas: [
          {
            name: 'Weighted Population Total Estimator',
            display: 'Ŷ = Σ (w_i × y_i)',
            variables: [
              { sym: 'Ŷ', desc: 'Estimated population aggregate total' },
              { sym: 'w_i', desc: 'Sampling multiplier / design weight for sample unit i' },
              { sym: 'y_i', desc: 'Observed value of the variable' }
            ]
          }
        ]
      };
    }
    
    return {
      subtitle: 'NSSTA & MoSPI Official Curriculum • Official Survey Design',
      modules: [
        { title: '1. Multi-Stage Stratified Sampling Frame', desc: 'Selection of Census Villages/UFS blocks as FSUs and households as USUs.' },
        { title: '2. Questionnaire Design & Reference Periods', desc: 'Canvassing structured schedules under Usual Principal Status (UPSS) and Current Weekly Status (CWS).' },
        { title: '3. National Quality Assurance (UN NQAF)', desc: 'Validating impartiality, methodology, transparent metadata, and respondent confidentiality safeguards.' }
      ],
      formulas: [
        {
          name: 'Stratified Sample Variance Formula',
          display: 'Var(ȳ_st) = Σ [ W_h² × (S_h² / n_h) × (1 - f_h) ]',
          variables: [
            { sym: 'W_h', desc: 'Stratum population weight' },
            { sym: 'S_h²', desc: 'Variance of the variable in stratum h' }
          ]
        }
      ]
    };
  };

  const details = getDetailedContent();

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-stone-900/50">
      <div className="bg-white rounded-lg border border-[#E7E5E4] shadow-xl w-full max-w-xl max-h-[85vh] flex flex-col overflow-hidden text-xs">
        
        {/* Modal Header */}
        <div className="bg-[#FAFAF9] text-[#1C1917] p-4 border-b border-[#E7E5E4] relative">
          <button
            onClick={onClose}
            className="absolute top-3.5 right-3.5 p-1 text-[#78716C] hover:text-[#1C1917] rounded"
          >
            <X className="w-4 h-4" />
          </button>

          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[#FEF3C7] text-[#1C1917] border border-[#D97706] uppercase">
              {source}
            </span>
            <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-[#FEE2E2] text-[#991B1B] border border-[#FCA5A5]">
              {difficulty}
            </span>
            {estimated_duration_mins && (
              <span className="text-[11px] text-[#78716C] flex items-center gap-1">
                <Clock className="w-3 h-3 text-[#D97706]" /> {estimated_duration_mins}m
              </span>
            )}
          </div>

          <h2 className="text-sm font-extrabold text-[#1C1917]">
            {title}
          </h2>
          <p className="text-[11px] text-[#78716C] mt-0.5">
            {details.subtitle}
          </p>
        </div>

        {/* Modal Navigation */}
        <div className="flex border-b border-[#E7E5E4] bg-[#FAFAF9] px-4 pt-2 gap-4 font-semibold text-xs font-mono">
          <button
            onClick={() => setActiveTab('curriculum')}
            className={`pb-2 border-b-2 transition ${
              activeTab === 'curriculum'
                ? 'border-[#991B1B] text-[#1C1917] font-bold'
                : 'border-transparent text-[#78716C] hover:text-[#1C1917]'
            }`}
          >
            Syllabus
          </button>
          <button
            onClick={() => setActiveTab('methodology')}
            className={`pb-2 border-b-2 transition ${
              activeTab === 'methodology'
                ? 'border-[#991B1B] text-[#1C1917] font-bold'
                : 'border-transparent text-[#78716C] hover:text-[#1C1917]'
            }`}
          >
            Formulas & SOPs
          </button>
          <button
            onClick={() => setActiveTab('practice')}
            className={`pb-2 border-b-2 transition ${
              activeTab === 'practice'
                ? 'border-[#991B1B] text-[#1C1917] font-bold'
                : 'border-transparent text-[#78716C] hover:text-[#1C1917]'
            }`}
          >
            AI Practice
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-4 overflow-y-auto space-y-3 flex-1 text-[#1C1917]">
          {activeTab === 'curriculum' && (
            <div className="space-y-3">
              <p className="text-xs bg-[#FAFAF9] p-3 rounded border border-[#E7E5E4]">{description}</p>
              <h4 className="font-bold text-[#1C1917] uppercase text-[11px] font-mono">Syllabus Modules</h4>
              <div className="space-y-2">
                {details.modules.map((m, idx) => (
                  <div key={idx} className="p-2.5 rounded border border-[#E7E5E4] bg-white">
                    <h5 className="font-bold text-[#1C1917]">{m.title}</h5>
                    <p className="text-[11px] text-[#78716C] mt-0.5">{m.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'methodology' && (
            <div className="space-y-3">
              {details.formulas.map((item, idx) => (
                <div key={idx} className="rounded border border-[#E7E5E4] overflow-hidden bg-white">
                  <div className="bg-[#FAFAF9] px-3 py-1.5 border-b border-[#E7E5E4] font-bold text-[#1C1917]">
                    {item.name}
                  </div>
                  <div className="bg-[#FEF3C7] text-[#1C1917] p-2.5 font-mono text-center font-bold">
                    {item.display}
                  </div>
                  <div className="p-3 space-y-1 text-[11px]">
                    {item.variables.map((v, vIdx) => (
                      <div key={vIdx} className="flex items-start gap-2">
                        <span className="font-mono font-bold text-[#1C1917]">{v.sym}:</span>
                        <span className="text-[#78716C]">{v.desc}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'practice' && (
            <div className="text-center py-6 space-y-2">
              <h4 className="text-xs font-bold text-[#1C1917]">Generate Practice Quiz</h4>
              <p className="text-[#78716C] max-w-xs mx-auto">
                Generate an AI assessment based on "{title}".
              </p>
              <button
                onClick={handleLaunchQuiz}
                className="px-4 py-2 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded text-xs font-bold shadow-2xs transition"
              >
                Launch AI Quiz Studio
              </button>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="bg-[#FAFAF9] px-4 py-3 border-t border-[#E7E5E4] flex items-center justify-between">
          <button
            type="button"
            onClick={handleOpenPortal}
            className="px-3 py-1.5 bg-white text-[#1C1917] border border-[#E7E5E4] rounded text-xs font-semibold hover:bg-stone-50 flex items-center gap-1"
          >
            <span>Official Portal</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={handleLaunchQuiz}
            className="px-4 py-1.5 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded text-xs font-bold shadow-2xs"
          >
            Generate AI Quiz
          </button>
        </div>
      </div>
    </div>
  );
};

/* ==========================================================================
   4. GapCard Component
   ========================================================================== */
export const GapCard = ({ gapItem }) => {
  const {
    name,
    domain,
    current_level,
    required_level,
    gap,
    priority,
    recommended_focus_action,
  } = gapItem;

  const getPriorityBadge = (p) => {
    switch (p) {
      case 'High':
        return 'bg-[#FEE2E2] text-[#991B1B] border-[#FCA5A5]';
      case 'Medium':
        return 'bg-[#FEF3C7] text-[#1C1917] border-[#D97706]';
      case 'Low':
        return 'bg-stone-100 text-[#1C1917] border-[#E7E5E4]';
      default:
        return 'bg-emerald-50 text-emerald-900 border-emerald-200';
    }
  };

  const getTopBorderClass = (p) => {
    switch (p) {
      case 'High': return 'border-t-4 border-t-[#991B1B]';
      case 'Medium': return 'border-t-4 border-t-[#D97706]';
      default: return 'border-t-4 border-t-stone-400';
    }
  };

  return (
    <div className={`bg-white rounded-lg border border-[#E7E5E4] p-4 shadow-2xs space-y-3 flex flex-col justify-between text-xs ${getTopBorderClass(priority)}`}>
      <div>
        <div className="flex items-start justify-between gap-2 mb-2">
          <div>
            <span className="text-[10px] font-bold text-[#78716C] uppercase font-mono">
              {domain}
            </span>
            <h3 className="text-xs sm:text-sm font-bold text-[#1C1917] mt-0.5">
              {name}
            </h3>
          </div>
          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded border flex-shrink-0 ${getPriorityBadge(priority)}`}>
            {priority === 'Met' ? 'Met' : `${priority} Priority`}
          </span>
        </div>

        <div className="space-y-1.5 my-2.5 bg-[#FAFAF9] p-2.5 rounded border border-[#E7E5E4] text-xs">
          <div className="flex justify-between items-center text-[#78716C]">
            <span>Assessed: <strong className="text-[#1C1917]">{current_level}%</strong></span>
            <span>Target: <strong className="text-[#1C1917]">{required_level}%</strong></span>
          </div>
          <div className="w-full bg-stone-200 rounded-full h-1.5 overflow-hidden">
            <div
              className={`h-full ${gap > 0 ? 'bg-[#991B1B]' : 'bg-emerald-600'}`}
              style={{ width: `${Math.min(100, current_level)}%` }}
            />
          </div>
          <div className="flex justify-between items-center text-[11px] text-[#78716C] pt-0.5">
            {gap > 0 ? (
              <span className="text-[#991B1B] font-bold">Gap: {gap}%</span>
            ) : (
              <span className="text-emerald-700 font-bold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> Met
              </span>
            )}
          </div>
        </div>

        <p className="text-[#78716C] leading-relaxed">
          <strong className="text-[#1C1917]">Action:</strong> {recommended_focus_action}
        </p>
      </div>

      <div className="flex items-center gap-2 pt-2.5 border-t border-[#E7E5E4]">
        <Link
          to={`/recommendations?gap=${encodeURIComponent(name)}`}
          className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-1.5 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded text-xs font-bold shadow-2xs transition"
        >
          <BookOpen className="w-3.5 h-3.5 text-[#FEF3C7]" />
          <span>Modules</span>
        </Link>
        <Link
          to={`/studio?topic=${encodeURIComponent(name)}`}
          className="inline-flex items-center justify-center p-1.5 bg-[#FEF3C7] hover:bg-[#D97706]/20 text-[#1C1917] rounded text-xs font-bold border border-[#D97706] transition"
          title="AI Quiz Studio"
        >
          <Sparkles className="w-3.5 h-3.5 text-[#991B1B]" />
        </Link>
      </div>
    </div>
  );
};

/* ==========================================================================
   5. ResourceCard Component
   ========================================================================== */
export const ResourceCard = ({ resource, relevanceReason }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const {
    title,
    description,
    source,
    difficulty,
    estimated_duration_mins,
    resource_type,
    publisher_org,
    provenance_type,
    verification_level,
  } = resource;

  return (
    <>
      <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-4 shadow-2xs space-y-2.5 flex flex-col justify-between text-xs">
        <div>
          <div className="flex flex-wrap items-center justify-between gap-1.5 mb-1.5">
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-[#FEF3C7] text-[#1C1917] border border-[#D97706] font-mono">
              {publisher_org || source || 'MoSPI Official'}
            </span>
            <span className="text-[10px] text-[#78716C] font-mono">
              {difficulty} {estimated_duration_mins && `• ${estimated_duration_mins}m`}
            </span>
          </div>

          <h3 
            onClick={() => setIsModalOpen(true)}
            className="text-xs sm:text-sm font-bold text-[#1C1917] hover:text-[#991B1B] transition cursor-pointer mb-1 leading-snug"
          >
            {title}
          </h3>

          <p className="text-[#78716C] line-clamp-3 leading-relaxed mb-2">
            {description}
          </p>

          <div className="flex flex-wrap gap-1.5 mb-2">
            {provenance_type && (
              <span className="text-[9px] px-1.5 py-0.5 rounded bg-stone-100 text-[#78716C] border border-[#E7E5E4] font-mono">
                {provenance_type}
              </span>
            )}
            {verification_level && (
              <span className="text-[9px] px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200 font-mono font-bold">
                {verification_level}
              </span>
            )}
          </div>

          {relevanceReason && (
            <div className="mb-2 bg-[#FAFAF9] p-2 rounded border border-[#E7E5E4] text-[11px] text-[#1C1917]">
              <span className="font-bold text-[#991B1B]">Gap Fit: </span>{relevanceReason}
            </div>
          )}
        </div>

        <div className="pt-2.5 border-t border-[#E7E5E4] flex items-center justify-between">
          <span className="text-[10px] text-[#78716C] font-mono">
            {resource_type ? resource_type.replace('_', ' ') : 'Module'}
          </span>
          <button
            type="button"
            onClick={() => setIsModalOpen(true)}
            className="px-3 py-1.5 bg-[#991B1B] hover:bg-[#7F1D1D] text-white rounded text-xs font-bold transition shadow-2xs"
          >
            View Details
          </button>
        </div>
      </div>

      <ModuleReaderModal
        resource={resource}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
};

/* ==========================================================================
   6. CompetencyDeltaBanner Component
   ========================================================================== */
export const CompetencyDeltaBanner = ({
  competencyName,
  beforeScore,
  afterScore,
  delta,
  quizTitle,
}) => {
  return (
    <div className="bg-white rounded-lg border border-[#E7E5E4] border-t-4 border-t-[#991B1B] p-4 shadow-2xs space-y-3 mb-6 text-xs">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#E7E5E4] pb-2">
        <div className="flex items-center gap-1.5">
          <TrendingUp className="w-4 h-4 text-[#991B1B]" />
          <span className="font-bold text-[#1C1917]">
            Verified Gain: {competencyName || 'Statistical Skill'}
          </span>
        </div>
        <span className="text-[10px] bg-[#FEF3C7] text-[#1C1917] border border-[#D97706] px-2 py-0.5 rounded font-semibold">
          Evaluated via {quizTitle || 'Quiz'}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-3 text-center">
        <div className="bg-[#FAFAF9] rounded p-2.5 border border-[#E7E5E4]">
          <p className="text-[10px] text-[#78716C]">Initial</p>
          <p className="text-lg font-bold text-[#1C1917]">{beforeScore}%</p>
        </div>
        <div className="bg-[#FEE2E2] rounded p-2.5 border border-[#FCA5A5]">
          <p className="text-[10px] text-[#991B1B] font-semibold">Gain</p>
          <p className="text-xl font-bold text-[#991B1B]">+{delta}%</p>
        </div>
        <div className="bg-[#FEF3C7] rounded p-2.5 border border-[#D97706]">
          <p className="text-[10px] text-[#1C1917] font-semibold">Updated Level</p>
          <p className="text-lg font-bold text-[#1C1917]">{afterScore}%</p>
        </div>
      </div>
    </div>
  );
};
