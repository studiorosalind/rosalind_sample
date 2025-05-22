import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold mb-4">SAHUR 이슈 분석 데모</h1>
      <p className="mb-6">Slack에서 이슈 분석 요청이 들어오면, 실시간 사고 과정을 모니터링할 수 있습니다.</p>
      <Link href="/issue/tracking/demo-issue-1" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        데모 이슈 트래킹 페이지로 이동
      </Link>
    </main>
  )
}
