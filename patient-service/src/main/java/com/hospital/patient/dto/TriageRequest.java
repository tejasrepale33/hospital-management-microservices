package com.hospital.patient.dto;

public class TriageRequest {
    private String symptoms;
    private Integer age;
    private String gender;
    private Integer durationDays;
    private String existingConditions;

    public TriageRequest() {}

    public TriageRequest(String symptoms, Integer age, String gender, Integer durationDays, String existingConditions) {
        this.symptoms = symptoms;
        this.age = age;
        this.gender = gender;
        this.durationDays = durationDays;
        this.existingConditions = existingConditions;
    }

    public String getSymptoms() {
        return symptoms;
    }

    public void setSymptoms(String symptoms) {
        this.symptoms = symptoms;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public Integer getDurationDays() {
        return durationDays;
    }

    public void setDurationDays(Integer durationDays) {
        this.durationDays = durationDays;
    }

    public String getExistingConditions() {
        return existingConditions;
    }

    public void setExistingConditions(String existingConditions) {
        this.existingConditions = existingConditions;
    }
}
