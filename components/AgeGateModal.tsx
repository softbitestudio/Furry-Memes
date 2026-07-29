'use client';

import { useState, useEffect } from 'react';

export default function AgeGateModal() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Check if the age_verified cookie exists
    const hasVerified = document.cookie
      .split('; ')
      .some((item) => item.trim().startsWith('age_verified=true'));

    // Only open modal on client mount if no cookie is found (prevents SSR hydration errors)
    if (!hasVerified) {
      setIsOpen(true);
    }
  }, []);

  const handleAccept = () => {
    // Set consent cookie persistent for 30 days (2,592,000 seconds)
    document.cookie = "age_verified=true; max-age=2592000; path=/; SameSite=Lax; Secure";
    setIsOpen(false);
  };

  const handleDecline = () => {
    // Bounce unverified or under-age visitors back to the SFW site
    window.location.href = 'https://furrymemes.com';
  };

  // If already verified or SSR, render nothing
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-in fade-in duration-200">
      <div className="w-full max-w-md rounded-2xl bg-neutral-900 border border-neutral-800 p-6 sm:p-8 text-center shadow-2xl">
        <div className="text-4xl mb-3">🔞</div>
        
        <h2 className="text-2xl font-bold text-white tracking-tight">
          18+ Age Verification
        </h2>
        
        <p className="mt-3 text-sm text-neutral-400 leading-relaxed">
          <strong className="text-neutral-200">furrymemes.net</strong> contains adult and explicit memes. By entering, you confirm you are at least 18 years of age or the legal age of majority in your region.
        </p>

        <div className="mt-6 flex flex-col gap-3">
          <button
            onClick={handleAccept}
            className="w-full py-3 px-4 rounded-xl font-semibold text-white bg-red-600 hover:bg-red-500 active:scale-[0.98] transition-all shadow-lg shadow-red-600/25"
          >
            I am 18 or older — Enter
          </button>
          
          <button
            onClick={handleDecline}
            className="w-full py-3 px-4 rounded-xl font-medium text-neutral-400 bg-neutral-800 hover:bg-neutral-700 hover:text-white transition-all"
          >
            Take me to furrymemes.com (SFW)
          </button>
        </div>

        <p className="mt-5 text-[11px] text-neutral-500">
          A necessary functional cookie is set upon entry to remember your choice for 30 days.
        </p>
      </div>
    </div>
  );
}
