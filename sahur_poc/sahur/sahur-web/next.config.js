/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    // Server-side environment variables that should be available to the client
    DATABASE_URL: process.env.DATABASE_URL,
    VECTORDATABASE_URL: process.env.VECTORDATABASE_URL
  }
};

module.exports = nextConfig;
