package com.hospital.patient;

import com.hospital.patient.dto.TriageRequest;
import com.hospital.patient.dto.TriageResponse;
import com.hospital.patient.service.SpringAiTriageService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class PatientServiceTest {

    @Autowired(required = false)
    private SpringAiTriageService aiTriageService;

    @Test
    public void testAiCardiacEmergencyTriage() {
        if (aiTriageService != null) {
            TriageRequest request = new TriageRequest(
                    "Severe chest pain radiating to left arm and shortness of breath",
                    52,
                    "MALE",
                    1,
                    "Hypertension"
            );

            TriageResponse response = aiTriageService.evaluateSymptomsAndTriage(request);

            assertNotNull(response);
            assertEquals("Cardiology", response.getRecommendedDepartment());
            assertEquals("EMERGENCY", response.getUrgencyLevel());
            assertNotNull(response.getPreliminaryPrecautions());
            assertFalse(response.getPreliminaryPrecautions().isEmpty());
        }
    }

    @Test
    public void testAiDermatologyTriage() {
        if (aiTriageService != null) {
            TriageRequest request = new TriageRequest(
                    "Red skin rash and severe itching on arms",
                    26,
                    "FEMALE",
                    3,
                    "None"
            );

            TriageResponse response = aiTriageService.evaluateSymptomsAndTriage(request);

            assertNotNull(response);
            assertEquals("Dermatology", response.getRecommendedDepartment());
            assertEquals("MODERATE", response.getUrgencyLevel());
        }
    }
}
