"use client"

import { useEffect, useState, useMemo } from "react"
import Link from "next/link"

export default function Dashboard() {

  const [contracts, setContracts] = useState<any[]>([])
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [search, setSearch] = useState("")
  const [sortByRisk, setSortByRisk] = useState(false)

  // ==============================
  // Fetch contracts
  // ==============================
  const fetchContracts = async () => {
    try {
      const res = await fetch("http://localhost:8080/contracts")
      const json = await res.json()
      setContracts(json)
    } catch (err) {
      console.error("Fetch failed")
    }
  }

  // ==============================
  // Polling
  // ==============================
  useEffect(() => {
    fetchContracts()

    const interval = setInterval(async () => {
      const res = await fetch("http://localhost:8080/contracts")
      const json = await res.json()
      setContracts(json)

      const stillProcessing = json.some(
        (c: any) => c.status === "processing"
      )

      if (!stillProcessing) clearInterval(interval)
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  // ==============================
  // Upload
  // ==============================
  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append("file", file)

      await fetch("http://localhost:8080/upload", {
        method: "POST",
        body: formData,
      })

      setFile(null)
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)

      fetchContracts()

    } catch (err) {
      setError("Upload failed. Try again.")
    } finally {
      setUploading(false)
    }
  }

  // ==============================
  // Filter + Sort Logic
  // ==============================
  const filteredContracts = useMemo(() => {
    let filtered = contracts.filter((c) =>
      c.file_name.toLowerCase().includes(search.toLowerCase())
    )

    if (sortByRisk) {
      filtered = [...filtered].sort(
        (a, b) => (b.risk_score || 0) - (a.risk_score || 0)
      )
    }

    return filtered
  }, [contracts, search, sortByRisk])

  return (
    <div className="min-h-screen bg-gray-950 text-white p-10">

      <h1 className="text-4xl font-bold mb-8">
        Contract Dashboard
      </h1>

      {/* ================= Upload Section ================= */}
      <div className="mb-8 flex items-center gap-4 flex-wrap">

        <input
          type="file"
          accept="application/pdf"
          id="fileUpload"
          className="hidden"
          onChange={(e) =>
            setFile(e.target.files ? e.target.files[0] : null)
          }
        />

        <label
          htmlFor="fileUpload"
          className="cursor-pointer bg-gray-800 hover:bg-gray-700 px-5 py-2 rounded-lg border border-gray-700 transition"
        >
          {file ? "Change File" : "Choose PDF"}
        </label>

        {file && (
          <span className="text-gray-400 text-sm truncate max-w-xs">
            {file.name}
          </span>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="bg-blue-600 hover:bg-blue-700 px-5 py-2 rounded-lg font-semibold transition disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload Contract"}
        </button>

      </div>

      {/* ================= Success Toast ================= */}
      {success && (
        <div className="bg-green-600 px-4 py-2 rounded mb-6 w-fit">
          Contract uploaded successfully!!
        </div>
      )}

      {error && (
        <p className="text-red-400 mb-6">{error}</p>
      )}

      {/* ================= Search + Sort ================= */}
      <div className="mb-8 flex gap-4 flex-wrap items-center">

        <input
          type="text"
          placeholder="Search contracts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-gray-800 px-4 py-2 rounded-lg border border-gray-700 w-64"
        />

        <button
          onClick={() => setSortByRisk(!sortByRisk)}
          className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition"
        >
          {sortByRisk ? "Sorted by Risk ✓" : "Sort by Risk"}
        </button>

      </div>

      {/* ================= Empty State ================= */}
      {filteredContracts.length === 0 && (
        <p className="text-gray-400">No contracts found.</p>
      )}

      {/* ================= Contracts List ================= */}
      <div className="grid gap-6">

        {filteredContracts.map((contract) => (
          <Link
            key={contract.id}
            href={`/analysis/${contract.id}`}
            className="bg-gray-900 p-6 rounded-xl border border-gray-800 hover:border-blue-500 transition"
          >
            <div className="flex justify-between items-center">

              <div>
                <p className="font-semibold text-lg">
                  {contract.file_name}
                </p>

                <p className="text-gray-400 text-sm">
                  {new Date(contract.created_at).toLocaleString()}
                </p>

                {contract.risk_score !== undefined && (
                  <p className="mt-2 text-sm text-blue-400">
                    Risk Score: {contract.risk_score}
                  </p>
                )}
              </div>

              {/* Status Indicator */}
              {contract.status === "processing" ? (
                <span className="bg-yellow-500 px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-2">
                  <span className="w-2 h-2 bg-white rounded-full animate-ping"></span>
                  Processing
                </span>
              ) : (
                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    contract.status === "completed"
                      ? "bg-green-600"
                      : "bg-red-600"
                  }`}
                >
                  {contract.status}
                </span>
              )}

            </div>
          </Link>
        ))}

      </div>

    </div>
  )
}