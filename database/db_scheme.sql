-- =====================================================
-- CareAssist Database Schema
-- =====================================================

-- Use database (create manually or via RDS config)
-- CREATE DATABASE careassist;
-- USE careassist;

-- =====================================================
-- 1. PATIENTS
-- =====================================================
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    gender ENUM('MALE', 'FEMALE', 'OTHER') NOT NULL,
    date_of_birth DATE NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. PATIENT LOGIN
-- =====================================================
CREATE TABLE patient_login (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_patient_login_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);

-- =====================================================
-- 3. DOCTOR LOGIN
-- =====================================================
CREATE TABLE doctor_login (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 4. DOCTORS (PROFILE)
-- =====================================================
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    specialization VARCHAR(100),
    license_number VARCHAR(50) UNIQUE,
    years_of_experience INT,
    email VARCHAR(100),
    phone VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_doctor_profile
        FOREIGN KEY (doctor_id)
        REFERENCES doctor_login(doctor_id)
        ON DELETE CASCADE
);

-- =====================================================
-- 5. ADMIN LOGIN
-- =====================================================
CREATE TABLE admin_login (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 6. CONSULTATIONS (CENTRAL ENTITY)
-- =====================================================
CREATE TABLE consultations (
    consultation_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NULL,

    chief_complaint TEXT,
    doctor_remarks TEXT,

    status ENUM('PENDING', 'REVIEWED') DEFAULT 'PENDING',

    prediction_json JSON NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_consult_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_consult_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctor_login(doctor_id)
        ON DELETE SET NULL
);

-- =====================================================
-- 7. PATIENT VITALS (ONE ROW PER CONSULTATION)
-- =====================================================
CREATE TABLE patient_vitals (
    vitals_id INT AUTO_INCREMENT PRIMARY KEY,
    consultation_id INT NOT NULL,

    height_cm DECIMAL(5,2),
    weight_kg DECIMAL(5,2),
    temperature_c DECIMAL(4,1),

    systolic_bp INT,
    diastolic_bp INT,

    blood_sugar INT,
    heart_rate INT,
    spO2 INT,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vitals_consult
        FOREIGN KEY (consultation_id)
        REFERENCES consultations(consultation_id)
        ON DELETE CASCADE
);

-- =====================================================
-- 8. SYMPTOMS MASTER
-- =====================================================
CREATE TABLE symptoms_master (
    symptom_id INT AUTO_INCREMENT PRIMARY KEY,
    symptom_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50)
);

-- =====================================================
-- 9. CONSULTATION SYMPTOMS (M:N)
-- =====================================================
CREATE TABLE consultation_symptoms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    consultation_id INT NOT NULL,
    symptom_id INT NOT NULL,

    CONSTRAINT fk_cs_consult
        FOREIGN KEY (consultation_id)
        REFERENCES consultations(consultation_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_cs_symptom
        FOREIGN KEY (symptom_id)
        REFERENCES symptoms_master(symptom_id)
        ON DELETE CASCADE
);

-- =====================================================
-- 10. LOGIN AUDIT LOGS
-- =====================================================
CREATE TABLE login_audit_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_type ENUM('PATIENT', 'DOCTOR', 'ADMIN') NOT NULL,
    user_id INT NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    login_status ENUM('SUCCESS', 'FAILED') NOT NULL
);


ALTER TABLE doctor_login
ADD COLUMN doctor_id_fk INT;

ALTER TABLE doctor_login
ADD CONSTRAINT fk_doctor_login_doctor
FOREIGN KEY (doctor_id_fk) REFERENCES doctors(doctor_id);

CREATE TABLE diseases (
    disease_id INT AUTO_INCREMENT PRIMARY KEY,
    disease_name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE disease_precautions (
    precaution_id INT AUTO_INCREMENT PRIMARY KEY,
    disease_id INT NOT NULL,
    precaution_text VARCHAR(255) NOT NULL,
    precaution_order INT,

    CONSTRAINT fk_precaution_disease
        FOREIGN KEY (disease_id)
        REFERENCES diseases(disease_id)
        ON DELETE CASCADE
);