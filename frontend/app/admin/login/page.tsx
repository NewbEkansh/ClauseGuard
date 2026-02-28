"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"

export default function AdminLogin() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleLogin = async () => {
    setLoading(true)

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    })

    const data = await res.json()

    if (res.ok) {
      localStorage.setItem("admin_token", data.access_token)
      router.push("/admin/dashboard")
    } else {
      alert("Invalid credentials")
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen flex bg-[#0B1120]">

      {/* Left Branding Panel */}
      <div className="hidden md:flex w-1/2 bg-gradient-to-br from-blue-700 via-cyan-700 to-[#0B1120] items-center justify-center p-12">
        <div className="text-white space-y-6 max-w-md">
          <h1 className="text-4xl font-bold tracking-tight">
            ClauseGuard Admin
          </h1>
          <p className="text-blue-200">
            Secure AI-powered contract risk monitoring and analytics.
          </p>
          <div className="text-sm text-blue-300">
            • Real-time risk scoring  
            • Audit logging  
            • Retry tracking  
            • Admin analytics dashboard
          </div>
        </div>
      </div>

      {/* Right Login Panel */}
      <div className="flex w-full md:w-1/2 items-center justify-center px-6">

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md bg-slate-900/70 backdrop-blur-xl border border-slate-800 rounded-2xl p-8 shadow-2xl"
        >
          <h2 className="text-2xl font-semibold text-white mb-6">
            Admin Login
          </h2>

          <div className="space-y-4">

            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-600 transition"
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-600 transition"
            />

            <button
              onClick={handleLogin}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 rounded-lg py-3 font-medium text-white transition shadow-lg hover:shadow-blue-500/30"
            >
              {loading ? "Logging in..." : "Login"}
            </button>

          </div>

        </motion.div>

      </div>
    </div>
  )
}