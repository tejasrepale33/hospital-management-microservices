package com.hospital.auth;

import com.hospital.auth.dto.AuthRequest;
import com.hospital.auth.dto.AuthResponse;
import com.hospital.auth.dto.RegisterRequest;
import com.hospital.auth.service.AuthService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class AuthServiceTest {

    @Autowired
    private AuthService authService;

    @Test
    public void testUserRegistrationAndLogin() {
        String username = "test_user_" + System.currentTimeMillis();
        RegisterRequest registerRequest = new RegisterRequest(username, "Password@123", "test@hospital.com", "ROLE_PATIENT");
        AuthResponse regResponse = authService.registerUser(registerRequest);

        assertNotNull(regResponse);
        assertNotNull(regResponse.getToken(), "Token should not be null upon registration");
        assertEquals(username, regResponse.getUsername());

        // Test Login
        AuthRequest loginRequest = new AuthRequest(username, "Password@123");
        AuthResponse loginResponse = authService.login(loginRequest);

        assertNotNull(loginResponse);
        assertNotNull(loginResponse.getToken());
        assertTrue(authService.validateToken(loginResponse.getToken()));
    }
}
