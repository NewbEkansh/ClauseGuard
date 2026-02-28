"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

type AdminStats = {
  total_contracts: number
  completed: number
  failed: number
  processing: number
  average_risk_score: number
}

type ContractItem = {
  id: string
  status: string
  risk_score: number | null
  created_at: string
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [contracts, setContracts] = useState<ContractItem[]>([])
  const [statusFilter, setStatusFilter] = useState("")
  const [minScore, setMinScore] = useState("")
  const [maxScore, setMaxScore] = useState("")
  const router = useRouter()

  const fetchContracts = (token: string) => {
    let url = `${process.env.NEXT_PUBLIC_API_URL}/admin/contracts?`
    if (statusFilter) url += `status=${statusFilter}&`
    if (minScore) url += `min_score=${minScore}&`
    if (maxScore) url += `max_score=${maxScore}&`

    fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        if (res.status === 401) router.push("/admin/login")
        return res.json()
      })
      .then(data => setContracts(data))
  }

  useEffect(() => {
    const token = localStorage.getItem("admin_token")
    if (!token) {
      router.push("/admin/login")
      return
    }

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/stats`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        if (res.status === 401) router.push("/admin/login")
        return res.json()
      })
      .then(data => setStats(data))

    fetchContracts(token)
  }, [statusFilter, minScore, maxScore])

  const handleLogout = () => {
    localStorage.removeItem("admin_token")
    router.push("/admin/login")
  }

  const clearFilters = () => {
    setStatusFilter("")
    setMinScore("")
    setMaxScore("")
  }

  if (!stats)
    return (
      <div className="p-10 text-slate-400 animate-pulse">
        Loading admin dashboard...
      </div>
    )

  return (
    <div className="space-y-10">

      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">
            Admin Dashboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Monitor contract risk analytics
          </p>
        </div>

        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg text-sm font-medium transition"
        >
          Logout
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        <StatCard title="Total Contracts" value={stats.total_contracts} />
        <StatCard title="Completed" value={stats.completed} color="green" />
        <StatCard title="Failed" value={stats.failed} color="red" />
        <StatCard title="Processing" value={stats.processing} color="yellow" />
        <StatCard title="Avg Risk Score" value={stats.average_risk_score} color="purple" />
      </div>

      {/* Filters */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-lg font-medium">Filters</h2>

        <div className="flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-xs text-slate-400 mb-1">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
            >
              <option value="">All</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
              <option value="processing">Processing</option>
            </select>
          </div>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Min Risk</label>
            <input
              type="number"
              value={minScore}
              onChange={(e) => setMinScore(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm w-28"
            />
          </div>

          <div>
            <label className="block text-xs text-slate-400 mb-1">Max Risk</label>
            <input
              type="number"
              value={maxScore}
              onChange={(e) => setMaxScore(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm w-28"
            />
          </div>

          <button
            onClick={clearFilters}
            className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-sm transition"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Contracts Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-800 text-slate-400">
            <tr>
              <th className="px-6 py-4 text-left">ID</th>
              <th className="px-6 py-4 text-left">Status</th>
              <th className="px-6 py-4 text-left">Risk</th>
              <th className="px-6 py-4 text-left">Created</th>
            </tr>
          </thead>

          <tbody>
            {contracts.map((c) => (
              <tr
                key={c.id}
                className="border-t border-slate-800 hover:bg-slate-800/40 cursor-pointer transition"
                onClick={() => router.push(`/admin/contracts/${c.id}`)}
              >
                <td className="px-6 py-4 font-mono text-slate-300">
                  {c.id.slice(0, 8)}...
                </td>

                <td className="px-6 py-4">
                  <StatusBadge status={c.status} />
                </td>

                <td className="px-6 py-4 font-semibold text-purple-400">
                  {c.risk_score ?? "N/A"}
                </td>

                <td className="px-6 py-4 text-slate-400">
                  {new Date(c.created_at).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

/* ---------- Components ---------- */

function StatCard({
  title,
  value,
  color = "slate"
}: {
  title: string
  value: number
  color?: "green" | "red" | "yellow" | "purple" | "slate"
}) {
  const colors: Record<string, string> = {
    green: "text-green-400",
    red: "text-red-400",
    yellow: "text-yellow-400",
    purple: "text-purple-400",
    slate: "text-slate-200"
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-md">
      <p className="text-sm text-slate-400">{title}</p>
      <p className={`text-2xl font-semibold mt-2 ${colors[color]}`}>
        {value}
      </p>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    completed: "bg-green-500/20 text-green-400",
    failed: "bg-red-500/20 text-red-400",
    processing: "bg-yellow-500/20 text-yellow-400"
  }

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${styles[status] || "bg-slate-700 text-slate-300"}`}>
      {status}
    </span>
  )
}