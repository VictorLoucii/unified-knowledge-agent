# frontend/frontend.Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the frontend code
COPY . .

# The API URL must be set BEFORE `next build` runs, not at container start.
# Next.js inlines every NEXT_PUBLIC_* value into the browser bundle during the
# build and the bundle then ignores the environment for ever after, so an
# `environment:` entry in docker-compose.yml is too late to change it. See
# node_modules/next/dist/docs/01-app/02-guides/environment-variables.md:166.
# The ENV line is what makes the ARG visible to the RUN step below.
#
# The default preserves the previous behaviour: it is the same fallback the
# three call sites already hardcode, so a bare `docker build` with no
# --build-arg produces exactly the bundle it produced before. docker-compose.yml
# overrides it with the host port the backend is actually published on.
ARG NEXT_PUBLIC_API_URL=http://localhost:7860
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the Next.js app
RUN npm run build

# Expose the Next.js port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]