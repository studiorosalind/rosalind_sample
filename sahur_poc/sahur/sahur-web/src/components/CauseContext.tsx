export default function CauseContext({ context }: { context: any }) {
  if (!context) {
    return (
      <div className="bg-white border rounded p-4">
        <h3 className="font-semibold mb-2">CauseContext</h3>
        <div className="text-gray-400">컨텍스트 없음</div>
      </div>
    )
  }
  return (
    <div className="bg-white border rounded p-4">
      <h3 className="font-semibold mb-2">CauseContext</h3>
      {context.stackTrace && (
        <div className="mb-2">
          <div className="text-xs text-gray-500 mb-1">StackTrace</div>
          <pre className="bg-gray-100 p-2 rounded text-xs">{context.stackTrace}</pre>
        </div>
      )}
      {context.httpRequest && (
        <div className="mb-2">
          <div className="text-xs text-gray-500 mb-1">HTTP 요청</div>
          <pre className="bg-gray-100 p-2 rounded text-xs">{JSON.stringify(context.httpRequest, null, 2)}</pre>
        </div>
      )}
      {context.kafkaMessage && (
        <div className="mb-2">
          <div className="text-xs text-gray-500 mb-1">Kafka 메시지</div>
          <pre className="bg-gray-100 p-2 rounded text-xs">{JSON.stringify(context.kafkaMessage, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
