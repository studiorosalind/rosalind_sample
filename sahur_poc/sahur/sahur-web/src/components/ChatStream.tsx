type StreamMessage = {
  step: string
  issueTrackingId: string
  solution?: string
}

export default function ChatStream({ messages }: { messages: StreamMessage[] }) {
  return (
    <div className="bg-white border rounded p-4 h-48 overflow-y-auto">
      <h3 className="font-semibold mb-2">에이전트 사고 과정</h3>
      <ul>
        {messages.map((msg, idx) => (
          <li key={idx} className="mb-1">
            <span className="text-gray-700">{msg.step}</span>
            {msg.solution && (
              <span className="ml-2 text-green-700 font-semibold">[해결책] {msg.solution}</span>
            )}
          </li>
        ))}
      </ul>
      {messages.length === 0 && (
        <div className="text-gray-400">아직 스트림 메시지가 없습니다.</div>
      )}
    </div>
  )
}
