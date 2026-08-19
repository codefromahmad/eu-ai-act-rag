import {
  ArrowRight,
  Check,
  FileText,
  LoaderCircle,
  ShieldCheck,
  Upload,
  X,
} from "lucide-react";
import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import { createReport } from "../services/api";

const supportedExtensions = [".pdf", ".docx", ".txt", ".md"];

export default function Home() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const selectFile = (selectedFile) => {
    if (!selectedFile) return;

    const extension = "." + selectedFile.name.split(".").pop().toLowerCase();

    if (!supportedExtensions.includes(extension)) {
      setError("Supported formats are PDF, DOCX, TXT and Markdown.");
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError("The maximum supported file size is 10 MB.");
      return;
    }

    setError("");
    setFile(selectedFile);
  };

  const handleAnalyze = async () => {
    if (!file || loading) return;

    try {
      setLoading(true);
      setError("");

      const result = await createReport(file);

      navigate("/report", {
        state: {
          reportData: result,
        },
      });
    } catch (err) {
      const status = err?.response?.status;
      const detail = err?.response?.data?.detail;

      if (status === 503) {
        setError(
          "The AI service is temporarily unavailable or has reached its usage quota. Please try again later.",
        );
      } else if (status === 429) {
        setError(
          "Too many requests were sent to the AI service. Please try again shortly.",
        );
      } else if (!err?.response) {
        setError(
          "The backend could not be reached. Make sure the API server is running.",
        );
      } else {
        setError(
          detail || "We could not analyze this document. Please try again.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-5 py-14 lg:px-8 lg:py-20">
      <div className="mx-auto max-w-3xl text-center">
        <div className="mx-auto mb-5 flex w-fit items-center gap-2 rounded-full border border-border-light bg-white px-3 py-1.5 text-xs font-medium text-text-secondary shadow-sm">
          <ShieldCheck size={14} className="text-primary" />
          EU AI Act assessment workspace
        </div>

        <h1 className="text-4xl font-semibold tracking-[-0.04em] text-navy sm:text-5xl lg:text-[56px] lg:leading-[1.05]">
          Understand your AI system’s
          <span className="text-primary"> compliance posture.</span>
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-base leading-7 text-text-secondary sm:text-lg">
          Upload your AI system documentation and receive an evidence-based
          preliminary assessment against relevant EU AI Act requirements.
        </p>
      </div>

      <div className="mx-auto mt-12 max-w-2xl">
        <div className="rounded-2xl border border-border-light bg-white p-5 shadow-[0_10px_40px_rgba(15,23,42,0.06)] sm:p-7">
          {!file ? (
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(event) => {
                event.preventDefault();
                setDragging(true);
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={(event) => {
                event.preventDefault();
                setDragging(false);

                selectFile(event.dataTransfer.files?.[0]);
              }}
              className={[
                "flex min-h-64 w-full flex-col items-center justify-center",
                "rounded-xl border border-dashed px-6 text-center transition",
                dragging
                  ? "border-primary bg-indigo-50"
                  : "border-border-strong bg-surface-secondary/60 hover:border-primary hover:bg-indigo-50/40",
              ].join(" ")}
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-border-light bg-white text-primary shadow-sm">
                <Upload size={21} />
              </div>

              <div className="mt-5 text-base font-semibold text-text-primary">
                Drop your documentation here
              </div>

              <div className="mt-2 text-sm text-text-muted">
                or click to browse your files
              </div>

              <div className="mt-5 rounded-md bg-white px-3 py-1.5 text-xs text-text-muted ring-1 ring-border-light">
                PDF · DOCX · TXT · MD · Max 10 MB
              </div>
            </button>
          ) : (
            <div>
              <div className="flex items-center gap-4 rounded-xl border border-border-light bg-surface-secondary/60 p-4">
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-white text-primary shadow-sm ring-1 ring-border-light">
                  <FileText size={20} />
                </div>

                <div className="min-w-0 flex-1">
                  <div className="truncate text-sm font-semibold text-text-primary">
                    {file.name}
                  </div>

                  <div className="mt-1 text-xs text-text-muted">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </div>
                </div>

                {!loading && (
                  <button
                    type="button"
                    onClick={() => {
                      setFile(null);
                      setError("");
                    }}
                    className="flex h-8 w-8 items-center justify-center rounded-lg text-text-muted hover:bg-white hover:text-text-primary"
                  >
                    <X size={17} />
                  </button>
                )}
              </div>

              <button
                type="button"
                disabled={loading}
                onClick={handleAnalyze}
                className="mt-5 flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-primary px-5 text-sm font-semibold text-white shadow-sm transition hover:bg-primary-hover disabled:cursor-not-allowed disabled:opacity-70"
              >
                {loading ? (
                  <>
                    <LoaderCircle size={18} className="animate-spin" />
                    Analyzing document…
                  </>
                ) : (
                  <>
                    Analyze compliance
                    <ArrowRight size={17} />
                  </>
                )}
              </button>

              {loading && (
                <div className="mt-4 rounded-xl border border-blue-100 bg-info-bg px-4 py-4">
                  <div className="text-sm font-medium text-info">
                    Running compliance analysis
                  </div>

                  <div className="mt-2 text-xs leading-5 text-text-secondary">
                    Extracting the system profile, classifying risk, retrieving
                    relevant EU AI Act provisions, and assessing compliance
                    requirements. This may take a little while.
                  </div>
                </div>
              )}
            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            accept=".pdf,.docx,.txt,.md"
            onChange={(event) => selectFile(event.target.files?.[0])}
          />

          {error && (
            <div className="mt-4 rounded-lg border border-red-200 bg-danger-bg px-4 py-3 text-sm leading-6 text-danger">
              {error}
            </div>
          )}
        </div>

        <div className="mt-7 grid gap-3 sm:grid-cols-3">
          {[
            "Evidence grounded",
            "EU AI Act retrieval",
            "Actionable findings",
          ].map((item) => (
            <div
              key={item}
              className="flex items-center justify-center gap-2 text-xs font-medium text-text-muted"
            >
              <Check size={14} className="text-success" />
              {item}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
