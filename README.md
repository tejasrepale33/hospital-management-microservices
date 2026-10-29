# Hospital Management Microservices Ecosystem

An enterprise-grade, cloud-native distributed Hospital Management Platform engineered with **Spring Boot 3.2**, **Spring Cloud API Gateway**, **Netflix Eureka Service Discovery & Load Balancing**, **Spring Security 6 with JWT**, **Spring AI Symptom Triage**, **Distributed Redis Caching**, **PostgreSQL Dual-Database Architecture**, and **Docker Containerization**.

---

## 🏛️ System Architecture

```
                                [ Client / Postman / Frontend ]
                                               │
                                               ▼
                        ┌──────────────────────────────────────────────┐
                        │      Spring Cloud API Gateway (Port 8080)    │
                        │    - JwtAuthenticationFilter (HMAC-SHA256)   │
                        │    - Spring Cloud Client-Side LoadBalancer   │
                        │    - Global CORS Configuration               │
                        └──────┬───────────────┬──────────────┬────────┘
                               │               │              │
                  ┌────────────┘               │              └────────────┐
                  ▼                            ▼                           ▼
       ┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
       │  Auth Service (8081)│      │Patient Service(8082)│      │ Doctor Service(8083)│
       │ - Spring Security 6 │      │ - Spring AI Triage  │      │ - Specialty Catalog │
       │ - JJWT Token Minting│      │ - Medical Records   │      │ - Schedule Slots    │
       │ - Role-Based (RBAC) │      │ - Appointments      │      │ - Slot Booking      │
       └──────────┬──────────┘      └──────────┬──────────┘      └──────────┬──────────┘
                  │                            │                            │
                  ▼                            ▼                            ▼
       ┌─────────────────────┐      ┌─────────────────────┐      ┌─────────────────────┐
       │Eureka Registry(8761)│      │PostgreSQL:patient_db│      │ PostgreSQL:doctor_db│
       │ - Dynamic Discovery │      │Redis Cache:6379     │      │ Redis Cache:6379    │
       └─────────────────────┘      └─────────────────────┘      └─────────────────────┘
```

---

## 🚀 Key Features

1. **Spring Cloud API Gateway (Port 8080)**:
   - Dynamic routing to microservices via Eureka discovery (`lb://auth-service`, `lb://patient-service`, `lb://doctor-service`).
   - `JwtAuthenticationFilter` validates Bearer tokens on protected paths and injects user identity headers (`X-Auth-Username`, `X-Auth-Role`).
2. **Netflix Eureka Service Registry (Port 8761)**:
   - Live dashboard at `http://localhost:8761`.
   - Real-time heartbeat healthchecks and client-side load balancing.
3. **Auth Service (Port 8081)**:
   - Spring Security 6 with BCrypt password hashing.
   - JWT generation, validation, and claims parsing (`ROLE_PATIENT`, `ROLE_DOCTOR`, `ROLE_ADMIN`).
4. **Spring AI Symptom Triage Engine (Patient Service, Port 8082)**:
   - Evaluates patient symptoms and assigns clinical urgency (`EMERGENCY`, `HIGH`, `MODERATE`, `LOW`).
   - Identifies the appropriate department (Cardiology, Dermatology, Neurology, Orthopedics, General Medicine).
   - Dynamically calls `doctor-service` via load-balanced HTTP to suggest top matching doctors and open appointment slots.
   - Resilient design: supports external OpenAI/Ollama keys, plus a 100% offline clinical rules engine when keys are absent.
5. **Multi-Tier Redis Caching**:
   - Sub-2ms query responses for doctor catalogs and patient profiles via `@Cacheable`.
   - Intelligent cache invalidation (`@CacheEvict`) on database mutations.
   - Resilient `CacheErrorHandler` fallback to PostgreSQL if Redis is offline.
6. **Dual PostgreSQL Architecture**:
   - `patient_db`: Manages patients and appointments.
   - `doctor_db`: Manages doctors and availability slots.
   - Username: `postgres`, Password: `root`, Port: `5432`.
7. **Native Eclipse & STS Support**:
   - Multi-module Maven structure with native Eclipse `.project` and `.classpath` descriptors.

---

## 📊 Project Presentation & Diagrams

This project includes a **16-slide PowerPoint Presentation** and an **interactive HTML slide deck**:

- **PowerPoint Presentation**: [`hospital_microservices_presentation.pptx`](hospital_microservices_presentation.pptx)
  - Slide 1: Title & Tech Stack Badges
  - Slide 2: Problem Statement & Engineering Goals
  - Slide 3: Microservices System Architecture Topology
  - Slide 4: Eureka Service Registry & Client-Side Load Balancing
  - Slide 5: Spring Cloud API Gateway & Security Filter
  - Slide 6: Spring Security 6 & JJWT Token Lifecycle
  - Slide 7: Spring AI Medical Diagnostic & Symptom Triage Engine
  - Slide 8: Multi-Level Redis Caching Architecture & TTL
  - Slide 9: PostgreSQL Dual-Database Schemas (`patient_db` & `doctor_db`)
  - Slide 10: UML Working Activity Diagram (Patient Triage & Appointment Booking Flow)
  - Slide 11: UML Working Activity Diagram (Doctor Onboarding & Schedule Management)
  - Slide 12: Sequence Diagram (End-to-End API Request Flow)
  - Slide 13: Microservices Test Cases & Verification Matrix
  - Slide 14: Docker Containerization & Multi-Container Topology
  - Slide 15: Step-by-Step Eclipse IDE / STS Setup Guide
  - Slide 16: Project Summary & Future Roadmap
- **Interactive Browser Slide Deck**: Open [`presentation.html`](presentation.html) in any web browser!

---

## 💻 Running in Eclipse IDE / Spring Tool Suite (STS)

### Step 1: Import into Eclipse / STS
1. Open **Eclipse IDE for Enterprise Java** or **Spring Tool Suite (STS)**.
2. Click `File` ➔ `Import...`
3. Expand `Maven` ➔ Select `Existing Maven Projects` ➔ Click `Next`.
4. Click `Browse...` and select this directory:
   `c:\Users\tejas\Downloads\hospital management microservice`
5. Ensure the root `pom.xml` and all 5 submodules are checked:
   - `service-registry`
   - `api-gateway`
   - `auth-service`
   - `doctor-service`
   - `patient-service`
6. Click `Finish`. Eclipse will configure all project dependencies and classpaths automatically.

### Step 2: Launch Order
Run each microservice in Eclipse by opening its main Application class, right-clicking ➔ `Run As` ➔ `Spring Boot App` (or `Java Application`):

1. **`service-registry`**: `com.hospital.registry.ServiceRegistryApplication` (Port 8761)
2. **`auth-service`**: `com.hospital.auth.AuthServiceApplication` (Port 8081)
3. **`doctor-service`**: `com.hospital.doctor.DoctorServiceApplication` (Port 8083)
4. **`patient-service`**: `com.hospital.patient.PatientServiceApplication` (Port 8082)
5. **`api-gateway`**: `com.hospital.gateway.ApiGatewayApplication` (Port 8080)

*Check Eureka Dashboard at [http://localhost:8761](http://localhost:8761) to see all 4 services registered.*

---

## 🐳 Running with Docker

You can build and spin up the complete cluster (PostgreSQL, Redis, Eureka, Gateway, and all 3 microservices) with Docker Compose:

```bash
# Build and start all 7 containers in detached mode
docker-compose up --build -d

# Check cluster health
docker-compose ps

# View live service logs
docker-compose logs -f patient-service

# Stop all containers
docker-compose down -v
```

---

## 📡 REST API Reference

### 1. Authentication Service (`/api/auth`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register a new user (`ROLE_PATIENT`, `ROLE_DOCTOR`, `ROLE_ADMIN`) | Public |
| `POST` | `/api/auth/login` | Authenticate and obtain signed JWT token | Public |
| `GET` | `/api/auth/validate?token=...` | Validate JWT token signature and expiration | Public |

**Sample Login Request:**
```json
POST /api/auth/login
{
  "username": "patient_john",
  "password": "patient123"
}
```

---

### 2. Spring AI Symptom Triage (`/api/patients/ai/symptom-triage`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/patients/ai/symptom-triage` | Submit natural language symptoms for AI diagnostic triage | Protected (JWT) |

**Sample Request:**
```json
POST /api/patients/ai/symptom-triage
{
  "symptoms": "Severe chest pain radiating to left arm and shortness of breath",
  "age": 48,
  "gender": "MALE",
  "durationDays": 1,
  "existingConditions": "Mild hypertension"
}
```

**Sample Response:**
```json
{
  "symptoms": "Severe chest pain radiating to left arm and shortness of breath",
  "urgencyLevel": "EMERGENCY",
  "recommendedDepartment": "Cardiology",
  "diagnosisHypothesis": "Potential Acute Coronary Syndrome or Cardiac Arrhythmia",
  "preliminaryPrecautions": [
    "Seek immediate emergency medical care or call 911/ambulance",
    "Do not exert yourself physically; rest in a seated position",
    "Loosen tight clothing and avoid eating or drinking stimulants"
  ],
  "recommendedLabTests": [
    "12-Lead ECG",
    "Troponin I/T Serum Biomarkers",
    "Echocardiogram",
    "Chest X-Ray"
  ],
  "suggestedDoctors": [
    {
      "id": 1,
      "name": "Dr. Sarah Jenkins",
      "department": "Cardiology",
      "specialization": "Interventional Cardiologist",
      "consultationFee": 150.0,
      "rating": 4.9,
      "experienceYears": 14,
      "isAvailable": true
    }
  ],
  "aiAnalysisSummary": "Spring AI Assessment: Patient presents with symptoms characteristic of Cardiology conditions. Urgency categorized as EMERGENCY. Departmental referral to Cardiology recommended."
}
```

---

### 3. Doctor Service (`/api/doctors`)
| Method | Endpoint | Description | Cache |
|---|---|---|---|
| `GET` | `/api/doctors` | Retrieve all doctors | Redis Cached |
| `GET` | `/api/doctors/{id}` | Retrieve doctor by ID | Redis Cached |
| `GET` | `/api/doctors/department/{dept}` | Find doctors by department | Redis Cached |
| `POST` | `/api/doctors` | Add new doctor | Evicts Cache |
| `GET` | `/api/doctors/{id}/slots` | View available appointment slots | Dynamic |
| `POST` | `/api/doctors/{id}/slots` | Add new availability slot | Dynamic |
| `PUT` | `/api/doctors/slots/{slotId}/book`| Reserve an availability slot | Dynamic |

---

### 4. Patient Service (`/api/patients`)
| Method | Endpoint | Description | Cache |
|---|---|---|---|
| `GET` | `/api/patients` | Retrieve all patients | Redis Cached |
| `GET` | `/api/patients/{id}` | Retrieve patient by ID | Redis Cached |
| `POST` | `/api/patients` | Register new patient profile | Evicts Cache |
| `POST` | `/api/patients/{id}/appointments` | Book appointment with doctor | Dynamic |
| `GET` | `/api/patients/{id}/appointments` | List all patient appointments | Dynamic |

---

## 🧪 Running Automated Tests

Run the PowerShell test suite against the running services:

```powershell
.\test-endpoints.ps1
```

Or run unit tests via Maven:

```bash
mvn test
```
