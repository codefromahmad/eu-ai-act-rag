import { ArrowRight, FileText, LoaderCircle, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getAnalyses } from "../services/api";

export default function Analyses() {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getAnalyses();

        setAnalyses(data);
      } catch (err) {
        setError(
          err?.response?.data?.detail || "Could not load previous analyses.",
        );
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-5 py-12 lg:px-8">
      <div>
        <div className="text-sm font-medium text-primary">
          Saved assessments
        </div>

        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-navy">
          Analysis history
        </h1>

        <p className="mt-2 text-sm text-text-secondary">
          Review previously generated compliance assessments.
        </p>
      </div>

      {loading && (
        <div className="flex min-h-72 items-center justify-center">
          <LoaderCircle className="animate-spin text-primary" size={28} />
        </div>
      )}

      {error && (
        <div className="mt-8 rounded-xl border border-red-200 bg-danger-bg px-4 py-3 text-sm text-danger">
          {error}
        </div>
      )}

      {!loading && !error && analyses.length === 0 && (
        <div className="mt-10 rounded-2xl border border-dashed border-border-strong bg-white px-6 py-14 text-center">
          <FileText size={30} className="mx-auto text-text-muted" />

          <div className="mt-4 font-semibold text-text-primary">
            No analyses yet
          </div>

          <p className="mt-2 text-sm text-text-muted">
            Your completed assessments will appear here.
          </p>

          <Link
            to="/"
            className="mt-5 inline-flex rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-hover"
          >
            Start an analysis
          </Link>
        </div>
      )}

      {!loading && analyses.length > 0 && (
        <div className="mt-8 overflow-hidden rounded-2xl border border-border-light bg-white shadow-sm">
          {analyses.map((analysis, index) => (
            <Link
              key={analysis.analysis_id}
              to={`/analyses/${analysis.analysis_id}`}
              className={[
                "flex flex-col gap-4 p-5 transition hover:bg-surface-secondary/60",
                "sm:flex-row sm:items-center sm:justify-between",
                index !== analyses.length - 1
                  ? "border-b border-border-light"
                  : "",
              ].join(" ")}
            >
              <div className="flex min-w-0 items-center gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-primary">
                  <ShieldCheck size={18} />
                </div>

                <div className="min-w-0">
                  <div className="truncate text-sm font-semibold text-text-primary">
                    {analysis.filename}
                  </div>

                  <div className="mt-1 text-xs text-text-muted">
                    {analysis.file_type?.toUpperCase()} ·{" "}
                    {analysis.risk_category?.replaceAll("_", " ")}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-5">
                <div className="text-right">
                  <div className="text-sm font-semibold text-navy">
                    {analysis.compliance_score ?? 0}%
                  </div>

                  <div className="text-xs text-text-muted">
                    Coverage {analysis.coverage ?? 0}%
                  </div>
                </div>

                <ArrowRight size={17} className="text-text-muted" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
