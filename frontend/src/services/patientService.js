import api from './api';

export const patientService = {
  // Get all patients
  getAllPatients: async () => {
    const response = await api.get('/api/patients');
    return response.data;
  },

  // Get patient by id
  getPatientById: async (id) => {
    const response = await api.get(`/api/patients/${id}`);
    return response.data;
  },

  // Register new patient record
  createPatient: async (patientData) => {
    const response = await api.post('/api/patients', patientData);
    return response.data;
  },

  // Spring AI Clinical Symptom Triage
  triageSymptoms: async (triageData) => {
    const response = await api.post('/api/patients/ai/symptom-triage', triageData);
    return response.data;
  },

  // Book appointment
  bookAppointment: async (patientId, appointmentData) => {
    const response = await api.post(`/api/patients/${patientId}/appointments`, appointmentData);
    return response.data;
  },

  // Get appointments for a patient
  getAppointments: async (patientId) => {
    const response = await api.get(`/api/patients/${patientId}/appointments`);
    return response.data;
  }
};
