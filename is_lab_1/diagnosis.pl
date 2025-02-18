% Facts
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

% Rules
disease(flu) :- symptom(fever), symptom(cough), symptom(fatigue), symptom(muscle_aches).
disease(common_cold) :- symptom(runny_nose), symptom(sneezing), symptom(sore_throat), symptom(headache).
disease(pneumonia) :- symptom(fever), symptom(chest_pain), symptom(shortness_of_breath), symptom(cough).
disease(covid19) :- symptom(fever), symptom(cough), symptom(loss_of_taste), symptom(loss_of_smell).
disease(food_poisoning) :- symptom(nausea), symptom(vomiting), symptom(diarrhea).
disease(allergy) :- symptom(sneezing), symptom(runny_nose), symptom(skin_rash).
disease(bronchitis) :- symptom(cough), symptom(chest_pain), symptom(fatigue), symptom(wheezing).
disease(asthma) :- symptom(shortness_of_breath), symptom(wheezing), symptom(cough).
disease(migraine) :- symptom(headache), symptom(pressure_in_head), symptom(sensitivity_to_light).
disease(gastroenteritis) :- symptom(nausea), symptom(vomiting), symptom(diarrhea), symptom(abdominal_pain).

% Examples:
% ?- disease(flu).
% ?- disease(covid19).
% ?- disease(common_cold).
