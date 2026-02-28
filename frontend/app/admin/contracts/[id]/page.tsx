"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"

type ContractDetail = {
  id: string
  status: string
  risk_score: number | null
  file_url: string
  created_at: string
  analysis: any
}

type AuditLog = {
  action: string
  status: string
  message: string
  created_at: string
}

export default function ContractDetailPage() {
  const params = useParams()
  const id = params.id as string
  const router = useRouter()

  const [contract, setContract] = useState<ContractDetail | null>(null)
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("admin_token")

    if (!token) {
      router.push("/admin/login")
      return
    }

    Promise.all([
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/contracts/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      }),
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/contracts/${id}/audit`, {
        headers: { Authorization: `Bearer ${token}` }
      })
    ])
      .then(async ([contractRes, auditRes]) => {
        if (contractRes.status === 401 || auditRes.status === 401) {
          router.push("/admin/login")
          return
        }

        const contractData = await contractRes.json()
        const auditData = await auditRes.json()

        setContract(contractData)
        setAuditLogs(auditData)
      })
      .finally(() => setLoading(false))
  }, [id])

  const handleDownload = () => {
    const token = localStorage.getItem("admin_token")

    if (!token) {
      router.push("/admin/login")
      return
    }

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/analysis/${id}/report`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = `contract_${id}.pdf`
        a.click()
      })
  }

  if (loading) return <p className="p-8">Loading...</p>
  if (!contract) return <p className="p-8">Contract not found</p>

  return (
    <div className="p-8">

      {/* Header Actions */}
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => router.back()}
          className="text-blue-500"
        >
          ← Back
        </button>

        <button
          onClick={handleDownload}
          className="bg-black text-white px-4 py-2 rounded"
        >
          Download Report
        </button>
      </div>

      <h1 className="text-2xl mb-6">Contract Detail</h1>

      {/* Basic Info */}
      <div className="border p-4 rounded mb-6 space-y-1">
        <p><strong>ID:</strong> {contract.id}</p>
        <p><strong>Status:</strong> {contract.status}</p>
        <p><strong>Risk Score:</strong> {contract.risk_score ?? "N/A"}</p>
        <p><strong>Created:</strong> {new Date(contract.created_at).toLocaleString()}</p>
      </div>

      {/* Clause Analysis */}
      <h2 className="text-xl mb-3">Clause Analysis</h2>
      <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto mb-8">
        {JSON.stringify(contract.analysis, null, 2)}
      </pre>

      {/* Audit Timeline */}
      <h2 className="text-xl mb-3">Audit Timeline</h2>

      <div className="space-y-3">
        {auditLogs.map((log, index) => (
          <div key={index} className="border p-3 rounded">
            <p><strong>{log.action}</strong> ({log.status})</p>
            <p className="text-sm text-gray-600">{log.message}</p>
            <p className="text-xs text-gray-400">
              {new Date(log.created_at).toLocaleString()}
            </p>
          </div>
        ))}
      </div>

    </div>
  )
}