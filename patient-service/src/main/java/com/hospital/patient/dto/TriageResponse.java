package com.hospital.patient.dto;

import java.util.List;

public class TriageResponse {
    private String symptoms;
    private String urgencyLevel; // EMERGENCY, HIGH, MODERATE, LOW
    private String recommendedDepartment;
    private String diagnosisHypothesis;
    private List<String> preliminaryPrecautions;
    private List<String> recommendedLabTests;
    private List<DoctorSummaryDto> suggestedDoctors;
    private String aiAnalysisSummary;

    public TriageResponse() {}

    public String getSymptoms() {
        return symptoms;
    }

    public void setSymptoms(String symptoms) {
        this.symptoms = symptoms;
    }

    public String getUrgencyLevel() {
        return urgencyLevel;
    }

    public void setUrgencyLevel(String urgencyLevel) {
        this.urgencyLevel = urgencyLevel;
    }

    public String getRecommendedDepartment() {
        return recommendedDepartment;
    }

    public void setRecommendedDepartment(String recommendedDepartment) {
        this.recommendedDepartment = recommendedDepartment;
    }

    public String getDiagnosisHypothesis() {
        return diagnosisHypothesis;
    }

    public void setDiagnosisHypothesis(String diagnosisHypothesis) {
        this.diagnosisHypothesis = diagnosisHypothesis;
    }

    public List<String> getPreliminaryPrecautions() {
        return preliminaryPrecautions;
    }

    public void setPreliminaryPrecautions(List<String> preliminaryPrecautions) {
        this.preliminaryPrecautions = preliminaryPrecautions;
    }

    public List<String> getRecommendedLabTests() {
        return recommendedLabTests;
    }

    public void setRecommendedLabTests(List<String> recommendedLabTests) {
        this.recommendedLabTests = recommendedLabTests;
    }

    public List<DoctorSummaryDto> getSuggestedDoctors() {
        return suggestedDoctors;
    }

    public void setSuggestedDoctors(List<DoctorSummaryDto> suggestedDoctors) {
        this.suggestedDoctors = suggestedDoctors;
    }

    public String getAiAnalysisSummary() {
        return aiAnalysisSummary;
    }

    public void setAiAnalysisSummary(String aiAnalysisSummary) {
        this.aiAnalysisSummary = aiAnalysisSummary;
    }
}
