import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/router'
import ChatStream from '../../../components/ChatStream'
import CauseContext from '../../../components/CauseContext'
import HistoryContext from '../../../components/HistoryContext'

type StreamMessage = {
  step: string
  issueTrackingId: string
  solution?: string
}

export default function IssueTrackingPage() {
  const router = useRouter()
  const { issueTrackingId } = router.query
  const [messages, setMessages] = useState<StreamMessage[]>([])
  const [cause, setCause] = useState<any>(null)
  const [history, setHistory] = useState<any>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!issueTrackingId) return
    // sahur-batch WebSocket 연결 (포트 8010)
    const ws = new window.WebSocket(`ws://localhost:8010/ws/stream/${issueTrackingId}`)
    wsRef.current = ws
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMessages((prev) => [...prev, data])
      if (data.step === 'CauseContext/HistoryContext 수집') {
        // 더미 컨텍스트
        setCause({
          stackTrace: 'FileNotFoundError: app/main.py',
          httpRequest: { method: 'POST', url: '/api/data' }
        })
        setHistory({
          similarIssues: [
            { description: 'DB 연결 실패', solution: 'DB 설정 확인' }
          ]
        })
      }
    }
    ws.onclose = () => {}
    return () => ws.close()
  }, [issueTrackingId])

  return (
    <div className="max-w-3xl mx-auto py-8">
      <h2 className="text-2xl font-bold mb-4">이슈 트래킹: {issueTrackingId}</h2>
      <div className="mb-6">
        <ChatStream messages={messages} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <CauseContext context={cause} />
        <HistoryContext context={history} />
      </div>
      <div className="mt-8">
        <input
          type="text"
          className="border px-3 py-2 rounded w-full"
          placeholder="추가 질문 또는 중간 개입 메시지 입력"
          disabled
        />
        <p className="text-sm text-gray-400 mt-1">* 데모에서는 입력이 비활성화되어 있습니다.</p>
      </div>
    </div>
  )
}
