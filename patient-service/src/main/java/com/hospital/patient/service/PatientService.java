package com.hospital.patient.service;

import com.hospital.patient.entity.Appointment;
import com.hospital.patient.entity.Patient;
import com.hospital.patient.repository.AppointmentRepository;
import com.hospital.patient.repository.PatientRepository;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class PatientService {

    private static final Logger log = LoggerFactory.getLogger(PatientService.class);

    @Autowired
    private PatientRepository patientRepository;

    @Autowired
    private AppointmentRepository appointmentRepository;

    @PostConstruct
    public void initSamplePatients() {
        if (patientRepository.count() == 0) {
            log.info("Initializing sample patients in patient_db...");

            Patient p1 = new Patient("John", "Doe", "john.doe@gmail.com", "+1-555-1101", 38,
                    "MALE", "O+", "742 Evergreen Terrace, Springfield", "+1-555-9991", "Mild seasonal asthma");
            p1.addAppointment(new Appointment(1L, "Dr. Sarah Jenkins", "Cardiology",
                    LocalDate.now().plusDays(2), "09:00 AM - 10:00 AM", "Chest tightness during exercise", "Regular follow-up"));

            Patient p2 = new Patient("Alice", "Smith", "alice.smith@gmail.com", "+1-555-1102", 29,
                    "FEMALE", "A+", "221B Baker Street, London", "+1-555-9992", "No known chronic illnesses");
            p2.addAppointment(new Appointment(4L, "Dr. David Lee", "Dermatology",
                    LocalDate.now().plusDays(3), "10:00 AM - 11:00 AM", "Skin allergy on wrists", "First consultation"));

            Patient p3 = new Patient("Robert", "Williams", "robert.w@gmail.com", "+1-555-1103", 54,
                    "MALE", "B+", "10 Downing Street, London", "+1-555-9993", "Type 2 Diabetes, Hypertension");

            patientRepository.saveAll(List.of(p1, p2, p3));
            log.info("Initialized 3 sample patients with appointments.");
        }
    }

    @Cacheable(value = "patients", key = "'all'")
    @Transactional(readOnly = true)
    public List<Patient> getAllPatients() {
        log.info("Fetching all patients from PostgreSQL database (Cache Miss)");
        return patientRepository.findAll();
    }

    @Cacheable(value = "patients", key = "#id")
    @Transactional(readOnly = true)
    public Optional<Patient> getPatientById(Long id) {
        log.info("Fetching patient id {} from PostgreSQL database (Cache Miss)", id);
        return patientRepository.findById(id);
    }

    @CacheEvict(value = "patients", allEntries = true)
    @Transactional
    public Patient savePatient(Patient patient) {
        log.info("Evicting patients cache and saving patient: {} {}", patient.getFirstName(), patient.getLastName());
        return patientRepository.save(patient);
    }

    @CacheEvict(value = "patients", allEntries = true)
    @Transactional
    public Optional<Patient> updatePatient(Long id, Patient updated) {
        return patientRepository.findById(id).map(existing -> {
            existing.setFirstName(updated.getFirstName());
            existing.setLastName(updated.getLastName());
            existing.setEmail(updated.getEmail());
            existing.setPhone(updated.getPhone());
            existing.setAge(updated.getAge());
            existing.setGender(updated.getGender());
            existing.setBloodGroup(updated.getBloodGroup());
            existing.setAddress(updated.getAddress());
            existing.setEmergencyContact(updated.getEmergencyContact());
            existing.setMedicalHistory(updated.getMedicalHistory());
            return patientRepository.save(existing);
        });
    }

    @CacheEvict(value = "patients", allEntries = true)
    @Transactional
    public boolean deletePatient(Long id) {
        if (patientRepository.existsById(id)) {
            patientRepository.deleteById(id);
            return true;
        }
        return false;
    }

    @Transactional
    public Appointment bookAppointment(Long patientId, Appointment appointment) {
        Patient patient = patientRepository.findById(patientId)
                .orElseThrow(() -> new RuntimeException("Patient not found with id: " + patientId));
        patient.addAppointment(appointment);
        return appointmentRepository.save(appointment);
    }

    public List<Appointment> getPatientAppointments(Long patientId) {
        return appointmentRepository.findByPatientId(patientId);
    }
}
