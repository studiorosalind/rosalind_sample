export default function HistoryContext({ context }: { context: any }) {
  if (!context || !context.similarIssues) {
    return (
      <div className="bg-white border rounded p-4">
        <h3 className="font-semibold mb-2">HistoryContext</h3>
        <div className="text-gray-400">유사 이슈 없음</div>
      </div>
    )
  }
  return (
    <div className="bg-white border rounded p-4">
      <h3 className="font-semibold mb-2">HistoryContext</h3>
      <ul>
        {context.similarIssues.map((issue: any, idx: number) => (
          <li key={idx} className="mb-2">
            <div className="text-xs text-gray-500 mb-1">유사 이슈 {idx + 1}</div>
            <div className="text-sm font-medium">{issue.description}</div>
            <div className="text-xs text-green-700">해결책: {issue.solution}</div>
            {issue.stackTrace && (
              <pre className="bg-gray-100 p-2 rounded text-xs mt-1">{issue.stackTrace}</pre>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
