INSERT INTO admin_login (username, password_hash, is_active)
VALUES (
    'admin',
    '7676aaafb027c825bd9abab78b234070e702752f625b752e55e55b48e607e358',
    TRUE
);

INSERT INTO symptoms_master (symptom_name, category) VALUES
('abdominal_pain', 'GASTROINTESTINAL'),
('abnormal_menstruation', 'ENDOCRINE_METABOLIC'),
('acidity', 'GASTROINTESTINAL'),
('acute_liver_failure', 'HEPATIC'),
('altered_sensorium', 'NEUROLOGICAL'),
('anxiety', 'MENTAL_HEALTH'),
('back_pain', 'MUSCULOSKELETAL'),
('belly_pain', 'GASTROINTESTINAL'),
('blackheads', 'DERMATOLOGICAL'),
('bladder_discomfort', 'UROLOGICAL'),
('blister', 'DERMATOLOGICAL'),
('blood_in_sputum', 'RESPIRATORY'),
('bloody_stool', 'GASTROINTESTINAL'),
('blurred_and_distorted_vision', 'NEUROLOGICAL'),
('breathlessness', 'RESPIRATORY'),
('brittle_nails', 'DERMATOLOGICAL'),
('bruising', 'HEMATOLOGICAL'),
('burning_micturition', 'UROLOGICAL'),
('chest_pain', 'CARDIOVASCULAR'),
('chills', 'GENERAL'),
('cold_hands_and_feets', 'CARDIOVASCULAR'),
('coma', 'NEUROLOGICAL'),
('congestion', 'RESPIRATORY'),
('constipation', 'GASTROINTESTINAL'),
('continuous_feel_of_urine', 'UROLOGICAL'),
('continuous_sneezing', 'RESPIRATORY'),
('cough', 'RESPIRATORY'),
('cramps', 'MUSCULOSKELETAL'),
('dark_urine', 'HEPATIC'),
('dehydration', 'GENERAL'),
('depression', 'MENTAL_HEALTH'),
('diarrhoea', 'GASTROINTESTINAL'),
('dischromic_patches', 'DERMATOLOGICAL'),
('distention_of_abdomen', 'GASTROINTESTINAL'),
('dizziness', 'NEUROLOGICAL'),
('drying_and_tingling_lips', 'GENERAL'),
('enlarged_thyroid', 'ENDOCRINE_METABOLIC'),
('excessive_hunger', 'ENDOCRINE_METABOLIC'),
('extra_marital_contacts', 'GENERAL'),
('family_history', 'GENERAL'),
('fast_heart_rate', 'CARDIOVASCULAR'),
('fatigue', 'GENERAL'),
('fluid_overload', 'CARDIOVASCULAR'),
('foul_smell_of_urine', 'UROLOGICAL'),
('headache', 'NEUROLOGICAL'),
('high_fever', 'INFECTIOUS'),
('hip_joint_pain', 'MUSCULOSKELETAL'),
('history_of_alcohol_consumption', 'GENERAL'),
('increased_appetite', 'ENDOCRINE_METABOLIC'),
('indigestion', 'GASTROINTESTINAL'),
('inflammatory_nails', 'DERMATOLOGICAL'),
('internal_itching', 'DERMATOLOGICAL'),
('irregular_sugar_level', 'ENDOCRINE_METABOLIC'),
('irritability', 'MENTAL_HEALTH'),
('irritation_in_anus', 'GASTROINTESTINAL'),
('itching', 'DERMATOLOGICAL'),
('joint_pain', 'MUSCULOSKELETAL'),
('knee_pain', 'MUSCULOSKELETAL'),
('lack_of_concentration', 'MENTAL_HEALTH'),
('lethargy', 'GENERAL'),
('loss_of_appetite', 'GASTROINTESTINAL'),
('loss_of_balance', 'NEUROLOGICAL'),
('loss_of_smell', 'NEUROLOGICAL'),
('malaise', 'GENERAL'),
('mild_fever', 'INFECTIOUS'),
('mood_swings', 'MENTAL_HEALTH'),
('movement_stiffness', 'MUSCULOSKELETAL'),
('mucoid_sputum', 'RESPIRATORY'),
('muscle_pain', 'MUSCULOSKELETAL'),
('muscle_wasting', 'MUSCULOSKELETAL'),
('muscle_weakness', 'MUSCULOSKELETAL'),
('nausea', 'GASTROINTESTINAL'),
('neck_pain', 'MUSCULOSKELETAL'),
('nodal_skin_eruptions', 'DERMATOLOGICAL'),
('obesity', 'ENDOCRINE_METABOLIC'),
('pain_behind_the_eyes', 'NEUROLOGICAL'),
('pain_during_bowel_movements', 'GASTROINTESTINAL'),
('pain_in_anal_region', 'GASTROINTESTINAL'),
('painful_walking', 'MUSCULOSKELETAL'),
('palpitations', 'CARDIOVASCULAR'),
('passage_of_gases', 'GASTROINTESTINAL'),
('patches_in_throat', 'RESPIRATORY'),
('phlegm', 'RESPIRATORY'),
('polyuria', 'UROLOGICAL'),
('prominent_veins_on_calf', 'VASCULAR'),
('puffy_face_and_eyes', 'GENERAL'),
('pus_filled_pimples', 'DERMATOLOGICAL'),
('receiving_blood_transfusion', 'GENERAL'),
('receiving_unsterile_injections', 'GENERAL'),
('red_sore_around_nose', 'DERMATOLOGICAL'),
('red_spots_over_body', 'DERMATOLOGICAL'),
('redness_of_eyes', 'RESPIRATORY'),
('restlessness', 'MENTAL_HEALTH'),
('runny_nose', 'RESPIRATORY'),
('rusty_sputum', 'RESPIRATORY'),
('scurring', 'DERMATOLOGICAL'),
('shivering', 'INFECTIOUS'),
('silver_like_dusting', 'DERMATOLOGICAL'),
('sinus_pressure', 'RESPIRATORY'),
('skin_peeling', 'DERMATOLOGICAL'),
('skin_rash', 'DERMATOLOGICAL'),
('slurred_speech', 'NEUROLOGICAL'),
('small_dents_in_nails', 'DERMATOLOGICAL'),
('spinning_movements', 'NEUROLOGICAL'),
('spotting_urination', 'UROLOGICAL'),
('stiff_neck', 'NEUROLOGICAL'),
('stomach_bleeding', 'GASTROINTESTINAL'),
('stomach_pain', 'GASTROINTESTINAL'),
('sunken_eyes', 'GENERAL'),
('sweating', 'GENERAL'),
('swelled_lymph_nodes', 'INFECTIOUS'),
('swelling_joints', 'MUSCULOSKELETAL'),
('swelling_of_stomach', 'GASTROINTESTINAL'),
('swollen_blood_vessels', 'VASCULAR'),
('swollen_extremeties', 'CARDIOVASCULAR'),
('swollen_legs', 'CARDIOVASCULAR'),
('throat_irritation', 'RESPIRATORY'),
('toxic_look_(typhos)', 'INFECTIOUS'),
('ulcers_on_tongue', 'GASTROINTESTINAL'),
('unsteadiness', 'NEUROLOGICAL'),
('visual_disturbances', 'NEUROLOGICAL'),
('vomiting', 'GASTROINTESTINAL'),
('watering_from_eyes', 'RESPIRATORY'),
('weakness_in_limbs', 'NEUROLOGICAL'),
('weakness_of_one_body_side', 'NEUROLOGICAL'),
('weight_gain', 'ENDOCRINE_METABOLIC'),
('weight_loss', 'ENDOCRINE_METABOLIC'),
('yellow_crust_ooze', 'DERMATOLOGICAL'),
('yellow_urine', 'HEPATIC'),
('yellowing_of_eyes', 'HEPATIC'),
('yellowish_skin', 'HEPATIC');


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
(15, 'Dr. Gastro Specialist', 'GASTROINTESTINAL', 'LIC-GASTRO-001', 10, 'gastro@careassist.com', '9000000001'),
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


UPDATE doctor_login
SET password_hash = '63bbe564aa5c0882355f6dcd6f2241b6f8d02d6f39725966ae564cd310f07850'
WHERE username IN (
  'gastro_doc','resp_doc','cardio_doc','neuro_doc','mental_doc',
  'derma_doc','endo_doc','uro_doc','ortho_doc','hepatic_doc',
  'general_doc','hema_doc','infect_doc','vascular_doc'
);


UPDATE doctor_login SET doctor_id_fk = 15 WHERE username = 'gastro_doc';
UPDATE doctor_login SET doctor_id_fk = 2  WHERE username = 'resp_doc';
UPDATE doctor_login SET doctor_id_fk = 3  WHERE username = 'cardio_doc';
UPDATE doctor_login SET doctor_id_fk = 4  WHERE username = 'neuro_doc';
UPDATE doctor_login SET doctor_id_fk = 5  WHERE username = 'mental_doc';
UPDATE doctor_login SET doctor_id_fk = 6  WHERE username = 'derma_doc';
UPDATE doctor_login SET doctor_id_fk = 7  WHERE username = 'endo_doc';
UPDATE doctor_login SET doctor_id_fk = 8  WHERE username = 'uro_doc';
UPDATE doctor_login SET doctor_id_fk = 9  WHERE username = 'ortho_doc';
UPDATE doctor_login SET doctor_id_fk = 10 WHERE username = 'hepatic_doc';
UPDATE doctor_login SET doctor_id_fk = 11 WHERE username = 'general_doc';
UPDATE doctor_login SET doctor_id_fk = 12 WHERE username = 'hema_doc';
UPDATE doctor_login SET doctor_id_fk = 13 WHERE username = 'infect_doc';
UPDATE doctor_login SET doctor_id_fk = 14 WHERE username = 'vascular_doc';




INSERT INTO diseases (disease_name) VALUES
('Drug Reaction'),
('Malaria'),
('Allergy'),
('Hypothyroidism'),
('Psoriasis'),
('GERD'),
('Chronic cholestasis'),
('hepatitis A'),
('Osteoarthristis'),
('(vertigo) Paroymsal  Positional Vertigo'),
('Hypoglycemia'),
('Acne'),
('Diabetes'),
('Impetigo'),
('Hypertension'),
('Peptic ulcer diseae'),
('Dimorphic hemmorhoids(piles)'),
('Common Cold'),
('Chicken pox'),
('Cervical spondylosis'),
('Hyperthyroidism'),
('Urinary tract infection'),
('Varicose veins'),
('AIDS'),
('Paralysis (brain hemorrhage)'),
('Typhoid'),
('Hepatitis B'),
('Fungal infection'),
('Hepatitis C'),
('Migraine'),
('Bronchial Asthma'),
('Alcoholic hepatitis'),
('Jaundice'),
('Hepatitis E'),
('Dengue'),
('Hepatitis D'),
('Heart attack'),
('Pneumonia'),
('Arthritis'),
('Gastroenteritis'),
('Tuberculosis');

INSERT INTO disease_precautions (disease_id, precaution_text, precaution_order)

-- Drug Reaction
SELECT disease_id, 'stop irritation', 1 FROM diseases WHERE disease_name = 'Drug Reaction'
UNION ALL SELECT disease_id, 'consult nearest hospital', 2 FROM diseases WHERE disease_name = 'Drug Reaction'
UNION ALL SELECT disease_id, 'stop taking drug', 3 FROM diseases WHERE disease_name = 'Drug Reaction'
UNION ALL SELECT disease_id, 'follow up', 4 FROM diseases WHERE disease_name = 'Drug Reaction'

-- Malaria
UNION ALL SELECT disease_id, 'Consult nearest hospital', 1 FROM diseases WHERE disease_name = 'Malaria'
UNION ALL SELECT disease_id, 'avoid oily food', 2 FROM diseases WHERE disease_name = 'Malaria'
UNION ALL SELECT disease_id, 'avoid non veg food', 3 FROM diseases WHERE disease_name = 'Malaria'
UNION ALL SELECT disease_id, 'keep mosquitos out', 4 FROM diseases WHERE disease_name = 'Malaria'

-- Allergy
UNION ALL SELECT disease_id, 'apply calamine', 1 FROM diseases WHERE disease_name = 'Allergy'
UNION ALL SELECT disease_id, 'cover area with bandage', 2 FROM diseases WHERE disease_name = 'Allergy'
UNION ALL SELECT disease_id, 'use ice to compress itching', 3 FROM diseases WHERE disease_name = 'Allergy'

-- Hypothyroidism
UNION ALL SELECT disease_id, 'reduce stress', 1 FROM diseases WHERE disease_name = 'Hypothyroidism'
UNION ALL SELECT disease_id, 'exercise', 2 FROM diseases WHERE disease_name = 'Hypothyroidism'
UNION ALL SELECT disease_id, 'eat healthy', 3 FROM diseases WHERE disease_name = 'Hypothyroidism'
UNION ALL SELECT disease_id, 'get proper sleep', 4 FROM diseases WHERE disease_name = 'Hypothyroidism'

-- Psoriasis
UNION ALL SELECT disease_id, 'wash hands with warm soapy water', 1 FROM diseases WHERE disease_name = 'Psoriasis'
UNION ALL SELECT disease_id, 'stop bleeding using pressure', 2 FROM diseases WHERE disease_name = 'Psoriasis'
UNION ALL SELECT disease_id, 'consult doctor', 3 FROM diseases WHERE disease_name = 'Psoriasis'
UNION ALL SELECT disease_id, 'salt baths', 4 FROM diseases WHERE disease_name = 'Psoriasis'

-- GERD
UNION ALL SELECT disease_id, 'avoid fatty spicy food', 1 FROM diseases WHERE disease_name = 'GERD'
UNION ALL SELECT disease_id, 'avoid lying down after eating', 2 FROM diseases WHERE disease_name = 'GERD'
UNION ALL SELECT disease_id, 'maintain healthy weight', 3 FROM diseases WHERE disease_name = 'GERD'
UNION ALL SELECT disease_id, 'exercise', 4 FROM diseases WHERE disease_name = 'GERD'

-- Chronic cholestasis
UNION ALL SELECT disease_id, 'cold baths', 1 FROM diseases WHERE disease_name = 'Chronic cholestasis'
UNION ALL SELECT disease_id, 'anti itch medicine', 2 FROM diseases WHERE disease_name = 'Chronic cholestasis'
UNION ALL SELECT disease_id, 'consult doctor', 3 FROM diseases WHERE disease_name = 'Chronic cholestasis'
UNION ALL SELECT disease_id, 'eat healthy', 4 FROM diseases WHERE disease_name = 'Chronic cholestasis'

-- hepatitis A
UNION ALL SELECT disease_id, 'Consult nearest hospital', 1 FROM diseases WHERE disease_name = 'hepatitis A'
UNION ALL SELECT disease_id, 'wash hands thoroughly', 2 FROM diseases WHERE disease_name = 'hepatitis A'
UNION ALL SELECT disease_id, 'avoid fatty spicy food', 3 FROM diseases WHERE disease_name = 'hepatitis A'
UNION ALL SELECT disease_id, 'medication', 4 FROM diseases WHERE disease_name = 'hepatitis A'

-- Osteoarthristis
UNION ALL SELECT disease_id, 'acetaminophen', 1 FROM diseases WHERE disease_name = 'Osteoarthristis'
UNION ALL SELECT disease_id, 'consult nearest hospital', 2 FROM diseases WHERE disease_name = 'Osteoarthristis'
UNION ALL SELECT disease_id, 'follow up', 3 FROM diseases WHERE disease_name = 'Osteoarthristis'
UNION ALL SELECT disease_id, 'salt baths', 4 FROM diseases WHERE disease_name = 'Osteoarthristis'

-- (vertigo) Paroymsal Positional Vertigo
UNION ALL SELECT disease_id, 'lie down', 1 FROM diseases WHERE disease_name = '(vertigo) Paroymsal  Positional Vertigo'
UNION ALL SELECT disease_id, 'avoid sudden change in body', 2 FROM diseases WHERE disease_name = '(vertigo) Paroymsal  Positional Vertigo'
UNION ALL SELECT disease_id, 'avoid abrupt head movement', 3 FROM diseases WHERE disease_name = '(vertigo) Paroymsal  Positional Vertigo'
UNION ALL SELECT disease_id, 'relax', 4 FROM diseases WHERE disease_name = '(vertigo) Paroymsal  Positional Vertigo'

-- Hypoglycemia
UNION ALL SELECT disease_id, 'lie down on side', 1 FROM diseases WHERE disease_name = 'Hypoglycemia'
UNION ALL SELECT disease_id, 'check pulse', 2 FROM diseases WHERE disease_name = 'Hypoglycemia'
UNION ALL SELECT disease_id, 'drink sugary drinks', 3 FROM diseases WHERE disease_name = 'Hypoglycemia'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Hypoglycemia'

-- Acne
UNION ALL SELECT disease_id, 'bath twice', 1 FROM diseases WHERE disease_name = 'Acne'
UNION ALL SELECT disease_id, 'avoid fatty spicy food', 2 FROM diseases WHERE disease_name = 'Acne'
UNION ALL SELECT disease_id, 'drink plenty of water', 3 FROM diseases WHERE disease_name = 'Acne'
UNION ALL SELECT disease_id, 'avoid too many products', 4 FROM diseases WHERE disease_name = 'Acne'

-- Diabetes
UNION ALL SELECT disease_id, 'have balanced diet', 1 FROM diseases WHERE disease_name = 'Diabetes'
UNION ALL SELECT disease_id, 'exercise', 2 FROM diseases WHERE disease_name = 'Diabetes'
UNION ALL SELECT disease_id, 'consult doctor', 3 FROM diseases WHERE disease_name = 'Diabetes'
UNION ALL SELECT disease_id, 'follow up', 4 FROM diseases WHERE disease_name = 'Diabetes'

-- Impetigo
UNION ALL SELECT disease_id, 'soak affected area in warm water', 1 FROM diseases WHERE disease_name = 'Impetigo'
UNION ALL SELECT disease_id, 'use antibiotics', 2 FROM diseases WHERE disease_name = 'Impetigo'
UNION ALL SELECT disease_id, 'remove scabs with wet cloth', 3 FROM diseases WHERE disease_name = 'Impetigo'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Impetigo'

-- Hypertension
UNION ALL SELECT disease_id, 'reduce salt intake', 1 FROM diseases WHERE disease_name = 'Hypertension'
UNION ALL SELECT disease_id, 'exercise', 2 FROM diseases WHERE disease_name = 'Hypertension'
UNION ALL SELECT disease_id, 'consult doctor', 3 FROM diseases WHERE disease_name = 'Hypertension'
UNION ALL SELECT disease_id, 'follow up', 4 FROM diseases WHERE disease_name = 'Hypertension'

-- Peptic ulcer diseae
UNION ALL SELECT disease_id, 'avoid spicy food', 1 FROM diseases WHERE disease_name = 'Peptic ulcer diseae'
UNION ALL SELECT disease_id, 'consume probiotics', 2 FROM diseases WHERE disease_name = 'Peptic ulcer diseae'
UNION ALL SELECT disease_id, 'eliminate milk', 3 FROM diseases WHERE disease_name = 'Peptic ulcer diseae'
UNION ALL SELECT disease_id, 'limit alcohol', 4 FROM diseases WHERE disease_name = 'Peptic ulcer diseae'

-- Dimorphic hemmorhoids(piles)
UNION ALL SELECT disease_id, 'avoid fatty spicy food', 1 FROM diseases WHERE disease_name = 'Dimorphic hemmorhoids(piles)'
UNION ALL SELECT disease_id, 'consume witch hazel', 2 FROM diseases WHERE disease_name = 'Dimorphic hemmorhoids(piles)'
UNION ALL SELECT disease_id, 'warm bath with epsom salt', 3 FROM diseases WHERE disease_name = 'Dimorphic hemmorhoids(piles)'
UNION ALL SELECT disease_id, 'consume aloe vera juice', 4 FROM diseases WHERE disease_name = 'Dimorphic hemmorhoids(piles)'

-- Common Cold
UNION ALL SELECT disease_id, 'drink vitamin c rich drinks', 1 FROM diseases WHERE disease_name = 'Common Cold'
UNION ALL SELECT disease_id, 'take vapour', 2 FROM diseases WHERE disease_name = 'Common Cold'
UNION ALL SELECT disease_id, 'avoid cold food', 3 FROM diseases WHERE disease_name = 'Common Cold'
UNION ALL SELECT disease_id, 'keep fever in check', 4 FROM diseases WHERE disease_name = 'Common Cold'

-- Chicken pox
UNION ALL SELECT disease_id, 'use neem in bathing', 1 FROM diseases WHERE disease_name = 'Chicken pox'
UNION ALL SELECT disease_id, 'consume neem leaves', 2 FROM diseases WHERE disease_name = 'Chicken pox'
UNION ALL SELECT disease_id, 'take vaccine', 3 FROM diseases WHERE disease_name = 'Chicken pox'
UNION ALL SELECT disease_id, 'avoid public places', 4 FROM diseases WHERE disease_name = 'Chicken pox'

-- Cervical spondylosis
UNION ALL SELECT disease_id, 'use heating pad', 1 FROM diseases WHERE disease_name = 'Cervical spondylosis'
UNION ALL SELECT disease_id, 'exercise', 2 FROM diseases WHERE disease_name = 'Cervical spondylosis'
UNION ALL SELECT disease_id, 'take pain killers', 3 FROM diseases WHERE disease_name = 'Cervical spondylosis'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Cervical spondylosis'

-- Hyperthyroidism
UNION ALL SELECT disease_id, 'eat healthy', 1 FROM diseases WHERE disease_name = 'Hyperthyroidism'
UNION ALL SELECT disease_id, 'massage', 2 FROM diseases WHERE disease_name = 'Hyperthyroidism'
UNION ALL SELECT disease_id, 'use lemon balm', 3 FROM diseases WHERE disease_name = 'Hyperthyroidism'
UNION ALL SELECT disease_id, 'take radioactive iodine', 4 FROM diseases WHERE disease_name = 'Hyperthyroidism'

-- Urinary tract infection
UNION ALL SELECT disease_id, 'drink plenty of water', 1 FROM diseases WHERE disease_name = 'Urinary tract infection'
UNION ALL SELECT disease_id, 'increase vitamin c intake', 2 FROM diseases WHERE disease_name = 'Urinary tract infection'
UNION ALL SELECT disease_id, 'drink cranberry juice', 3 FROM diseases WHERE disease_name = 'Urinary tract infection'
UNION ALL SELECT disease_id, 'take probiotics', 4 FROM diseases WHERE disease_name = 'Urinary tract infection'

-- Varicose veins
UNION ALL SELECT disease_id, 'lie down flat and raise the leg', 1 FROM diseases WHERE disease_name = 'Varicose veins'
UNION ALL SELECT disease_id, 'use ointment', 2 FROM diseases WHERE disease_name = 'Varicose veins'
UNION ALL SELECT disease_id, 'use vein compression', 3 FROM diseases WHERE disease_name = 'Varicose veins'
UNION ALL SELECT disease_id, 'don’t stand still for long', 4 FROM diseases WHERE disease_name = 'Varicose veins'

-- AIDS
UNION ALL SELECT disease_id, 'avoid open cuts', 1 FROM diseases WHERE disease_name = 'AIDS'
UNION ALL SELECT disease_id, 'wear ppe if possible', 2 FROM diseases WHERE disease_name = 'AIDS'
UNION ALL SELECT disease_id, 'consult doctor', 3 FROM diseases WHERE disease_name = 'AIDS'
UNION ALL SELECT disease_id, 'follow up', 4 FROM diseases WHERE disease_name = 'AIDS'

-- Paralysis (brain hemorrhage)
UNION ALL SELECT disease_id, 'massage', 1 FROM diseases WHERE disease_name = 'Paralysis (brain hemorrhage)'
UNION ALL SELECT disease_id, 'eat healthy', 2 FROM diseases WHERE disease_name = 'Paralysis (brain hemorrhage)'
UNION ALL SELECT disease_id, 'exercise', 3 FROM diseases WHERE disease_name = 'Paralysis (brain hemorrhage)'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Paralysis (brain hemorrhage)'

-- Typhoid
UNION ALL SELECT disease_id, 'eat high calorie foods', 1 FROM diseases WHERE disease_name = 'Typhoid'
UNION ALL SELECT disease_id, 'antibiotic therapy', 2 FROM diseases WHERE disease_name = 'Typhoid'
UNION ALL SELECT disease_id, 'consult doctor', 3 FROM diseases WHERE disease_name = 'Typhoid'
UNION ALL SELECT disease_id, 'medication', 4 FROM diseases WHERE disease_name = 'Typhoid'

-- Hepatitis B
UNION ALL SELECT disease_id, 'consult nearest hospital', 1 FROM diseases WHERE disease_name = 'Hepatitis B'
UNION ALL SELECT disease_id, 'vaccination', 2 FROM diseases WHERE disease_name = 'Hepatitis B'
UNION ALL SELECT disease_id, 'eat healthy', 3 FROM diseases WHERE disease_name = 'Hepatitis B'
UNION ALL SELECT disease_id, 'medication', 4 FROM diseases WHERE disease_name = 'Hepatitis B'

-- Fungal infection
UNION ALL SELECT disease_id, 'bath twice', 1 FROM diseases WHERE disease_name = 'Fungal infection'
UNION ALL SELECT disease_id, 'use detol or neem in bathing water', 2 FROM diseases WHERE disease_name = 'Fungal infection'
UNION ALL SELECT disease_id, 'keep infected area dry', 3 FROM diseases WHERE disease_name = 'Fungal infection'
UNION ALL SELECT disease_id, 'use clean cloths', 4 FROM diseases WHERE disease_name = 'Fungal infection'

-- Hepatitis C
UNION ALL SELECT disease_id, 'consult nearest hospital', 1 FROM diseases WHERE disease_name = 'Hepatitis C'
UNION ALL SELECT disease_id, 'vaccination', 2 FROM diseases WHERE disease_name = 'Hepatitis C'
UNION ALL SELECT disease_id, 'eat healthy', 3 FROM diseases WHERE disease_name = 'Hepatitis C'
UNION ALL SELECT disease_id, 'medication', 4 FROM diseases WHERE disease_name = 'Hepatitis C'

-- Migraine
UNION ALL SELECT disease_id, 'meditation', 1 FROM diseases WHERE disease_name = 'Migraine'
UNION ALL SELECT disease_id, 'reduce stress', 2 FROM diseases WHERE disease_name = 'Migraine'
UNION ALL SELECT disease_id, 'use polaroid glasses in sun', 3 FROM diseases WHERE disease_name = 'Migraine'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Migraine'

-- Bronchial Asthma
UNION ALL SELECT disease_id, 'switch to loose clothing', 1 FROM diseases WHERE disease_name = 'Bronchial Asthma'
UNION ALL SELECT disease_id, 'take deep breaths', 2 FROM diseases WHERE disease_name = 'Bronchial Asthma'
UNION ALL SELECT disease_id, 'avoid dust', 3 FROM diseases WHERE disease_name = 'Bronchial Asthma'
UNION ALL SELECT disease_id, 'seek medical help', 4 FROM diseases WHERE disease_name = 'Bronchial Asthma'

-- Alcoholic hepatitis
UNION ALL SELECT disease_id, 'stop alcohol consumption', 1 FROM diseases WHERE disease_name = 'Alcoholic hepatitis'
UNION ALL SELECT disease_id, 'consult doctor', 2 FROM diseases WHERE disease_name = 'Alcoholic hepatitis'
UNION ALL SELECT disease_id, 'medication', 3 FROM diseases WHERE disease_name = 'Alcoholic hepatitis'
UNION ALL SELECT disease_id, 'follow up', 4 FROM diseases WHERE disease_name = 'Alcoholic hepatitis'

-- Jaundice
UNION ALL SELECT disease_id, 'drink plenty of water', 1 FROM diseases WHERE disease_name = 'Jaundice'
UNION ALL SELECT disease_id, 'consume milk thistle', 2 FROM diseases WHERE disease_name = 'Jaundice'
UNION ALL SELECT disease_id, 'eat fruits and vegetables', 3 FROM diseases WHERE disease_name = 'Jaundice'
UNION ALL SELECT disease_id, 'medication', 4 FROM diseases WHERE disease_name = 'Jaundice'

-- Hepatitis E
UNION ALL SELECT disease_id, 'rest', 1 FROM diseases WHERE disease_name = 'Hepatitis E'
UNION ALL SELECT disease_id, 'drink boiled water', 2 FROM diseases WHERE disease_name = 'Hepatitis E'
UNION ALL SELECT disease_id, 'avoid fatty food', 3 FROM diseases WHERE disease_name = 'Hepatitis E'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Hepatitis E'

-- Dengue
UNION ALL SELECT disease_id, 'drink papaya leaf juice', 1 FROM diseases WHERE disease_name = 'Dengue'
UNION ALL SELECT disease_id, 'avoid fatty spicy food', 2 FROM diseases WHERE disease_name = 'Dengue'
UNION ALL SELECT disease_id, 'keep mosquitos away', 3 FROM diseases WHERE disease_name = 'Dengue'
UNION ALL SELECT disease_id, 'keep hydrated', 4 FROM diseases WHERE disease_name = 'Dengue'

-- Hepatitis D
UNION ALL SELECT disease_id, 'consult doctor', 1 FROM diseases WHERE disease_name = 'Hepatitis D'
UNION ALL SELECT disease_id, 'medication', 2 FROM diseases WHERE disease_name = 'Hepatitis D'
UNION ALL SELECT disease_id, 'eat healthy', 3 FROM diseases WHERE disease_name = 'Hepatitis D'
UNION ALL SELECT disease_id, 'follow up', 4 FROM diseases WHERE disease_name = 'Hepatitis D'

-- Heart attack
UNION ALL SELECT disease_id, 'call ambulance', 1 FROM diseases WHERE disease_name = 'Heart attack'
UNION ALL SELECT disease_id, 'chew aspirin', 2 FROM diseases WHERE disease_name = 'Heart attack'
UNION ALL SELECT disease_id, 'keep calm', 3 FROM diseases WHERE disease_name = 'Heart attack'
UNION ALL SELECT disease_id, 'consult cardiologist', 4 FROM diseases WHERE disease_name = 'Heart attack'

-- Pneumonia
UNION ALL SELECT disease_id, 'rest', 1 FROM diseases WHERE disease_name = 'Pneumonia'
UNION ALL SELECT disease_id, 'drink fluids', 2 FROM diseases WHERE disease_name = 'Pneumonia'
UNION ALL SELECT disease_id, 'take antibiotics', 3 FROM diseases WHERE disease_name = 'Pneumonia'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Pneumonia'

-- Arthritis
UNION ALL SELECT disease_id, 'exercise', 1 FROM diseases WHERE disease_name = 'Arthritis'
UNION ALL SELECT disease_id, 'use hot and cold therapy', 2 FROM diseases WHERE disease_name = 'Arthritis'
UNION ALL SELECT disease_id, 'maintain healthy weight', 3 FROM diseases WHERE disease_name = 'Arthritis'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Arthritis'

-- Gastroenteritis
UNION ALL SELECT disease_id, 'drink oral rehydration solution', 1 FROM diseases WHERE disease_name = 'Gastroenteritis'
UNION ALL SELECT disease_id, 'avoid solid food', 2 FROM diseases WHERE disease_name = 'Gastroenteritis'
UNION ALL SELECT disease_id, 'rest', 3 FROM diseases WHERE disease_name = 'Gastroenteritis'
UNION ALL SELECT disease_id, 'consult doctor', 4 FROM diseases WHERE disease_name = 'Gastroenteritis'

-- Tuberculosis
UNION ALL SELECT disease_id, 'cover mouth', 1 FROM diseases WHERE disease_name = 'Tuberculosis'
UNION ALL SELECT disease_id, 'take medicine regularly', 2 FROM diseases WHERE disease_name = 'Tuberculosis'
UNION ALL SELECT disease_id, 'consult doctor', 3 FROM diseases WHERE disease_name = 'Tuberculosis'
UNION ALL SELECT disease_id, 'complete treatment', 4 FROM diseases WHERE disease_name = 'Tuberculosis';
