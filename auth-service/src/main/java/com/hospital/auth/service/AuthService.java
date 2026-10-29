package com.hospital.auth.service;

import com.hospital.auth.dto.AuthRequest;
import com.hospital.auth.dto.AuthResponse;
import com.hospital.auth.dto.RegisterRequest;
import com.hospital.auth.model.UserCredential;
import com.hospital.auth.util.JwtService;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class AuthService {

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtService jwtService;

    // Fast in-memory secure user store (can be connected to DB or used standalone)
    private final Map<String, UserCredential> userDatabase = new ConcurrentHashMap<>();

    @PostConstruct
    public void initSampleUsers() {
        registerUser(new RegisterRequest("admin", "admin123", "admin@hospital.com", "ROLE_ADMIN"));
        registerUser(new RegisterRequest("doctor_smith", "doctor123", "smith@hospital.com", "ROLE_DOCTOR"));
        registerUser(new RegisterRequest("patient_john", "patient123", "john@gmail.com", "ROLE_PATIENT"));
    }

    public AuthResponse registerUser(RegisterRequest request) {
        if (userDatabase.containsKey(request.getUsername())) {
            return new AuthResponse(null, request.getUsername(), null, "Username already exists");
        }

        String role = (request.getRole() != null && !request.getRole().isBlank()) 
                ? request.getRole() : "ROLE_PATIENT";

        UserCredential user = new UserCredential(
                request.getUsername(),
                passwordEncoder.encode(request.getPassword()),
                request.getEmail(),
                role
        );
        userDatabase.put(request.getUsername(), user);

        String token = jwtService.generateToken(user.getUsername(), user.getRole());
        return new AuthResponse(token, user.getUsername(), user.getRole(), "User registered successfully");
    }

    public AuthResponse login(AuthRequest request) {
        UserCredential user = userDatabase.get(request.getUsername());
        if (user == null || !passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid username or password");
        }

        String token = jwtService.generateToken(user.getUsername(), user.getRole());
        return new AuthResponse(token, user.getUsername(), user.getRole(), "Login successful");
    }

    public boolean validateToken(String token) {
        return jwtService.validateToken(token);
    }
}
