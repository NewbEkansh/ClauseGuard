"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

export default function AnalysisPage() {
  const params = useParams()
  const id = params?.id as string

  const [data, setData] = useState<any>(null)

  useEffect(() => {
    if (!id) return

    async function fetchData() {
      const res = await fetch(`http://localhost:8080/analysis/${id}`)
      const json = await res.json()
      setData(json)
    }

    fetchData()
  }, [id])

  if (!data) {
    return (
      <div className="min-h-screen bg-black text-white p-10">
        Loading...
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-10">
      <h1 className="text-3xl font-bold mb-6">Contract Analysis</h1>

      <div className="mb-6">
        <p><strong>Status:</strong> {data.status}</p>
        <p>
          <strong>Overall Risk Score:</strong>{" "}
          <span className="bg-red-600 px-3 py-1 rounded">
            {data.risk_score}
          </span>
        </p>
      </div>

      {Object.entries(data.analysis).map(([key, value]: any) => {
        if (key === "overall_risk_score") return null

        return (
          <div key={key} className="bg-gray-900 p-6 rounded-lg mb-6">
            <h2 className="text-xl font-semibold capitalize mb-3">
              {key}
            </h2>

            <p className="text-sm text-gray-400 mb-2">
              Risk Level: {value.risk_level}
            </p>

            <p className="mb-2">{value.text}</p>

            <p className="text-yellow-400 mb-2">
              Why Risky: {value.why_risky}
            </p>

            <p className="text-blue-400 mb-2">
              Scenario: {value.scenario_analysis}
            </p>

            <p className="text-green-400">
              Suggested Rewrite: {value.suggested_rewrite}
            </p>
          </div>
        )
      })}
    </div>
  )
}