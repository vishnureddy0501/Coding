import { ArrowUp, Paperclip, Square } from "lucide-react";
import { useEffect, useRef } from "react";

export default function Composer({
  value,
  onChange,
  onSubmit,
  onUpload,
  disabled,
  streaming,
  onStop,
  selectedCount,
}) {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current) {
      ref.current.style.height = "auto";
      ref.current.style.height = `${Math.min(ref.current.scrollHeight, 160)}px`;
    }
  }, [value]);
  function keyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSubmit(event);
    }
  }
  return (
    <div className="composer-wrap">
      <form className="composer" onSubmit={onSubmit}>
        <button
          className="composer-action"
          type="button"
          onClick={onUpload}
          aria-label="Upload resumes"
        >
          <Paperclip size={20} />
        </button>
        <textarea
          ref={ref}
          rows="1"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={keyDown}
          placeholder={
            selectedCount
              ? "Ask anything about the selected resumes…"
              : "Select or upload a resume first"
          }
          disabled={disabled}
        />
        {streaming ? (
          <button
            className="send-button"
            type="button"
            onClick={onStop}
            aria-label="Stop response"
          >
            <Square size={14} fill="currentColor" />
          </button>
        ) : (
          <button
            className="send-button"
            type="submit"
            disabled={disabled || !value.trim()}
            aria-label="Send"
          >
            <ArrowUp size={19} />
          </button>
        )}
      </form>
      <p>
        {selectedCount} resume{selectedCount === 1 ? "" : "s"} selected ·
        Answers may need verification.
      </p>
    </div>
  );
}
