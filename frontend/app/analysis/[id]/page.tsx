"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

export default function AnalysisPage() {

  const params = useParams()
  const id = params?.id as string

  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return

    async function fetchData() {
      try {
        const res = await fetch(`http://localhost:8080/analysis/${id}`)

        if (!res.ok) {
          if (res.status === 404) {
            setError("Analysis not completed yet. Please refresh in a few seconds.")
            setLoading(false)
            return
          }
          throw new Error("Failed to fetch analysis")
        }

        const json = await res.json()
        setData(json)
        setLoading(false)

      } catch (err) {
        setError("Error fetching analysis.")
        setLoading(false)
      }
    }

    fetchData()
  }, [id])

  // Color badge for clause risk level
  const getRiskColor = (level?: string) => {
    if (level === "High") return "bg-red-600"
    if (level === "Medium") return "bg-yellow-500"
    if (level === "Low") return "bg-green-600"
    return "bg-gray-500"
  }

  // Color overall risk score dynamically
  const getOverallRiskColor = (score?: number) => {
    if (score === undefined || score === null) return "bg-gray-500"
    if (score >= 70) return "bg-red-600"
    if (score >= 40) return "bg-yellow-500"
    return "bg-green-600"
  }

  // Download JSON analysis file
  const downloadJSON = () => {
    if (!data) return

    const jsonString = JSON.stringify(data, null, 2)
    const blob = new Blob([jsonString], { type: "application/json" })
    const url = URL.createObjectURL(blob)

    const a = document.createElement("a")
    a.href = url
    a.download = `analysis_${id}.json`
    a.click()

    URL.revokeObjectURL(url)
  }

  // Download PDF report from backend
  const downloadPDF = () => {
    if (!id) return
    window.open(`http://localhost:8080/analysis/${id}/report`, "_blank")
  }

  // Loading screen
  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white p-10">
        Processing analysis...
      </div>
    )
  }

  // Error screen
  if (error) {
    return (
      <div className="min-h-screen bg-black text-white p-10 text-yellow-400">
        {error}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-10">

      {/* Header */}
      <h1 className="text-4xl font-bold mb-8">Contract Analysis</h1>

      {/* Summary Section */}
      <div className="mb-10 flex flex-wrap items-center gap-6">

        <p>
          <strong>Status:</strong> {data?.status ?? "Unknown"}
        </p>

        <div>
          <strong>Overall Risk Score:</strong>{" "}
          <span
            className={`px-4 py-1 rounded-full font-semibold ${getOverallRiskColor(data?.risk_score)}`}
          >
            {data?.risk_score ?? "N/A"}
          </span>
        </div>

        <button
          onClick={downloadJSON}
          className="bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded-lg font-semibold transition"
        >
          Download JSON Report
        </button>

        <button
          onClick={downloadPDF}
          className="bg-purple-600 hover:bg-purple-700 px-5 py-2 rounded-lg font-semibold transition"
        >
          Download PDF Report
        </button>

      </div>

      {/* Clause Cards */}
      {data?.analysis &&
        Object.entries(data.analysis).map(([key, value]: any) => {

          // Skip overall score field
          if (key === "overall_risk_score") return null

          // Skip if clause is null (clause not present in contract)
          if (!value || typeof value !== "object") return null

          return (
            <div
              key={key}
              className="bg-gray-900 p-8 rounded-2xl mb-8 shadow-lg border border-gray-800"
            >

              {/* Title + Risk Badge */}
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold capitalize">
                  {key}
                </h2>

                <span
                  className={`px-4 py-1 rounded-full text-sm font-semibold ${getRiskColor(value?.risk_level)}`}
                >
                  {value?.risk_level ?? "N/A"}
                </span>
              </div>

              {/* Clause Text */}
              <p className="text-gray-300 mb-6 leading-relaxed">
                {value?.text ?? "Clause not found."}
              </p>

              {/* Why Risky */}
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <p className="text-yellow-400 font-semibold mb-1">
                  Why Risky
                </p>
                <p className="text-gray-300">
                  {value?.why_risky ?? "Not available"}
                </p>
              </div>

              {/* Scenario Analysis */}
              <div className="bg-gray-800 p-4 rounded-lg mb-4">
                <p className="text-blue-400 font-semibold mb-1">
                  Scenario Analysis
                </p>
                <p className="text-gray-300">
                  {value?.scenario_analysis ?? "Not available"}
                </p>
              </div>

              {/* Suggested Rewrite */}
              <div className="bg-gray-800 p-4 rounded-lg">
                <p className="text-green-400 font-semibold mb-1">
                  Suggested Rewrite
                </p>
                <p className="text-gray-300">
                  {value?.suggested_rewrite ?? "Not available"}
                </p>
              </div>

            </div>
          )
        })}

    </div>
  )
}