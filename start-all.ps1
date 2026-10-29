$MVN = "C:\Users\tejas\.m2\wrapper\dists\apache-maven-3.9.16\0daed3be3ebd1c706f0e69e8b07c6b73f5cc4ea3dfce72a8d0ec2e849ca2ddb0\bin\mvn.cmd"
$ROOT = "c:\Users\tejas\Downloads\hospital management microservice"

Write-Host "Starting Service Registry (port 8761)..." -ForegroundColor Yellow
Start-Process -FilePath "cmd.exe" -ArgumentList "/c "$MVN" spring-boot:run" -WorkingDirectory "$ROOT\service-registry" -WindowStyle Normal
