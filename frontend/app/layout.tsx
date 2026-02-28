import "./globals.css"
import Link from "next/link"
import { Toaster } from "react-hot-toast"
import { Plus_Jakarta_Sans } from "next/font/google"

const jakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-jakarta"
})

export const metadata = {
  title: "ClauseGuard",
  description: "AI Contract Risk Analysis"
}

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body
        className={`${jakarta.className} relative bg-[#0B1120] text-slate-200 min-h-screen antialiased overflow-x-hidden`}
      >

        {/* Background Ambient Glow */}
        <div className="absolute inset-0 -z-10 bg-gradient-to-br from-blue-900/20 via-[#0B1120] to-cyan-900/20" />
        <div className="absolute top-[-200px] left-[-200px] w-[500px] h-[500px] bg-blue-600/20 blur-3xl rounded-full -z-10" />
        <div className="absolute bottom-[-200px] right-[-200px] w-[500px] h-[500px] bg-cyan-600/20 blur-3xl rounded-full -z-10" />

        {/* Navbar */}
        <nav className="sticky top-0 z-50 backdrop-blur-xl bg-[#0B1120]/80 border-b border-slate-800">
          <div className="max-w-7xl mx-auto px-8 py-4 flex justify-between items-center">

            <Link
              href="/"
              className="text-xl font-semibold tracking-tight text-white hover:text-blue-400 transition"
            >
              ClauseGuard
            </Link>

            <div className="space-x-6 text-sm text-slate-400 font-medium">
              <Link
                href="/dashboard"
                className="hover:text-white transition"
              >
                Dashboard
              </Link>
              <Link
                href="/admin/login"
                className="hover:text-white transition"
              >
                Admin
              </Link>
            </div>

          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-6xl mx-auto px-6 py-12">
          {children}
        </main>

        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "#0B1120",
              color: "#E2E8F0",
              border: "1px solid #1E293B"
            }
          }}
        />

      </body>
    </html>
  )
}