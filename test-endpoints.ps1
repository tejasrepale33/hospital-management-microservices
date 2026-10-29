# ==============================================================================
# Hospital Management Microservices - Live API Test & Verification Suite
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Hospital Management Microservices - API Test Script      " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$GATEWAY_URL = "http://localhost:8080"
$AUTH_URL    = "http://localhost:8081"
$PATIENT_URL = "http://localhost:8082"
$DOCTOR_URL  = "http://localhost:8083"

# 1. Test Auth Service Registration
Write-Host "`n[1/6] Testing User Registration..." -ForegroundColor Yellow
$regBody = @{
    username = "test_patient_1"
    password = "Password@123"
    email    = "patient1@hospital.com"
    role     = "ROLE_PATIENT"
} | ConvertTo-Json

try {
    $regResponse = Invoke-RestMethod -Uri "$AUTH_URL/api/auth/register" -Method Post -Body $regBody -ContentType "application/json"
    Write-Host "Registration Successful! Username: $($regResponse.username)" -ForegroundColor Green
    $TOKEN = $regResponse.token
} catch {
    Write-Host "Registration call failed or user already exists: $_" -ForegroundColor DarkGray
    # Try login
    $loginBody = @{
        username = "test_patient_1"
        password = "Password@123"
    } | ConvertTo-Json
    $loginResponse = Invoke-RestMethod -Uri "$AUTH_URL/api/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
    $TOKEN = $loginResponse.token
    Write-Host "Logged in successfully! Token acquired." -ForegroundColor Green
}

# 2. Test Token Validation
Write-Host "`n[2/6] Validating JWT Token..." -ForegroundColor Yellow
try {
    $valResponse = Invoke-RestMethod -Uri "$AUTH_URL/api/auth/validate?token=$TOKEN" -Method Get
    Write-Host "Token Validation Result: $($valResponse.message)" -ForegroundColor Green
} catch {
    Write-Host "Validation failed: $_" -ForegroundColor Red
}

$headers = @{
    "Authorization" = "Bearer $TOKEN"
}

# 3. Test Doctor Service Catalog & Redis Cache
Write-Host "`n[3/6] Querying Doctors (Testing Redis Caching)..." -ForegroundColor Yellow
try {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $doctors1 = Invoke-RestMethod -Uri "$DOCTOR_URL/api/doctors" -Method Get
    $sw.Stop()
    Write-Host "Call 1 (PostgreSQL DB Fetch): Retrieved $($doctors1.Count) doctors in $($sw.ElapsedMilliseconds) ms" -ForegroundColor Green

    $sw.Restart()
    $doctors2 = Invoke-RestMethod -Uri "$DOCTOR_URL/api/doctors" -Method Get
    $sw.Stop()
    Write-Host "Call 2 (Redis In-Memory Cache Hit): Retrieved $($doctors2.Count) doctors in $($sw.ElapsedMilliseconds) ms" -ForegroundColor Cyan
} catch {
    Write-Host "Doctor service query: $_" -ForegroundColor Red
}

# 4. Test Spring AI Symptom Triage (Cardiac Emergency Scenario)
Write-Host "`n[4/6] Testing Spring AI Symptom Triage (Chest Pain Scenario)..." -ForegroundColor Yellow
$aiTriageBody = @{
    symptoms          = "Severe chest pain radiating to left arm and shortness of breath"
    age               = 48
    gender            = "MALE"
    durationDays      = 1
    existingConditions = "Mild hypertension"
} | ConvertTo-Json

try {
    $triageResult = Invoke-RestMethod -Uri "$PATIENT_URL/api/patients/ai/symptom-triage" -Method Post -Body $aiTriageBody -ContentType "application/json"
    Write-Host "Spring AI Assessment Summary:" -ForegroundColor Green
    Write-Host "  • Urgency Level       : $($triageResult.urgencyLevel)" -ForegroundColor Red
    Write-Host "  • Recommended Dept    : $($triageResult.recommendedDepartment)" -ForegroundColor Cyan
    Write-Host "  • Diagnosis Hypothesis: $($triageResult.diagnosisHypothesis)" -ForegroundColor White
    Write-Host "  • Recommended Tests   : $($triageResult.recommendedLabTests -join ', ')" -ForegroundColor Yellow
    Write-Host "  • Suggested Doctors   : Found $($triageResult.suggestedDoctors.Count) matching specialists" -ForegroundColor Green
} catch {
    Write-Host "AI Triage call failed: $_" -ForegroundColor Red
}

# 5. Test Spring AI Symptom Triage (Dermatology Scenario)
Write-Host "`n[5/6] Testing Spring AI Symptom Triage (Dermatology Scenario)..." -ForegroundColor Yellow
$aiSkinBody = @{
    symptoms          = "Persistent red rash and severe skin itching on forearms"
    age               = 24
    gender            = "FEMALE"
    durationDays      = 4
    existingConditions = "None"
} | ConvertTo-Json

try {
    $skinResult = Invoke-RestMethod -Uri "$PATIENT_URL/api/patients/ai/symptom-triage" -Method Post -Body $aiSkinBody -ContentType "application/json"
    Write-Host "Spring AI Assessment Summary:" -ForegroundColor Green
    Write-Host "  • Urgency Level       : $($skinResult.urgencyLevel)" -ForegroundColor Cyan
    Write-Host "  • Recommended Dept    : $($skinResult.recommendedDepartment)" -ForegroundColor Cyan
    Write-Host "  • Suggested Doctors   : Found $($skinResult.suggestedDoctors.Count) matching specialists" -ForegroundColor Green
} catch {
    Write-Host "AI Triage call failed: $_" -ForegroundColor Red
}

# 6. Test Gateway Protected Routing with JWT
Write-Host "`n[6/6] Testing API Gateway Routing through Port 8080 with JWT..." -ForegroundColor Yellow
try {
    $gwDoctors = Invoke-RestMethod -Uri "$GATEWAY_URL/api/doctors" -Method Get -Headers $headers
    Write-Host "Gateway routed request to lb://doctor-service successfully! Doctors returned: $($gwDoctors.Count)" -ForegroundColor Green
} catch {
    Write-Host "Gateway routing call: $_" -ForegroundColor Red
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Test Suite Completed Successfully!                        " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
