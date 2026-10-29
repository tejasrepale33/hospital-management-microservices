import api from './api';

export const doctorService = {
  // Get all doctors (Redis cached)
  getAllDoctors: async () => {
    const response = await api.get('/api/doctors');
    return response.data;
  },

  // Get doctor by ID (Redis cached)
  getDoctorById: async (id) => {
    const response = await api.get(`/api/doctors/${id}`);
    return response.data;
  },

  // Filter by department (Redis cached)
  getDoctorsByDepartment: async (department) => {
    const response = await api.get(`/api/doctors/department/${department}`);
    return response.data;
  },

  // Create new doctor (evicts cache)
  createDoctor: async (doctorData) => {
    const response = await api.post('/api/doctors', doctorData);
    return response.data;
  },

  // Update doctor (evicts cache)
  updateDoctor: async (id, doctorData) => {
    const response = await api.put(`/api/doctors/${id}`, doctorData);
    return response.data;
  },

  // Delete doctor (evicts cache)
  deleteDoctor: async (id) => {
    const response = await api.delete(`/api/doctors/${id}`);
    return response.data;
  },

  // Get doctor availability slots
  getDoctorSlots: async (doctorId) => {
    const response = await api.get(`/api/doctors/${doctorId}/slots`);
    return response.data;
  },

  // Add availability slot
  addSlot: async (doctorId, slotData) => {
    const response = await api.post(`/api/doctors/${doctorId}/slots`, slotData);
    return response.data;
  },

  // Book a slot
  bookSlot: async (slotId) => {
    const response = await api.put(`/api/doctors/slots/${slotId}/book`);
    return response.data;
  }
};
