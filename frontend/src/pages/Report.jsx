import {
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  CircleHelp,
  FileText,
  ShieldAlert,
  ShieldCheck,
  XCircle,
} from "lucide-react";
import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

const cleanLegalText = (text = "") => {
  return (
    text
      // Remove page footer/header noise.
      .replace(/\d+\/144\s+ELI:.*$/gm, "")
      .replace(/^ELI:.*$/gm, "")
      .replace(/^OJ L,.*$/gm, "")
      .replace(/^EN\s*$/gm, "")

      // Remove excessive spaces.
      .replace(/[ \t]+/g, " ")

      // Remove too many blank lines.
      .replace(/\n{3,}/g, "\n\n")

      // Join broken PDF lines that are really the same paragraph.
      .replace(/([a-zA-Z0-9,;:])\n(?=[a-z])/g, "$1 ")

      // Keep numbered / lettered legal points on their own lines.
      .replace(/\n\s*(\d+\.)\s*/g, "\n\n$1 ")
      .replace(/\n\s*(\([a-z]\))\s*/g, "\n\n$1 ")

      .trim()
  );
};

const statusStyles = {
  compliant: {
    label: "Compliant",
    icon: CheckCircle2,
    className: "bg-success-bg text-success border-green-200",
  },
  partial: {
    label: "Partial",
    icon: AlertTriangle,
    className: "bg-warning-bg text-warning border-amber-200",
  },
  non_compliant: {
    label: "Non-compliant",
    icon: XCircle,
    className: "bg-danger-bg text-danger border-red-200",
  },
  unknown: {
    label: "Unknown",
    icon: CircleHelp,
    className: "bg-surface-secondary text-text-muted border-border-light",
  },
};

const formatLabel = (value) => {
  if (!value) return "Unknown";

  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

function ScoreCard({ label, value, subtitle }) {
  const safeValue = Number.isFinite(Number(value)) ? Number(value) : 0;

  return (
    <div className="rounded-2xl border border-border-light bg-white p-5 shadow-sm">
      <div className="text-sm font-medium text-text-muted">{label}</div>

      <div className="mt-3 text-4xl font-semibold tracking-tight text-navy">
        {safeValue}%
      </div>

      <div className="mt-4 h-2 overflow-hidden rounded-full bg-surface-secondary">
        <div
          className="h-full rounded-full bg-primary"
          style={{
            width: `${Math.min(safeValue, 100)}%`,
          }}
        />
      </div>

      <div className="mt-3 text-xs leading-5 text-text-muted">{subtitle}</div>
    </div>
  );
}

function ListCard({ title, items = [] }) {
  return (
    <div className="rounded-2xl border border-border-light bg-white p-5 shadow-sm">
      <h3 className="font-semibold text-text-primary">{title}</h3>

      {items.length === 0 ? (
        <p className="mt-3 text-sm text-text-muted">No items reported.</p>
      ) : (
        <ul className="mt-4 space-y-3">
          {items.map((item, index) => (
            <li
              key={`${item}-${index}`}
              className="flex gap-3 text-sm leading-6 text-text-secondary"
            >
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function LegalReference({ reference }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="overflow-hidden rounded-xl border border-border-light bg-white">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="flex w-full items-center justify-between gap-4 px-4 py-3 text-left hover:bg-surface-secondary/60"
      >
        <div>
          <div className="text-sm font-semibold text-text-primary">
            {reference.article || "Legal reference"}
          </div>

          <div className="mt-1 text-xs text-text-muted">EU AI Act source</div>
        </div>

        {open ? (
          <ChevronUp size={17} className="shrink-0 text-text-muted" />
        ) : (
          <ChevronDown size={17} className="shrink-0 text-text-muted" />
        )}
      </button>

      {open && (
        <div className="max-h-96 overflow-y-auto rounded-lg bg-white px-5 py-4 text-sm leading-7 text-text-secondary">
          <div className="whitespace-pre-line">
            {reference.text
              ? cleanLegalText(reference.text)
              : "No legal text available."}
          </div>
        </div>
      )}
    </div>
  );
}

function RequirementCard({ assessment }) {
  const style = statusStyles[assessment.status] || statusStyles.unknown;

  const Icon = style.icon;

  return (
    <div className="rounded-2xl border border-border-light bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <div className="text-xs font-semibold uppercase tracking-[0.12em] text-text-muted">
            {assessment.requirement_id}
          </div>

          <p className="mt-2 text-sm leading-6 text-text-secondary">
            {assessment.explanation}
          </p>
        </div>

        <div
          className={`inline-flex w-fit shrink-0 items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-semibold ${style.className}`}
        >
          <Icon size={14} />
          {style.label}
        </div>
      </div>

      {assessment.user_evidence?.length > 0 && (
        <div className="mt-5 border-t border-border-light pt-4">
          <div className="text-xs font-semibold uppercase tracking-[0.1em] text-text-muted">
            User evidence
          </div>

          <div className="mt-3 space-y-2">
            {assessment.user_evidence.map((evidence, index) => (
              <div
                key={index}
                className="rounded-xl border border-border-light bg-surface-secondary/60 px-3 py-3 text-sm leading-6 text-text-secondary"
              >
                {typeof evidence === "string"
                  ? evidence
                  : evidence.quote || evidence.value || "Evidence available"}
              </div>
            ))}
          </div>
        </div>
      )}

      {assessment.legal_references?.length > 0 && (
        <div className="mt-5 border-t border-border-light pt-4">
          <div className="text-xs font-semibold uppercase tracking-[0.1em] text-text-muted">
            Legal references
          </div>

          <div className="mt-3 space-y-2">
            {assessment.legal_references.map((reference, index) => (
              <LegalReference
                key={`${reference.article}-${index}`}
                reference={reference}
              />
            ))}
          </div>
        </div>
      )}

      {assessment.recommendations?.length > 0 && (
        <div className="mt-5 border-t border-border-light pt-4">
          <div className="text-xs font-semibold uppercase tracking-[0.1em] text-text-muted">
            Recommendations
          </div>

          <ul className="mt-3 space-y-2">
            {assessment.recommendations.map((recommendation, index) => (
              <li
                key={index}
                className="flex gap-2 text-sm leading-6 text-text-secondary"
              >
                <span className="text-primary">•</span>

                <span>{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function Report() {
  const location = useLocation();
  const navigate = useNavigate();

  const data = location.state?.reportData;

  if (!data) {
    return (
      <div className="mx-auto max-w-3xl px-5 py-20 text-center">
        <FileText size={36} className="mx-auto text-text-muted" />

        <h1 className="mt-5 text-2xl font-semibold text-navy">
          No report loaded
        </h1>

        <p className="mt-2 text-text-secondary">
          Upload a document first or open a saved analysis.
        </p>

        <Link
          to="/"
          className="mt-6 inline-flex rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-primary-hover"
        >
          Analyze a document
        </Link>
      </div>
    );
  }

  const report = data.report || {};

  const risk = report.risk_classification || {};

  const score = report.score || {};

  const summary = report.summary || {};

  const assessments = report.assessments || [];

  return (
    <div className="mx-auto max-w-7xl px-5 py-10 lg:px-8 lg:py-14">
      <button
        type="button"
        onClick={() => navigate("/")}
        className="mb-6 inline-flex items-center gap-2 text-sm font-medium text-text-muted hover:text-text-primary"
      >
        <ArrowLeft size={16} />
        New analysis
      </button>

      <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <div className="text-sm font-medium text-primary">
            Compliance assessment
          </div>

          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-navy">
            {data.filename}
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-text-secondary">
            Preliminary evidence-based assessment against relevant EU AI Act
            requirements.
          </p>
        </div>

        <div className="inline-flex w-fit items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-semibold text-primary">
          <ShieldAlert size={17} />
          {formatLabel(risk.category)}
        </div>
      </div>

      <div className="mt-8 grid gap-4 md:grid-cols-2">
        <ScoreCard
          label="Compliance score"
          value={score.compliance_score}
          subtitle="Performance across requirements where enough evidence was available."
        />

        <ScoreCard
          label="Evidence coverage"
          value={score.coverage}
          subtitle="Percentage of applicable requirements that could be meaningfully assessed."
        />
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          {
            label: "Compliant",
            value: score.compliant ?? 0,
            className: "text-success",
          },
          {
            label: "Partial",
            value: score.partial ?? 0,
            className: "text-warning",
          },
          {
            label: "Non-compliant",
            value: score.non_compliant ?? 0,
            className: "text-danger",
          },
          {
            label: "Unknown",
            value: score.unknown ?? 0,
            className: "text-text-muted",
          },
        ].map((item) => (
          <div
            key={item.label}
            className="rounded-xl border border-border-light bg-white p-4 shadow-sm"
          >
            <div className={`text-2xl font-semibold ${item.className}`}>
              {item.value}
            </div>

            <div className="mt-1 text-xs font-medium text-text-muted">
              {item.label}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 rounded-2xl border border-border-light bg-white p-6 shadow-sm">
        <div className="flex items-center gap-2">
          <ShieldCheck size={18} className="text-primary" />

          <h2 className="font-semibold text-text-primary">Executive summary</h2>
        </div>

        <p className="mt-4 text-sm leading-7 text-text-secondary">
          {summary.executive_summary || "No executive summary available."}
        </p>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <ListCard title="Strengths" items={summary.strengths || []} />

        <ListCard title="Weaknesses" items={summary.weaknesses || []} />

        <ListCard
          title="Missing information"
          items={summary.missing_information || []}
        />

        <ListCard
          title="Recommendations"
          items={summary.recommendations || []}
        />
      </div>

      <div className="mt-10">
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-navy">
            Requirement assessment
          </h2>

          <p className="mt-1 text-sm text-text-muted">
            Detailed evaluation against each applicable requirement.
          </p>
        </div>

        {assessments.length === 0 ? (
          <div className="rounded-2xl border border-border-light bg-white p-6 text-sm text-text-muted shadow-sm">
            No requirement assessments are available.
          </div>
        ) : (
          <div className="space-y-4">
            {assessments.map((assessment) => (
              <RequirementCard
                key={assessment.requirement_id}
                assessment={assessment}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
