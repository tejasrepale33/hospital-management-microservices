package com.hospital.doctor.entity;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "doctors")
public class Doctor implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String department; // e.g. Cardiology, Dermatology, Neurology, Orthopedics, General Medicine

    @Column(nullable = false)
    private String specialization; // e.g. Interventional Cardiologist, Pediatric Neurologist

    @Column(nullable = false, unique = true)
    private String email;

    private String phone;
    private Double consultationFee;
    private Double rating; // 1.0 to 5.0
    private Integer experienceYears;
    private Boolean isAvailable;

    @OneToMany(mappedBy = "doctor", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
    @JsonManagedReference
    private List<AvailabilitySlot> availabilitySlots = new ArrayList<>();

    public Doctor() {
        this.isAvailable = true;
    }

    public Doctor(String name, String department, String specialization, String email, String phone, 
                  Double consultationFee, Double rating, Integer experienceYears) {
        this.name = name;
        this.department = department;
        this.specialization = specialization;
        this.email = email;
        this.phone = phone;
        this.consultationFee = consultationFee;
        this.rating = rating;
        this.experienceYears = experienceYears;
        this.isAvailable = true;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getSpecialization() {
        return specialization;
    }

    public void setSpecialization(String specialization) {
        this.specialization = specialization;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public Double getConsultationFee() {
        return consultationFee;
    }

    public void setConsultationFee(Double consultationFee) {
        this.consultationFee = consultationFee;
    }

    public Double getRating() {
        return rating;
    }

    public void setRating(Double rating) {
        this.rating = rating;
    }

    public Integer getExperienceYears() {
        return experienceYears;
    }

    public void setExperienceYears(Integer experienceYears) {
        this.experienceYears = experienceYears;
    }

    public Boolean getIsAvailable() {
        return isAvailable;
    }

    public void setIsAvailable(Boolean available) {
        isAvailable = available;
    }

    public List<AvailabilitySlot> getAvailabilitySlots() {
        return availabilitySlots;
    }

    public void setAvailabilitySlots(List<AvailabilitySlot> availabilitySlots) {
        this.availabilitySlots = availabilitySlots;
    }

    public void addSlot(AvailabilitySlot slot) {
        availabilitySlots.add(slot);
        slot.setDoctor(this);
    }
}
