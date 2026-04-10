import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  // 1. Move it to the top level as the CLI suggested
  // 2. Add 'as any' to bypass the outdated type definition
  allowedDevOrigins: ['192.168.0.103', 'localhost:3000'],
} as any; 

export default nextConfig;