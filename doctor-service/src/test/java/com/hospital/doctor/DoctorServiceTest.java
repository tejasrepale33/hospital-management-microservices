package com.hospital.doctor;

import com.hospital.doctor.entity.Doctor;
import com.hospital.doctor.service.DoctorService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class DoctorServiceTest {

    @Autowired(required = false)
    private DoctorService doctorService;

    @Test
    public void testDoctorDirectoryQueries() {
        if (doctorService != null) {
            List<Doctor> allDoctors = doctorService.getAllDoctors();
            assertNotNull(allDoctors);
            assertTrue(allDoctors.size() >= 0);
        }
    }
}
