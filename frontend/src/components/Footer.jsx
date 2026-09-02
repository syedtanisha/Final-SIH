import React from 'react';

export const Footer = () => {
  return (
    <footer className="bg-white border-t border-[#E7E5E4] py-4 mt-8 text-xs text-[#78716C]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-2">
        <div>
          <p className="font-semibold text-[#1C1917]">
            MoSPI Capacity Building Portal · Aligned with MoSPI and NSSTA Standards
          </p>
        </div>
        <div className="flex items-center gap-4 text-[11px]">
          <a href="https://www.mospi.gov.in/" target="_blank" rel="noopener noreferrer" className="hover:text-[#991B1B] transition underline font-medium">
            MoSPI Portal
          </a>
          <span>·</span>
          <a href="https://esankhyiki.mospi.gov.in/" target="_blank" rel="noopener noreferrer" className="hover:text-[#991B1B] transition underline font-medium">
            eSankhyiki Data
          </a>
          <span>·</span>
          <span>© 2026 StatLearn Team</span>
        </div>
      </div>
    </footer>
  );
};
