import { Menu, Sparkles, Upload } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  listResumes,
  removeResume,
  streamQuestion,
  uploadResumes,
} from "./api/client.js";
import ChatMessage from "./components/ChatMessage.jsx";
import Composer from "./components/Composer.jsx";
import Sidebar from "./components/Sidebar.jsx";
import UploadModal from "./components/UploadModal.jsx";

const suggestions = [
  "Summarize the selected candidates",
  "Who has the strongest backend experience?",
  "Compare their technical skills",
];

export default function App() {
  const [resumes, setResumes] = useState([]);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [error, setError] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const abortRef = useRef(null);
  const bottomRef = useRef(null);

  const loadResumes = useCallback(async () => {
    const data = await listResumes();
    setResumes(data);
    setSelectedIds((current) => {
      const available = new Set(data.map((resume) => resume.resume_id));
      const next = new Set([...current].filter((id) => available.has(id)));
      data.forEach((resume) => next.add(resume.resume_id));
      return next;
    });
  }, []);

  useEffect(() => {
    loadResumes().catch((err) => setError(err.message));
  }, [loadResumes]);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function toggleResume(id) {
    setSelectedIds((current) => {
      const next = new Set(current);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  async function handleUpload(files) {
    await uploadResumes(files);
    await loadResumes();
  }
  async function handleDelete(resume) {
    if (!window.confirm(`Delete ${resume.original_name}?`)) return;
    await removeResume(resume.resume_id);
    await loadResumes();
  }

  async function ask(event, suggestion) {
    event?.preventDefault?.();
    const text = (suggestion || question).trim();
    if (!text || !selectedIds.size || streaming) return;
    const assistantId = crypto.randomUUID();
    setQuestion("");
    setError("");
    setStreaming(true);
    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", content: text },
      {
        id: assistantId,
        role: "assistant",
        content: "",
        sources: [],
        streaming: true,
      },
    ]);

    const controller = new AbortController();
    abortRef.current = controller;
    try {
      await streamQuestion(
        { question: text, resume_ids: [...selectedIds] },
        (item) => {
          if (item.type === "error") throw new Error(item.detail);
          setMessages((current) =>
            current.map((message) => {
              if (message.id !== assistantId) return message;
              if (item.type === "token")
                return { ...message, content: message.content + item.text };
              if (item.type === "sources")
                return { ...message, sources: item.sources };
              return message;
            }),
          );
        },
        controller.signal,
      );
    } catch (err) {
      if (err.name !== "AbortError") {
        setError(err.message);
        setMessages((current) =>
          current.filter((message) => message.id !== assistantId),
        );
      }
    } finally {
      setMessages((current) =>
        current.map((message) =>
          message.id === assistantId
            ? { ...message, streaming: false }
            : message,
        ),
      );
      setStreaming(false);
      abortRef.current = null;
    }
  }

  return (
    <div className="app-shell">
      <div
        className={`sidebar-layer${sidebarOpen ? " open" : ""}`}
        onClick={() => setSidebarOpen(false)}
      />
      <div className={`sidebar-holder${sidebarOpen ? " open" : ""}`}>
        <Sidebar
          resumes={resumes}
          selectedIds={selectedIds}
          onToggle={toggleResume}
          onUpload={() => setModalOpen(true)}
          onNewChat={() => {
            setMessages([]);
            setError("");
          }}
          onClose={() => setSidebarOpen(false)}
        />
      </div>
      <main className="chat-shell">
        <header className="chat-header">
          <button
            className="icon-button menu-button"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open sidebar"
          >
            <Menu size={20} />
          </button>
          <div>
            <strong>Resume Assistant</strong>
            <span>
              <i /> Online
            </span>
          </div>
          <button className="header-upload" onClick={() => setModalOpen(true)}>
            <Upload size={16} /> Upload
          </button>
        </header>
        <div className={`conversation${messages.length ? " active" : ""}`}>
          {!messages.length ? (
            <section className="welcome">
              <span className="welcome-icon">
                <Sparkles size={28} />
              </span>
              <h1>What would you like to know?</h1>
              <p>
                Ask questions, compare candidates, and discover experience
                across your resume collection.
              </p>
              {!resumes.length ? (
                <button
                  className="welcome-upload"
                  onClick={() => setModalOpen(true)}
                >
                  <Upload size={18} /> Upload your first resume
                </button>
              ) : (
                <div className="suggestions">
                  {suggestions.map((item) => (
                    <button key={item} onClick={() => ask(null, item)}>
                      {item}
                    </button>
                  ))}
                </div>
              )}
            </section>
          ) : (
            messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))
          )}
          {error && <div className="chat-error">{error}</div>}
          <div ref={bottomRef} />
        </div>
        <Composer
          value={question}
          onChange={setQuestion}
          onSubmit={ask}
          onUpload={() => setModalOpen(true)}
          disabled={!selectedIds.size}
          streaming={streaming}
          onStop={() => abortRef.current?.abort()}
          selectedCount={selectedIds.size}
        />
      </main>
      <UploadModal
        open={modalOpen}
        resumes={resumes}
        onClose={() => setModalOpen(false)}
        onUpload={handleUpload}
        onDelete={handleDelete}
      />
    </div>
  );
}
