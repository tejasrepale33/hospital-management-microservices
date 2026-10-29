package com.hospital.doctor.repository;

import com.hospital.doctor.entity.AvailabilitySlot;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AvailabilitySlotRepository extends JpaRepository<AvailabilitySlot, Long> {
    List<AvailabilitySlot> findByDoctorId(Long doctorId);
    List<AvailabilitySlot> findByDoctorIdAndIsBookedFalse(Long doctorId);
}
