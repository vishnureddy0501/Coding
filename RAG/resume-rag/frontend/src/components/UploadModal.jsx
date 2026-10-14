import { FilePlus2, FileText, Trash2, Upload, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

export default function UploadModal({
  open,
  resumes,
  onClose,
  onUpload,
  onDelete,
}) {
  const [files, setFiles] = useState([]);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState("");
  const inputRef = useRef(null);

  useEffect(() => {
    if (!open) return undefined;
    const escape = (event) => event.key === "Escape" && !busy && onClose();
    window.addEventListener("keydown", escape);
    return () => window.removeEventListener("keydown", escape);
  }, [open, busy, onClose]);
  if (!open) return null;

  async function submit(event) {
    event.preventDefault();
    if (!files.length) return;
    setBusy(true);
    setStatus("Uploading and creating embeddings…");
    try {
      await onUpload(files);
      setFiles([]);
      if (inputRef.current) inputRef.current.value = "";
      setStatus("Ready to chat — indexing complete.");
    } catch (error) {
      setStatus(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div
      className="modal-backdrop"
      onMouseDown={(event) =>
        event.target === event.currentTarget && !busy && onClose()
      }
    >
      <section
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="upload-title"
      >
        <div className="modal-header">
          <div>
            <span className="modal-icon">
              <FilePlus2 size={20} />
            </span>
            <h2 id="upload-title">Resume knowledge base</h2>
            <p>
              Upload PDF, DOCX, or TXT files. Select them from the sidebar when
              chatting.
            </p>
          </div>
          <button
            className="icon-button"
            onClick={onClose}
            disabled={busy}
            aria-label="Close"
          >
            <X size={20} />
          </button>
        </div>
        <form onSubmit={submit}>
          <label className="dropzone">
            <Upload size={25} />
            <strong>
              {files.length
                ? `${files.length} file(s) selected`
                : "Choose resumes"}
            </strong>
            <span>Maximum 5 MB each</span>
            <input
              ref={inputRef}
              type="file"
              accept=".pdf,.docx,.txt"
              multiple
              onChange={(event) => setFiles([...event.target.files])}
            />
          </label>
          <button
            className="primary-button"
            type="submit"
            disabled={busy || !files.length}
          >
            {busy ? <span className="spinner" /> : <Upload size={17} />}
            {busy ? "Indexing…" : "Upload and index"}
          </button>
          {status && <p className="modal-status">{status}</p>}
        </form>
        <div className="file-list-header">
          <span>Uploaded resumes</span>
          <span>{resumes.length}</span>
        </div>
        <div className="modal-file-list">
          {!resumes.length && (
            <p className="empty-files">No resumes uploaded yet.</p>
          )}
          {resumes.map((resume) => (
            <div className="modal-file" key={resume.resume_id}>
              <span className="file-icon">
                <FileText size={18} />
              </span>
              <div>
                <strong>{resume.original_name}</strong>
                <span>{resume.chunk_count} indexed sections</span>
              </div>
              <button
                type="button"
                onClick={() => onDelete(resume)}
                aria-label={`Delete ${resume.original_name}`}
              >
                <Trash2 size={17} />
              </button>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
