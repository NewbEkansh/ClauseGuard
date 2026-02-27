"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

export default function AnalysisPage() {

  // Get contract ID from dynamic route
  const params = useParams()
  const id = params?.id as string

  // Store backend response
  const [data, setData] = useState<any>(null)

  // Fetch analysis from backend
  useEffect(() => {
    if (!id) return

    async function fetchData() {
      const res = await fetch(`http://localhost:8080/analysis/${id}`)
      const json = await res.json()
      setData(json)
    }

    fetchData()
  }, [id])

  // Color badge for clause risk level
  const getRiskColor = (level: string) => {
    if (level === "High") return "bg-red-600"
    if (level === "Medium") return "bg-yellow-500"
    if (level === "Low") return "bg-green-600"
    return "bg-gray-500"
  }

  // Optional: color overall score dynamically
  const getOverallRiskColor = (score: number) => {
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
  // ==========================================
  // 📄 Download PDF Report (from backend)
  // ==========================================
  const downloadPDF = () => {
    if (!id) return
    
    // This directly hits backend endpoint
    window.open(
        `http://localhost:8080/analysis/${id}/report`,
        "_blank"
    )
  }

  // Loading screen
  if (!data) {
    return (
      <div className="min-h-screen bg-black text-white p-10">
        Loading...
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
          <strong>Status:</strong> {data.status}
        </p>

        <div>
          <strong>Overall Risk Score:</strong>{" "}
          <span
            className={`px-4 py-1 rounded-full font-semibold ${getOverallRiskColor(data.risk_score)}`}
          >
            {data.risk_score}
          </span>
        </div>

        {/* ✅ Download JSON Button */}
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
      {Object.entries(data.analysis).map(([key, value]: any) => {

        if (key === "overall_risk_score") return null

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
                className={`px-4 py-1 rounded-full text-sm font-semibold ${getRiskColor(value.risk_level)}`}
              >
                {value.risk_level}
              </span>
            </div>

            {/* Clause Text */}
            <p className="text-gray-300 mb-6 leading-relaxed">
              {value.text}
            </p>

            {/* Why Risky */}
            <div className="bg-gray-800 p-4 rounded-lg mb-4">
              <p className="text-yellow-400 font-semibold mb-1">
                Why Risky
              </p>
              <p className="text-gray-300">
                {value.why_risky}
              </p>
            </div>

            {/* Scenario */}
            <div className="bg-gray-800 p-4 rounded-lg mb-4">
              <p className="text-blue-400 font-semibold mb-1">
                Scenario Analysis
              </p>
              <p className="text-gray-300">
                {value.scenario_analysis}
              </p>
            </div>

            {/* Suggested Rewrite */}
            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-green-400 font-semibold mb-1">
                Suggested Rewrite
              </p>
              <p className="text-gray-300">
                {value.suggested_rewrite}
              </p>
            </div>

          </div>
        )
      })}

    </div>
  )
}