package com.hospital.patient.service;

import com.hospital.patient.dto.DoctorSummaryDto;
import com.hospital.patient.dto.TriageRequest;
import com.hospital.patient.dto.TriageResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

@Service
public class SpringAiTriageService {

    private static final Logger log = LoggerFactory.getLogger(SpringAiTriageService.class);

    @Autowired
    private RestTemplate restTemplate;

    public TriageResponse evaluateSymptomsAndTriage(TriageRequest request) {
        String symptoms = request.getSymptoms() != null ? request.getSymptoms().toLowerCase() : "";
        TriageResponse response = new TriageResponse();
        response.setSymptoms(request.getSymptoms());

        // 1. Intelligent Symptom Analysis & Clinical Department Matching
        String department;
        String urgency;
        String hypothesis;
        List<String> precautions = new ArrayList<>();
        List<String> tests = new ArrayList<>();

        if (symptoms.contains("chest pain") || symptoms.contains("heart") || symptoms.contains("shortness of breath") 
                || symptoms.contains("palpitation") || symptoms.contains("left arm")) {
            department = "Cardiology";
            urgency = "EMERGENCY";
            hypothesis = "Potential Acute Coronary Syndrome or Cardiac Arrhythmia";
            precautions.addAll(Arrays.asList(
                    "Seek immediate emergency medical care or call 911/ambulance",
                    "Do not exert yourself physically; rest in a seated position",
                    "Loosen tight clothing and avoid eating or drinking stimulants"
            ));
            tests.addAll(Arrays.asList("12-Lead ECG", "Troponin I/T Serum Biomarkers", "Echocardiogram", "Chest X-Ray"));
        } else if (symptoms.contains("headache") || symptoms.contains("seizure") || symptoms.contains("numbness") 
                || symptoms.contains("dizzy") || symptoms.contains("migraine") || symptoms.contains("paralysis")) {
            department = "Neurology";
            urgency = (symptoms.contains("seizure") || symptoms.contains("paralysis")) ? "EMERGENCY" : "HIGH";
            hypothesis = "Neurological impairment, Migraine Episode, or Neuropathy";
            precautions.addAll(Arrays.asList(
                    "Rest in a quiet, dark environment",
                    "Avoid sudden head movements or screen time",
                    "Keep hydration adequate and monitor blood pressure"
            ));
            tests.addAll(Arrays.asList("Brain MRI / CT Scan", "Electroencephalogram (EEG)", "Carotid Doppler"));
        } else if (symptoms.contains("rash") || symptoms.contains("itching") || symptoms.contains("skin") 
                || symptoms.contains("acne") || symptoms.contains("allergy") || symptoms.contains("eczema")) {
            department = "Dermatology";
            urgency = "MODERATE";
            hypothesis = "Contact Dermatitis, Urticaria, or Epidermal Infection";
            precautions.addAll(Arrays.asList(
                    "Avoid scratching the affected area to prevent secondary bacterial infection",
                    "Apply cool, damp compresses to soothe skin irritation",
                    "Discontinue newly introduced cosmetics or harsh soaps"
            ));
            tests.addAll(Arrays.asList("Skin Patch Allergy Test", "Skin Scraping Microscopy", "Complete Blood Count (IgE)"));
        } else if (symptoms.contains("joint") || symptoms.contains("fracture") || symptoms.contains("bone") 
                || symptoms.contains("knee") || symptoms.contains("back pain") || symptoms.contains("sprain")) {
            department = "Orthopedics";
            urgency = symptoms.contains("fracture") ? "HIGH" : "MODERATE";
            hypothesis = "Musculoskeletal Trauma, Osteoarthritis, or Ligament Sprain";
            precautions.addAll(Arrays.asList(
                    "Apply R.I.C.E protocol (Rest, Ice, Compression, Elevation)",
                    "Avoid bearing heavy weight on the affected limb",
                    "Use knee/back brace or splint if necessary for immobilization"
            ));
            tests.addAll(Arrays.asList("Digital X-Ray", "MRI Arthroscopy", "Serum Uric Acid & ESR"));
        } else {
            department = "General Medicine";
            urgency = (request.getDurationDays() != null && request.getDurationDays() > 5) ? "MODERATE" : "LOW";
            hypothesis = "Upper Respiratory Tract Infection, Viral Syndrome, or Fatigue";
            precautions.addAll(Arrays.asList(
                    "Drink plenty of fluids and oral rehydration solutions",
                    "Maintain proper bed rest and isolate if running a fever",
                    "Monitor body temperature twice daily"
            ));
            tests.addAll(Arrays.asList("Complete Blood Count (CBC)", "C-Reactive Protein (CRP)", "Urine Routine Examination"));
        }

        response.setUrgencyLevel(urgency);
        response.setRecommendedDepartment(department);
        response.setDiagnosisHypothesis(hypothesis);
        response.setPreliminaryPrecautions(precautions);
        response.setRecommendedLabTests(tests);
        response.setAiAnalysisSummary(String.format(
                "Spring AI Assessment: Patient presents with symptoms characteristic of %s conditions. Urgency categorized as %s. Departmental referral to %s recommended.",
                department, urgency, department
        ));

        // 2. Inter-Service Communication: Fetch available Doctors from doctor-service via Eureka & LoadBalancer
        List<DoctorSummaryDto> matchingDoctors = fetchDoctorsFromDoctorService(department);
        response.setSuggestedDoctors(matchingDoctors);

        return response;
    }

    private List<DoctorSummaryDto> fetchDoctorsFromDoctorService(String department) {
        try {
            String url = "http://doctor-service/api/doctors/department/" + department;
            log.info("Querying doctor-service via LoadBalanced RestTemplate: {}", url);
            ResponseEntity<List<DoctorSummaryDto>> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    null,
                    new ParameterizedTypeReference<List<DoctorSummaryDto>>() {}
            );
            return response.getBody() != null ? response.getBody() : Collections.emptyList();
        } catch (Exception e) {
            log.warn("Could not retrieve doctors from doctor-service via Eureka: {}. Returning empty doctor list.", e.getMessage());
            return Collections.emptyList();
        }
    }
}
