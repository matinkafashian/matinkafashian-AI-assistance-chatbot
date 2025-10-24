/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  // Force Vercel to use latest code
  generateBuildId: async () => {
    return 'latest-build-' + Date.now()
  }
}

module.exports = nextConfig
