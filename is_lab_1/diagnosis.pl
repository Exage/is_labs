% Определение симптомов
symptom(cough).
symptom(fever).
symptom(runny_nose).
symptom(sneezing).
symptom(sore_throat).
symptom(fatigue).
symptom(headache).
symptom(chest_pain).
symptom(shortness_of_breath).
symptom(muscle_aches).
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(loss_of_taste).
symptom(loss_of_smell).
symptom(skin_rash).

% Определение заболеваний и их симптомов
disease(flu, [fever, cough, fatigue, muscle_aches]).
disease(common_cold, [runny_nose, sneezing, sore_throat, headache]).
disease(pneumonia, [fever, chest_pain, shortness_of_breath, cough]).
disease(covid19, [fever, cough, loss_of_taste, loss_of_smell]).
disease(food_poisoning, [nausea, vomiting, diarrhea]).
disease(allergy, [sneezing, runny_nose, skin_rash]).
disease(bronchitis, [cough, chest_pain, fatigue, wheezing]).
disease(asthma, [shortness_of_breath, wheezing, cough]).
disease(migraine, [headache, pressure_in_head, sensitivity_to_light]).
disease(gastroenteritis, [nausea, vomiting, diarrhea, abdominal_pain]).

% Симптомы у разных пациентов
patient(john, [fever, cough, fatigue, muscle_aches]).
patient(anna, [runny_nose, sneezing, sore_throat]).
patient(mike, [fever, chest_pain, shortness_of_breath, cough]).
patient(sarah, [nausea, vomiting, diarrhea, abdominal_pain]).
patient(david, [cough, chest_pain, fatigue, wheezing]).

diagnose_patient(Patient, Disease) :-
    patient(Patient, Symptoms),
    disease(Disease, DiseaseSymptoms),
    forall(member(Symptom, DiseaseSymptoms), member(Symptom, Symptoms)).

recommend_disease(Symptoms, Disease) :-
    disease(Disease, DiseaseSymptoms),
    forall(member(Symptom, DiseaseSymptoms), member(Symptom, Symptoms)).

diagnose_by_symptoms(Symptoms, Disease) :-
    disease(Disease, DiseaseSymptoms),
    forall(member(Symptom, DiseaseSymptoms), member(Symptom, Symptoms)).

patient_with_symptom(Symptom, Patient) :-
    patient(Patient, Symptoms),
    member(Symptom, Symptoms).

disease_with_symptom(Symptom, Disease) :-
    disease(Disease, Symptoms),
    member(Symptom, Symptoms).

disease_symptoms(Disease, Symptoms) :-
    disease(Disease, Symptoms).

has_disease(Patient, Disease) :-
    diagnose_patient(Patient, Disease).

disease_partially_match(Patient, Disease) :-
    patient(Patient, Symptoms),
    disease(Disease, DiseaseSymptoms),
    subset(Symptoms, DiseaseSymptoms).

diseases_with_cough(Disease) :-
    disease(Disease, Symptoms),
    member(cough, Symptoms).

patients_with_symptoms(Symptoms, Patient) :-
    patient(Patient, PatientSymptoms),
    subset(Symptoms, PatientSymptoms).

symptoms_for_disease(Disease, Symptoms) :-
    disease(Disease, Symptoms).

diagnose_patient_partial(Patient, Disease) :-
    patient(Patient, Symptoms),
    disease(Disease, DiseaseSymptoms),
    intersection(Symptoms, DiseaseSymptoms, CommonSymptoms),
    length(CommonSymptoms, L),
    L > 0.

% Примеры запросов
% consult('/Users/nikita/Desktop/is_labs/is_lab_1/diagnosis.pl')

% diagnose_patient(john, Disease).
% patient_with_symptom(cough, Patient).
% disease_with_symptom(cough, Disease).
% disease_symptoms(flu, Symptoms).
% has_disease(sarah, gastroenteritis).
% disease_partially_match(john, Disease).
% diseases_with_cough(Disease).
% patients_with_symptoms([cough, fever], Patient).
% symptoms_for_disease(pneumonia, Symptoms).
% diagnose_patient_partial(john, pneumonia).
