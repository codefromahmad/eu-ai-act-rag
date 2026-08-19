import { ArrowLeft, LoaderCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { getAnalysis } from "../services/api";

export default function AnalysisDetail() {
  const { analysisId } = useParams();
  const navigate = useNavigate();

  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getAnalysis(analysisId);

        setAnalysis(data);
      } catch (err) {
        setError(
          err?.response?.data?.detail || "Could not load this analysis.",
        );
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [analysisId]);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <LoaderCircle size={30} className="animate-spin text-primary" />
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="mx-auto max-w-3xl px-5 py-20 text-center">
        <h1 className="text-2xl font-semibold text-navy">
          Analysis unavailable
        </h1>

        <p className="mt-2 text-text-secondary">{error}</p>

        <Link
          to="/analyses"
          className="mt-6 inline-flex rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-hover"
        >
          Back to history
        </Link>
      </div>
    );
  }

  const reportData = {
    analysis_id: analysis.analysis_id,
    filename: analysis.filename,
    file_type: analysis.file_type,
    system_profile: analysis.system_profile,
    report: analysis.report,
  };

  const report = analysis.report;

  return (
    <div className="mx-auto max-w-7xl px-5 py-10 lg:px-8">
      <button
        type="button"
        onClick={() => navigate("/analyses")}
        className="inline-flex items-center gap-2 text-sm font-medium text-text-muted hover:text-text-primary"
      >
        <ArrowLeft size={16} />
        Analysis history
      </button>

      <div className="mt-6 rounded-2xl border border-border-light bg-white p-6 shadow-sm">
        <div className="text-xs font-semibold uppercase tracking-[0.12em] text-primary">
          Saved analysis
        </div>

        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-navy">
          {analysis.filename}
        </h1>

        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          <div>
            <div className="text-xs text-text-muted">Risk category</div>

            <div className="mt-1 text-sm font-semibold text-text-primary">
              {analysis.risk_category?.replaceAll("_", " ")}
            </div>
          </div>

          <div>
            <div className="text-xs text-text-muted">Compliance score</div>

            <div className="mt-1 text-sm font-semibold text-text-primary">
              {analysis.compliance_score}%
            </div>
          </div>

          <div>
            <div className="text-xs text-text-muted">Coverage</div>

            <div className="mt-1 text-sm font-semibold text-text-primary">
              {analysis.coverage}%
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={() =>
            navigate("/report", {
              state: {
                reportData,
              },
            })
          }
          className="mt-6 rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-hover"
        >
          Open full report
        </button>
      </div>

      <div className="mt-6 rounded-2xl border border-border-light bg-white p-6 shadow-sm">
        <h2 className="font-semibold text-text-primary">Executive summary</h2>

        <p className="mt-3 text-sm leading-7 text-text-secondary">
          {report?.summary?.executive_summary}
        </p>
      </div>
    </div>
  );
}
