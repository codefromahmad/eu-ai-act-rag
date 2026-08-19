import { FileSearch, History, ShieldCheck } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const navItemClass = ({ isActive }) =>
  [
    "flex items-center gap-2 rounded-lg px-3 py-2",
    "text-sm font-medium transition-colors",
    isActive
      ? "bg-surface-secondary text-text-primary"
      : "text-text-muted hover:bg-surface-secondary hover:text-text-primary",
  ].join(" ");

export default function Layout() {
  return (
    <div className="min-h-screen bg-app-bg">
      <header className="sticky top-0 z-50 border-b border-border-light bg-white/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 lg:px-8">
          <NavLink to="/" className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-navy text-white">
              <ShieldCheck size={20} />
            </div>

            <div>
              <div className="text-sm font-semibold tracking-tight text-text-primary">
                AI Act Compass
              </div>

              <div className="hidden text-xs text-text-muted sm:block">
                EU AI Act Compliance
              </div>
            </div>
          </NavLink>

          <nav className="flex items-center gap-1">
            <NavLink to="/" end className={navItemClass}>
              <FileSearch size={17} />

              <span className="hidden sm:inline">Analyze</span>
            </NavLink>

            <NavLink to="/analyses" className={navItemClass}>
              <History size={17} />

              <span className="hidden sm:inline">History</span>
            </NavLink>
          </nav>
        </div>
      </header>

      <main>
        <Outlet />
      </main>

      <footer className="border-t border-border-light bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-2 px-5 py-6 text-xs text-text-muted sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <span>AI-assisted preliminary EU AI Act assessment</span>

          <span>Not a substitute for professional legal advice.</span>
        </div>
      </footer>
    </div>
  );
}
