import React from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { Shield } from 'lucide-react'

const SEGMENTS = [
  { label: 'Collateral', path: '/assetsafe/collateral' },
  { label: 'HP', path: '/assetsafe/hire-purchase' },
  { label: 'Registry', path: '/assetsafe/registry' },
] as const

export default function AssetSafeLayout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-[#f0f2f5]">
      {/* ── Top brand bar ── */}
      <header className="bg-[#0d1f3c] px-6 py-0 shadow-md">
        <div className="flex items-center gap-0">
          {/* Brand */}
          <div className="flex items-center gap-2 px-4 py-3 border-r border-white/10 mr-2">
            <Shield className="h-5 w-5 text-[#1a9aad]" />
            <span className="text-lg font-bold tracking-widest text-white">ASSETSAFE</span>
          </div>

          {/* Segment tabs */}
          <nav className="flex h-full">
            {SEGMENTS.map(({ label, path }) => {
              const isActive = location.pathname.startsWith(path)
              return (
                <NavLink
                  key={path}
                  to={path}
                  className={cn(
                    'flex items-center px-6 py-3 text-sm font-medium transition-colors',
                    'border-b-2 border-transparent hover:text-white',
                    isActive
                      ? 'border-b-2 border-[#1a9aad] text-white bg-white/5'
                      : 'text-slate-400 hover:bg-white/5',
                  )}
                >
                  {label}
                </NavLink>
              )
            })}
          </nav>
        </div>
      </header>

      {/* ── Page content ── */}
      <main className="p-5">
        <Outlet />
      </main>
    </div>
  )
}
