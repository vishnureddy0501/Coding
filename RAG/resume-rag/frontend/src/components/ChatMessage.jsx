import { Bot, ChevronDown, FileSearch, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ChatMessage({ message }) {
  const assistant = message.role === "assistant";
  return (
    <article className={`message ${message.role}`}>
      <div className="avatar">
        {assistant ? <Bot size={19} /> : <User size={18} />}
      </div>
      <div className="message-content">
        <div className="message-author">{assistant ? "ResumeAI" : "You"}</div>
        {assistant ? (
          <div className="markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
            {message.streaming && <span className="stream-cursor" />}
          </div>
        ) : (
          <p>{message.content}</p>
        )}
        {!!message.sources?.length && (
          <details className="citations">
            <summary>
              <FileSearch size={16} /> {message.sources.length} sources{" "}
              <ChevronDown size={15} />
            </summary>
            <div className="citation-list">
              {message.sources.map((source, index) => (
                <div
                  className="citation"
                  key={`${source.resume_id}-${source.chunk_number}-${index}`}
                >
                  <strong>{source.resume_name}</strong>
                  <span>
                    Section {source.chunk_number} · relevance{" "}
                    {Math.round(source.score * 100)}%
                  </span>
                  <p>{source.text}</p>
                </div>
              ))}
            </div>
          </details>
        )}
      </div>
    </article>
  );
}
