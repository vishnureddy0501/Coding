import { Check, FileText, PanelLeftClose, Plus, Upload } from "lucide-react";
import Logo from "./Logo.jsx";

export default function Sidebar({
  resumes,
  selectedIds,
  onToggle,
  onUpload,
  onNewChat,
  onClose,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <Logo />
        <button
          className="icon-button mobile-close"
          onClick={onClose}
          aria-label="Close sidebar"
        >
          <PanelLeftClose size={19} />
        </button>
      </div>
      <button className="new-chat" onClick={onNewChat}>
        <Plus size={18} /> New conversation
      </button>
      <div className="sidebar-section-heading">
        <span>Knowledge base</span>
        <span>
          {selectedIds.size}/{resumes.length}
        </span>
      </div>
      <div className="resume-nav">
        {!resumes.length && (
          <p className="sidebar-empty">
            Upload a resume to start asking questions.
          </p>
        )}
        {resumes.map((resume) => {
          const selected = selectedIds.has(resume.resume_id);
          return (
            <button
              className={`resume-nav-item${selected ? " selected" : ""}`}
              key={resume.resume_id}
              onClick={() => onToggle(resume.resume_id)}
              title={resume.original_name}
            >
              <FileText size={17} />
              <span>{resume.original_name}</span>
              <span className="check">{selected && <Check size={14} />}</span>
            </button>
          );
        })}
      </div>
      <button className="upload-trigger" onClick={onUpload}>
        <Upload size={17} /> Manage resumes
      </button>
    </aside>
  );
}
