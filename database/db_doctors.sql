INSERT INTO doctor_login (username, password_hash, is_active) VALUES
('gastro_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('resp_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('cardio_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('neuro_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('mental_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('derma_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('endo_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('uro_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('ortho_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('hepatic_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('general_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('hema_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('infect_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE),
('vascular_doc', '8a7c9a8c9a9f1f26c8c4d76c18c35e6c9b8f97e7b07a44d2a0d1c4f77c0f1c88', TRUE);



INSERT INTO doctors
(doctor_id, full_name, specialization, license_number, years_of_experience, email, phone)
VALUES
(1, 'Dr. Gastro Specialist', 'GASTROINTESTINAL', 'LIC-GASTRO-001', 10, 'gastro@careassist.com', '9000000001'),
(2, 'Dr. Pulmonologist', 'RESPIRATORY', 'LIC-RESP-002', 9, 'resp@careassist.com', '9000000002'),
(3, 'Dr. Cardiologist', 'CARDIOVASCULAR', 'LIC-CARDIO-003', 12, 'cardio@careassist.com', '9000000003'),
(4, 'Dr. Neurologist', 'NEUROLOGICAL', 'LIC-NEURO-004', 11, 'neuro@careassist.com', '9000000004'),
(5, 'Dr. Psychiatrist', 'MENTAL_HEALTH', 'LIC-MENTAL-005', 8, 'mental@careassist.com', '9000000005'),
(6, 'Dr. Dermatologist', 'DERMATOLOGICAL', 'LIC-DERMA-006', 7, 'derma@careassist.com', '9000000006'),
(7, 'Dr. Endocrinologist', 'ENDOCRINE_METABOLIC', 'LIC-ENDO-007', 10, 'endo@careassist.com', '9000000007'),
(8, 'Dr. Urologist', 'UROLOGICAL', 'LIC-URO-008', 9, 'uro@careassist.com', '9000000008'),
(9, 'Dr. Orthopedic', 'MUSCULOSKELETAL', 'LIC-ORTHO-009', 13, 'ortho@careassist.com', '9000000009'),
(10, 'Dr. Hepatologist', 'HEPATIC', 'LIC-HEP-010', 11, 'hepatic@careassist.com', '9000000010'),
(11, 'Dr. General Physician', 'GENERAL', 'LIC-GEN-011', 15, 'general@careassist.com', '9000000011'),
(12, 'Dr. Hematologist', 'HEMATOLOGICAL', 'LIC-HEMA-012', 10, 'hema@careassist.com', '9000000012'),
(13, 'Dr. Infectious Disease Specialist', 'INFECTIOUS', 'LIC-INF-013', 12, 'infect@careassist.com', '9000000013'),
(14, 'Dr. Vascular Surgeon', 'VASCULAR', 'LIC-VASC-014', 14, 'vascular@careassist.com', '9000000014');

