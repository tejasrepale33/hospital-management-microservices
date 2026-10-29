package com.hospital.doctor.service;

import com.hospital.doctor.entity.AvailabilitySlot;
import com.hospital.doctor.entity.Doctor;
import com.hospital.doctor.repository.AvailabilitySlotRepository;
import com.hospital.doctor.repository.DoctorRepository;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class DoctorService {

    private static final Logger log = LoggerFactory.getLogger(DoctorService.class);

    @Autowired
    private DoctorRepository doctorRepository;

    @Autowired
    private AvailabilitySlotRepository slotRepository;

    @PostConstruct
    public void initSampleDoctors() {
        if (doctorRepository.count() == 0) {
            log.info("Initializing sample doctors in doctor_db...");

            Doctor doc1 = new Doctor("Dr. Sarah Jenkins", "Cardiology", "Interventional Cardiologist",
                    "sarah.jenkins@hospital.com", "+1-555-0101", 150.0, 4.9, 14);
            doc1.addSlot(new AvailabilitySlot("MONDAY", "09:00 AM", "12:00 PM"));
            doc1.addSlot(new AvailabilitySlot("WEDNESDAY", "02:00 PM", "05:00 PM"));

            Doctor doc2 = new Doctor("Dr. Marcus Thorne", "Neurology", "Neurosurgeon & Stroke Specialist",
                    "marcus.thorne@hospital.com", "+1-555-0102", 200.0, 4.8, 18);
            doc2.addSlot(new AvailabilitySlot("TUESDAY", "10:00 AM", "01:00 PM"));
            doc2.addSlot(new AvailabilitySlot("THURSDAY", "03:00 PM", "06:00 PM"));

            Doctor doc3 = new Doctor("Dr. Priya Sharma", "General Medicine", "Internal Medicine Consultant",
                    "priya.sharma@hospital.com", "+1-555-0103", 80.0, 4.7, 9);
            doc3.addSlot(new AvailabilitySlot("MONDAY", "08:00 AM", "01:00 PM"));
            doc3.addSlot(new AvailabilitySlot("FRIDAY", "09:00 AM", "02:00 PM"));

            Doctor doc4 = new Doctor("Dr. David Lee", "Dermatology", "Clinical & Cosmetic Dermatologist",
                    "david.lee@hospital.com", "+1-555-0104", 110.0, 4.9, 11);
            doc4.addSlot(new AvailabilitySlot("WEDNESDAY", "10:00 AM", "03:00 PM"));

            Doctor doc5 = new Doctor("Dr. Emily Clark", "Orthopedics", "Joint Replacement Surgeon",
                    "emily.clark@hospital.com", "+1-555-0105", 160.0, 4.8, 12);
            doc5.addSlot(new AvailabilitySlot("THURSDAY", "09:00 AM", "01:00 PM"));

            doctorRepository.saveAll(List.of(doc1, doc2, doc3, doc4, doc5));
            log.info("Initialized 5 sample doctors with availability slots.");
        }
    }

    @Cacheable(value = "doctors", key = "'all'")
    @Transactional(readOnly = true)
    public List<Doctor> getAllDoctors() {
        log.info("Fetching all doctors from PostgreSQL database (Cache Miss)");
        return doctorRepository.findAll();
    }

    @Cacheable(value = "doctors", key = "#id")
    @Transactional(readOnly = true)
    public Optional<Doctor> getDoctorById(Long id) {
        log.info("Fetching doctor id {} from PostgreSQL database (Cache Miss)", id);
        return doctorRepository.findById(id);
    }

    @Cacheable(value = "doctors_dept", key = "#department.toLowerCase()")
    @Transactional(readOnly = true)
    public List<Doctor> getDoctorsByDepartment(String department) {
        log.info("Fetching doctors for department '{}' from PostgreSQL database", department);
        return doctorRepository.findByDepartmentIgnoreCase(department);
    }

    public List<Doctor> getDoctorsBySpecialization(String specialization) {
        return doctorRepository.findBySpecializationContainingIgnoreCase(specialization);
    }

    @CacheEvict(value = {"doctors", "doctors_dept"}, allEntries = true)
    @Transactional
    public Doctor saveDoctor(Doctor doctor) {
        log.info("Evicting doctors cache and saving doctor: {}", doctor.getName());
        return doctorRepository.save(doctor);
    }

    @CacheEvict(value = {"doctors", "doctors_dept"}, allEntries = true)
    @Transactional
    public Optional<Doctor> updateDoctor(Long id, Doctor updatedDoctor) {
        return doctorRepository.findById(id).map(existing -> {
            existing.setName(updatedDoctor.getName());
            existing.setDepartment(updatedDoctor.getDepartment());
            existing.setSpecialization(updatedDoctor.getSpecialization());
            existing.setEmail(updatedDoctor.getEmail());
            existing.setPhone(updatedDoctor.getPhone());
            existing.setConsultationFee(updatedDoctor.getConsultationFee());
            existing.setRating(updatedDoctor.getRating());
            existing.setExperienceYears(updatedDoctor.getExperienceYears());
            existing.setIsAvailable(updatedDoctor.getIsAvailable());
            return doctorRepository.save(existing);
        });
    }

    @CacheEvict(value = {"doctors", "doctors_dept"}, allEntries = true)
    @Transactional
    public boolean deleteDoctor(Long id) {
        if (doctorRepository.existsById(id)) {
            doctorRepository.deleteById(id);
            return true;
        }
        return false;
    }

    public List<AvailabilitySlot> getAvailableSlots(Long doctorId) {
        return slotRepository.findByDoctorIdAndIsBookedFalse(doctorId);
    }

    @Transactional
    public AvailabilitySlot addSlot(Long doctorId, AvailabilitySlot slot) {
        Doctor doctor = doctorRepository.findById(doctorId)
                .orElseThrow(() -> new RuntimeException("Doctor not found with id: " + doctorId));
        doctor.addSlot(slot);
        return slotRepository.save(slot);
    }

    @Transactional
    public boolean bookSlot(Long slotId) {
        return slotRepository.findById(slotId).map(slot -> {
            if (Boolean.TRUE.equals(slot.getIsBooked())) {
                return false;
            }
            slot.setIsBooked(true);
            slotRepository.save(slot);
            return true;
        }).orElse(false);
    }
}
