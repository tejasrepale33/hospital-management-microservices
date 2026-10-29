# Hospital Management Platform — Frontend

A responsive, clinical-grade React 18 frontend for the Hospital Management Microservices Platform, consuming the Spring Cloud API Gateway on port `8080` (`/api/auth/**`, `/api/patients/**`, `/api/doctors/**`, JWT bearer auth).

---

## 🛠️ Tech Stack
- **React 18**: Functional components & modern hooks
- **React Router v6**: Declarative client-side routing & role-based guards
- **Plain CSS Design System**: Custom clinical color palette (`#1E5F8C` primary, `#2EC4B6` teal accent, soft neutrals), no external CSS framework bloat
- **Axios with Interceptors**:
  - Request Interceptor: Automatically attaches `Authorization: Bearer <token>`
  - Response Interceptor: Redirects to `/login` on HTTP 401 Unauthorized
- **Context API (`AuthContext`)**: Centralized JWT session management and role normalization (`PATIENT`, `DOCTOR`, `ADMIN`)

---

## 🎨 Visual Design & Experience
- **Clinical Palette**: Hospital Navy (`#1E5F8C`), Fresh Teal (`#2EC4B6`), Surface White, Soft Slate Neutrals.
- **Urgency Badges with Pulse Animation**:
  - 🚨 `EMERGENCY`: Rose Red with live CSS pulse glow animation
  - ⚠️ `HIGH`: Warm Orange
  - ⏱️ `MODERATE`: Amber Yellow
  - ✓ `LOW / ROUTINE`: Emerald Green
- **Smooth Accordion Expanders**: Interactive available slots reveal inside doctor cards.
- **Shimmering Skeleton Loaders**: Placeholder loading states while fetching Redis-cached doctor and patient endpoints.
- **Mobile & Tablet Responsive**: Adapts fluidly from wide monitors to tablets and mobile screens.

---

## 🚀 Running the Frontend Locally

### Prerequisites
- Node.js (v18+)
- Backend services running (specifically `api-gateway` on port `8080`)

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Start the Vite Development Server
```bash
npm run dev
```
The app will launch at: **`http://localhost:3000`**

### Step 3: Log In with Demo Accounts
The login page provides **1-click Demo Fill buttons**:
- **Patient**: `patient_john` / `patient123`
- **Doctor**: `doctor_smith` / `doctor123`
- **Admin**: `admin` / `admin123`

---

## 🐳 Docker Deployment

The frontend is ready to run as an Alpine Nginx container:

```bash
# Build frontend container
docker build -t hospital-frontend ./frontend

# Run container on port 3000
docker run -p 3000:80 hospital-frontend
```

Or spin it up along with the full microservices cluster via the root `docker-compose.yml`:
```bash
docker-compose up --build -d
```
Visit `http://localhost:3000` in your browser.
